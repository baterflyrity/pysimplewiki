from engine.path import Path


class IRequest:
	"Base class of user requests."
	pass


class RedirectedRequest(IRequest):


	def __init__(self, url: str):
		self.url = url

	def __str__(self):
		return f'[Redirect] {self.url}'


class RootRequest(IRequest):


	def __init__(self, root: Path):
		if not root.is_dir():
			raise ValueError(f'Root directory {root} does not exist.')
		self.root = root

	def __str__(self):
		return f'[Root] {self.root}'


class SearchRequest(RootRequest):
	"Search query."

	def __init__(self, query: str, wiki_root: Path):
		super().__init__(root=wiki_root)
		self.query = query

	def __str__(self):
		return f'[Search] {self.query}'


class FileSystemRequest(RootRequest):
	"Request of file or directory."

	def __init__(self, path: Path, root: Path):
		super().__init__(root=root)
		self.path = path

	def __str__(self):
		return f'[File system] {self.path.relative_to(self.root)}'


class ResourceRequest(FileSystemRequest):
	"Request of resource file, e.g. script, style, favicon."

	def __init__(self, path: Path, root: Path):
		if not path.is_file():
			raise ValueError(f'Requested resource {path} does not point to resource file.')
		super().__init__(path=path, root=root)


class PageRequest(FileSystemRequest):
	"Request of wiki page. Must point to file."

	def __init__(self, path: Path, root: Path):
		if not path.is_file():
			raise ValueError(f'Requested page {path} does not exist.')
		super().__init__(path=path, root=root)


class SectionRequest(FileSystemRequest):
	"Request of wiki section. Must point to directory."

	def __init__(self, path: Path, root: Path):
		if not path.is_dir():
			raise ValueError(f'Requested section {path} does not exist.')
		super().__init__(path=path, root=root)
