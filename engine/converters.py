import importlib
import importlib.util
from collections import defaultdict
from importlib.machinery import ModuleSpec
from types import ModuleType
from typing import Callable

from engine.path import Path

processors: dict[str, Callable[[Path], str | None]] = defaultdict(lambda: lambda *_, **__: None)
post_processors: list[Callable[[str], str]] = []


class ConvertionError(RuntimeError):
	pass


class PostProcessingError(ConvertionError):
	pass


def converter(*extensions: str) -> Callable[[Callable[[Path], str | None]], Callable[[Path], str | None]]:
	"""
	Converter function decorator.

	Decorated function should accept path to file with specified extension and return HTML markup for page content.

	If converter/extension has been already defined overrides it.

	:param extension: file extension with dot, e.g. '.docx', which can be processed with this converter.
	"""

	def decorator(processor: Callable[[Path], str | None]) -> Callable[[Path], str | None]:
		for extension in extensions:
			processors[extension] = processor
		return processor

	return decorator


def post_converter(processor: Callable[[str], str]) -> Callable[[str], str]:
	"""
	Post converter function decorator.

	Decorated function should accept HTML markup for page content and return processed HTML markup.

	Post converters are user in sequence of definition/decoration and after appropriate converter acquired markup from file.
	"""
	post_processors.append(processor)
	return processor


def load_converters(directory: Path = Path.cwd() / 'converters', recursively: bool = True, pattern: str = '*.py') -> dict[str, ModuleType]:
	"""
	Load all converters from specified directory.

	Actually imports all Python files from directory.

	:param directory: path to directory with converter files (*.py).
	:param recursively: whether to search for Python files in subdirectories.
	:param pattern: glob search pattern.
	:return: dictionary of loaded files. Each file is named as converters.package{i} where i=0..N-1.
	"""
	modules = {}
	files = directory.rglob(pattern) if recursively else directory.glob(pattern)
	for i, file in enumerate(files):
		name = f"converters.package{i}"
		spec: ModuleSpec = importlib.util.spec_from_file_location(name, file)
		module: ModuleType = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(module)
		modules[name] = module
	return modules


def get_content(file: Path) -> str | None:
	"""
	Use currently loaded processors to convert file.

	:return: HTML markup of file or None
	"""
	processor = processors[file.suffix]
	try:
		content = processor(file)
	except Exception as ex:
		raise ConvertionError(f'Can not convert {file}.') from ex
	if content is None and (desc := file.guess_text()) is not None:
		content = f'<pre>{desc.text}</pre>'
	if content is None:
		return None
	for pp in post_processors:
		try:
			content = pp(content)
		except Exception as ex:
			raise PostProcessingError(f'Can not post process file {file}.') from ex
	return content


_converters = load_converters()
"Dynamically preloaded modules (*.py files) from ./converters/ directory."
