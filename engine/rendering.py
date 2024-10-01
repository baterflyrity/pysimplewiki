import jinja2

from engine.path import Path
from engine.settings import settings

templates = jinja2.Environment(loader=jinja2.FileSystemLoader(Path.cwd() / 'templates'), autoescape=True)


def render(template: str, **rendering_arguments) -> str:
	"""
	Render template by name with defined settings.

	Automatically add config parameters to each template context.

	:param template: HTML markup template name (without .html extension) in ./templates/ directory.
	"""
	return templates.get_template(template).render(config=settings, **rendering_arguments)
