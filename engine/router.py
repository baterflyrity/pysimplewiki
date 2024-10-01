from typing import Callable, Optional, Sequence

from engine.path import make_relative_url, Path
from engine.requests import IRequest, PageRequest, RedirectedRequest, ResourceRequest, SearchRequest, SectionRequest

Router = Callable[[Path], Optional[IRequest]]


class BadRequestedPath(ValueError):
	pass


class FileSystemRouter:
	"Routes requests relative to root directory."

	def __init__(self, wiki_root: Path = Path.cwd() / 'wiki', resources_root: Path = Path(Path.cwd() / 'resources'), index_patterns: Sequence[str] = ('index.*', 'main.*')):
		"""
		:param wiki_root: the most top directory to search wiki pages in.
		:param resources_root: the most top directory to search resource files in.
		:param index_patterns: glob patterns to search in case of directory wiki requests. In case not found returns directory listing.
		"""
		self.index_patterns = index_patterns
		self.resources_root = resources_root
		self.wiki_root = wiki_root

	@staticmethod
	def _resolve_path(root: Path, path: Path) -> Path:
		result = (root / path).resolve().absolute()
		if not result.is_relative_to(root):
			raise BadRequestedPath(f'Requested path {path} is outside of root directory {root}.')
		return result

	def __call__(self, requested_path: Path) -> Optional[IRequest]:
		if path := requested_path.match_start('./resources/'):
			path = FileSystemRouter._resolve_path(self.resources_root, path)
			if path.is_file():
				return ResourceRequest(path, self.resources_root)
			return
		if path := requested_path.match_start('./search/'):
			return SearchRequest(str(path).strip(), wiki_root=self.wiki_root)
		if path := requested_path.match_start('./wiki/'):
			return self._process_wiki_request(path)
		return RedirectedRequest(make_relative_url('wiki', requested_path))

	def _process_wiki_request(self, requested_path: Path) -> Optional[IRequest]:
		requested_path = FileSystemRouter._resolve_path(self.wiki_root, requested_path)
		if requested_path.name.startswith('.'):
			return SearchRequest(requested_path.name, self.wiki_root)
		if requested_path.is_dir():
			return SectionRequest(requested_path, self.wiki_root)
		if requested_path.is_file():
			return PageRequest(requested_path, self.wiki_root)
		if requested_path.exists():
			return
		files = [f for f in requested_path.parent.glob(f'{requested_path.name}.*') if f.is_file()]
		if not len(files):
			return SearchRequest(requested_path.name, self.wiki_root)
		return PageRequest(FileSystemRouter.resolve_page_file(files), self.wiki_root)

	@staticmethod
	def resolve_page_file(candidates: list[Path]) -> Path:
		return sorted(candidates)[0]
