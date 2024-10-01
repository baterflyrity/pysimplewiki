import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import auto, Enum
from typing import Self

from engine.cache import cache
from engine.converters import get_content
from engine.path import Path
from engine.rendering import render
from engine.requests import PageRequest, RootRequest, SearchRequest, SectionRequest
from engine.responses import DataResponse, FileResponse, Response
from engine.settings import settings


class LinkType(Enum):
	Article = auto()
	Section = auto()


@dataclass
class Link:
	name: str
	url: str
	type: LinkType

	def __repr__(self):
		return f'{self.type.value}: {self.name} ({self.url})'

	def __str__(self):
		return repr(self)

	@staticmethod
	def from_path(path: Path, type: LinkType | None, wiki_root: Path) -> Self:
		if type is None:
			if path.is_file():
				type = LinkType.Article
			elif path.is_dir():
				type = LinkType.Section
			else:
				raise ValueError(f'Can not autodetect link type for path: {path.resolve()}.')
		wiki_path = path.relative_to(wiki_root)
		if type is LinkType.Article:
			wiki_path = wiki_path.with_suffix('')
		return Link(name=wiki_path.name, url=f'/wiki/{wiki_path}', type=type)


class IPage(ABC):
	"""Base class for all wiki pages."""

	def __init__(self, request: RootRequest):
		self.request = request

	def render(self) -> DataResponse:
		"""Generate response from page content."""
		content = self._render_markup()
		if isinstance(content, Response):
			return content
		return DataResponse(content.encode('utf-8'), 'text/html')

	@property
	@abstractmethod
	def content(self) -> str | Response:
		"""Must return page content HTML markup."""
		...

	@property
	@abstractmethod
	def current_path(self) -> Path:
		"""Must return path of requested file or directory."""
		...

	def _render_markup(self) -> str | Response:
		content = self.content
		if isinstance(content, Response):
			return content
		logo = ''
		logo_path = Path('resources') / settings["logo"]
		if logo_path.exists() and logo_path.is_file():
			logo = logo_path.read_text(encoding='utf-8')
		return render('page.html', content=content, sidebar=self._render_sidebar(), icon=settings["icon"], logo=logo)

	def _render_sidebar(self) -> str:
		current_section = self.current_path.parent if isinstance(self.request, PageRequest) else self.current_path
		main_links = [Link(name='Заглавная страница', url='/wiki/', type=LinkType.Section)]
		# get top level sections
		if not self.request.root.is_the_same(self.current_path):
			for section in [self.current_path.parent, self.current_path.parent.parent]:
				if section.is_child_of(self.request.root):
					main_links.append(Link.from_path(section, LinkType.Section, self.request.root))
		siblings = [Link.from_path(f, LinkType.Article, self.request.root) for f in current_section.glob('*') if f.is_file() and not self.current_path.is_the_same(f)]
		subsections = [Link.from_path(f, LinkType.Section, self.request.root) for f in current_section.glob('*') if f.is_dir() and not self.current_path.is_the_same(f)]
		return self._render_side_block(main_links, sort=False) + self._render_side_block(siblings, 'Статьи в разделе') + self._render_side_block(subsections, 'Подразделы')

	def _render_side_block(self, links: list[Link], label: str = '', *, sort: bool = True, maximum: int = 10) -> str:
		"""
		Generate block of links markup for sidebar.

		:param label: label of block.
		:param links: list of Links. Returns empty string in case of empty list.
		:param sort: whether to sort links by name (label).
		:param maximum: maximum amount of links to render. Chooses random sample in case of overflow.
		"""
		if not len(links):
			return ''
		if len(links) > maximum:
			links = random.sample(links, maximum)
		if sort:
			links = sorted(links, key=lambda link: link.name)
		return render('side_block.html', label=label, links=links)


class SearchPage(IPage):


	@property
	def content(self) -> str:
		return render('search_results.html', query=self.request.query, found=[Link.from_path(self.request.root / x, None, self.request.root) for x in self.found])

	@property
	def current_path(self) -> Path:
		return self.request.root

	@staticmethod
	def match_text(query: str, text: str, minimum_length: int = 3) -> bool:
		"""
		Whether query is a substring of text.
		"""
		if len(query) < minimum_length or len(text) < minimum_length:
			return False
		return query.lower() in text.lower()

	@staticmethod
	def match_content(query: str, file: Path, minimum_length: int = 3) -> bool:
		"""
		Whether query is a substring of text file's content.
		"""
		if (content := file.guess_text()) is not None and SearchPage.match_text(query, content.text, minimum_length=minimum_length):
			return True
		return False

	def __init__(self, request: SearchRequest):
		super().__init__(request)
		self.found = set()
		for path in request.root.rglob('*'):
			if not path.is_dir() and not path.is_file():
				continue
			if SearchPage.match_text(request.query, str(path.relative_to(request.root))):
				self.found.add(path.relative_to(self.request.root))
			elif path.is_file() and SearchPage.match_content(request.query, path):
				self.found.add(path.relative_to(self.request.root))
		for p, f in cache.files.items():
			if f.content is not None and SearchPage.match_text(request.query, f.content):
				self.found.add((cache.root / p).relative_to(self.request.root))


class SectionPage(IPage):


	@property
	def content(self) -> str:
		links = [Link.from_path(x, None, self.request.root) for x in self.current_path.glob('*') if x.is_file() or x.is_dir()]
		return render('section.html', section=self.current_path.name, subsections=[x for x in links if x.type == LinkType.Section], pages=[x for x in links if x.type == LinkType.Article])

	@property
	def current_path(self) -> Path:
		return self.request.path

	def __init__(self, request: SectionRequest):
		super().__init__(request)
		self.subsections: set[Path] = set()
		self.pages: set[Path] = set()
		for entry in request.path.glob('*'):
			if entry.is_dir():
				self.subsections.add(entry)
			elif entry.is_file():
				self.pages.add(entry.with_suffix(''))


class FilePage(IPage):


	@property
	def content(self) -> str | Response:
		if (content := cache[self.current_path]) is not None:
			return content
		return FileResponse(self.current_path)

	@property
	def current_path(self) -> Path:
		return self.request.path

	def __init__(self, request: PageRequest):
		super().__init__(request)
