from engine.converters import converter
from engine.path import Path


@converter('.html', '.htm')
def load_sourcecode_file(path: Path) -> str:
	"""
	Just load HTML markup.
	"""
	sources = path.guess_text()
	if sources:
		return sources.text
