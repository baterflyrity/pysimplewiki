from __future__ import annotations
from pathlib import Path as PathBase

_IMPOSSIBLE_FILE_NAME = '0x5SXkOAsXZsKDdZsmUF8s00MSpMhpyN2CZ8S1BrCzCJdW3WbbDPuI17Nq5ahIBaPoPmEr9EUtsP4nOMUsj10YC4vJgwfmAogJae'


class Path(type(PathBase())):


	# Interface unification for Linux and Windows.
	def is_relative_to(self, root: Path) -> bool:
		path = self._append_slash()
		base = root._append_slash()
		return len(path) >= len(base) and path.startswith(base)

	def relative_to(self, root: Path) -> Path:
		if not self.is_relative_to(root):
			raise ValueError(f'{self} is not in the subpath of {root} OR one path is relative and the other is absolute.')
		return Path(str(self.absolute()).removeprefix(root._append_slash()))

	def _append_slash(self) -> str:
		return str(self.absolute() / _IMPOSSIBLE_FILE_NAME).removesuffix(_IMPOSSIBLE_FILE_NAME)
	#
	# @classmethod
	# def cwd(cls) -> Path:
	# 	return PathBase.cwd()
