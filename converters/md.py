import re

from markdown import markdown

from engine.converters import converter
from engine.path import make_relative_url, Path


@converter('.md')
def load_markdown_file(path: Path) -> str:
	"Convert markdown file to HTML."
	if (content := path.guess_text()) is not None:
		return markdown(content.text, extensions=['extra', 'mdx_math', 'admonition', 'toc', 'wikilinks'], extension_configs={
			'extra':     {
				'footnotes':   {
					'UNIQUE_IDS': True
				},
				'fenced_code': {
					'lang_prefix': 'lang-'
				}
			},
			'mdx_math':  {
				'enable_dollar_delimiter': True,
				'add_preview':             True
			},
			'wikilinks': {
				# 'pattern':   r'\[\[([\w0-9_ \t-/#]+)\]\]',
				'build_url': make_internal_link
			}
		})


def make_internal_link(label, *_):
	wiki_path = Path.cwd() / 'wiki'
	label = re.sub(r'\s*/\s*', '/', label)
	match = re.search(r'\s*#.*', label)
	if match:
		anchor = re.sub(r'\s*#\s*', '#', match.group())
		label = label[:match.start(0)]
	else:
		anchor = ''
	found = list(wiki_path.rglob(f'{label}*'))
	if len(found) != 0:
		name = found[0].name.split('.')[0]
		label = str(found[0].relative_to(wiki_path))
	else:
		name = label.split('/')[-1]
	# if len(anchor) != 0:
	# 	name = anchor[1:]
	return f'{make_relative_url("wiki", Path(label),drop_extension=True)}{anchor}'
