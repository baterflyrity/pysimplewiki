from __future__ import annotations
import dataclasses
import pickle
from hashlib import md5, sha1

from engine.converters import get_content
from engine.path import Path
from engine.logging import logger


@dataclasses.dataclass
class CachedFile:
	md5: str
	"MD5 hash of original content."
	sha1: str
	"SHA1 hash of original content."
	content: str | None
	"HTML markup converted from original content."

	def has_changed(self, file: Path) -> bool:
		"""
		Whether cached file has changed.
		"""
		f = CachedFile.from_file(file, None)
		return f.md5 != self.md5 or f.sha1 != self.sha1

	def serialize(self) -> dict[str, str]:
		return dataclasses.asdict(self)

	@staticmethod
	def deserialize(data: dict[str, str]) -> CachedFile:
		return CachedFile(**data)

	@staticmethod
	def from_file(file: Path, content: str | None) -> CachedFile:
		data = file.read_bytes()
		return CachedFile(md5=md5(data).hexdigest(), sha1=sha1(data).hexdigest(), content=content)


class Cache:

	def __init__(self, path: Path, root: Path = Path.cwd() / 'wiki', preload: bool = True):
		self._version = 1
		self.path = path
		self.root = root
		self.files: dict[str, CachedFile] = {}
		self.load()
		self.purge()
		if preload:
			self.preload()

	def purge(self):
		"""
		Remove old files that do not exist anymore.
		"""
		old = len(self.files)
		for f in list(self.files):
			if not (self.root / f).is_file():
				del self.files[f]
		if len(self.files) != old:
			self.save()

	def preload(self):
		logger.info('Preloading cache...')
		old_files = set(self.files)
		for entry in self.root.rglob('*'):
			if entry.is_file() and not entry.name.startswith('.') and all([not parent.name.startswith('.') for parent in entry.parents]):
				self.get_content(entry, save=False)
		preloaded_files = set(self.files) - old_files
		if len(preloaded_files):
			logger.info(f'Preloaded {len(preloaded_files)} article pages from {", ".join(preloaded_files)}.')
		self.save()

	def get_content(self, file: Path, save: bool = True) -> str | None:
		if not file.is_relative_to(self.root):
			raise ValueError(f'Requested file {file} is outside of cache folder.')
		key = file.relative_to(self.root).to_url_format()
		if key not in self.files or self.files[key].has_changed(file):
			self.files[key] = CachedFile.from_file(file, get_content(file))
			if save:
				self.save()
		return self.files[key].content

	def __getitem__(self, file: Path) -> str | None:
		return self.get_content(file=file)

	def serialize(self) -> dict[str, int | dict[str, dict[str, str]]]:
		return {
			'version': self._version,
			'files'  : {p: f.serialize() for p, f in self.files.items()}
		}

	def deserialize(self, data: dict[str, ...]):
		self._version = data['version']
		self.files = {p: CachedFile.deserialize(f) for p, f in data['files'].items()}

	def save(self):
		self.path.write_bytes(pickle.dumps(self.serialize()))

	def load(self):
		if self.path.exists():
			self.deserialize(pickle.loads(self.path.read_bytes()))

	def __del__(self):
		# self.save()
		pass


cache = Cache(Path.cwd() / 'cache.pkl', root=Path('wiki'))
