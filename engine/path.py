from __future__ import annotations

import mimetypes
from dataclasses import dataclass
from pathlib import Path as PathBase
from typing import Literal, Self

import chardet

mimetypes.add_type('text/markdown', '.md', strict=False)
mimetypes.add_type('font/woff', '.woff', strict=False)
mimetypes.add_type('font/woff2', '.woff2', strict=False)

_IMPOSSIBLE_FILE_NAME = '0x5SXkOAsXZsKDdZsmUF8s00MSpMhpyN2CZ8S1BrCzCJdW3WbbDPuI17Nq5ahIBaPoPmEr9EUtsP4nOMUsj10YC4vJgwfmAogJae'


@dataclass
class FileContentDescription:
	text: str
	mime: str
	path: Path


class Path(type(PathBase())):

	# Interface unification for Linux and Windows.
	def is_relative_to(self, root: Path) -> bool:
		path = self._append_slash()
		base = root._append_slash()
		return len(path) >= len(base) and path.startswith(base)

	def relative_to(self, root: Path) -> Self:
		if not self.is_relative_to(root):
			raise ValueError(f'{self} is not in the subpath of {root} OR one path is relative and the other is absolute.')
		if self.is_the_same(root):
			return Path('.')
		return Path(str(self.absolute()).removeprefix(root._append_slash()))

	def is_the_same(self, other: Path) -> bool:
		"""
		Whether both paths point to the same location.
		"""
		return self.resolve() == other.resolve()

	def is_child_of(self, parent: Path) -> bool:
		"""
		Whether the current path is relative to parent but not the same.
		"""
		return self.is_relative_to(parent) and not self.is_the_same(parent)

	def _append_slash(self) -> str:
		return str(self.absolute() / _IMPOSSIBLE_FILE_NAME).removesuffix(_IMPOSSIBLE_FILE_NAME)

	@classmethod
	def cwd(cls) -> Self:
		return Path(PathBase.cwd())

	def startswith(self, prefix: str) -> bool:
		"""
		Check whether path is relative to prefix.
		"""
		return self.is_relative_to(Path(prefix))

	def removeprefix(self, prefix: str) -> Self:
		"""
		Make path relative to prefix.
		"""
		return self.relative_to(Path(prefix))

	def match_start(self, prefix: str) -> Self | Literal[False]:
		"""
		Checks whether the path starts with defined prefix and returns new path with removed prefix. Otherwise, returns False.
		"""
		if self.startswith(prefix):
			return self.removeprefix(prefix)
		return False

	def guess_mime(self) -> str | None:
		"Try to guess mime type of file. Returns None when can not guess."
		return mimetypes.guess_type(self, strict=False)[0]

	def guess_encoding(self) -> str | None:
		"Try to guess encoding of text file. Returns None when can not guess."
		content = self.read_bytes()
		try:
			encoding = chardet.detect(content)['encoding']
			if not encoding:
				return
			content.decode(encoding)  # just test whether guess is right
			return encoding
		except UnicodeDecodeError:
			return

	def guess_text(self, strict: bool = True) -> FileContentDescription | None:
		"""
		Try to guess encoding and optionally mime type.

		In case can not guess returns None.

		:param strict: whether to guess encoding only for textual mime types.
		"""
		mime = self.guess_mime()
		if mime is None or strict and not mime.startswith('text'):
			return
		encoding = self.guess_encoding()
		if encoding is None:
			return
		return FileContentDescription(text=self.read_text(encoding), mime=mime, path=self)

	@property
	def parent(self) -> Self:
		return Path(super().parent)

	def to_url_format(self) -> str:
		"Make web style slashes."
		return str(self).replace('\\', '/')

	def glob(self, pattern, *, case_sensitive: bool | None = None, ignore_dotted: bool = True) -> list[Path]:
		return sorted(Path(entry) for entry in super().glob(pattern, case_sensitive=case_sensitive) if not ignore_dotted or not entry.name.startswith('.'))

	def rglob(self, pattern, *, case_sensitive=None, ignore_dotted: bool = True) -> list[Path]:
		entries = []
		for entry in self.glob(pattern, case_sensitive=case_sensitive, ignore_dotted=ignore_dotted):
			if entry.is_dir():
				entries += entry.rglob(pattern, case_sensitive=case_sensitive, ignore_dotted=ignore_dotted)
			else:
				entries.append(entry)
		return sorted(entries)


def make_relative_url(root: str | Path, path: Path, *, drop_extension: bool = False) -> str:
	root = Path(root)
	if path.is_absolute() and not path.is_relative_to(root):
		raise ValueError('Can not generate relative URL for absolute path outside of root.')
	if path.is_file() and drop_extension:
		path = path.with_suffix('')
	return '/' + (root / path).to_url_format()
