from typing import Callable, Optional

from engine.path import Path

Router = Callable[[Path], Optional[Path]]


class FileSystemRouter:


	def __init__(self, root: Path = Path.cwd() / 'htdocs', redirect_directories: Optional[str] = 'index.html'):
		self.redirect_directories = redirect_directories
		self.root = root

	def __call__(self, path: Path) -> Optional[Path]:
		path = self.root / path
		if path.is_dir():
			if self.redirect_directories is not None:
				path /= self.redirect_directories
		if path.is_file():
			return path
