import subprocess
from hashlib import md5
from tempfile import mkstemp

from engine.converters import converter
from engine.path import Path


@converter('.rtf', '.docx', '.odt', '.csv', '.tsv', '.ipynb', '.dw', '.mw')
def load_pandoc_file(path: Path) -> str:
	"Convert files to HTML using pandoc."
	wiki = Path.cwd() / 'wiki'
	media_dir = (Path('resources') / 'media' / md5(str(path.relative_to(wiki)).encode('utf8')).hexdigest()).to_url_format()
	tmp = Path(mkstemp()[1])
	subprocess.check_call(['pandoc', '-o', str(tmp), '--extract-media', str(media_dir), str(path)], timeout=60)
	with open(tmp, 'r', encoding='utf8') as f:
		return f.read().replace(media_dir, f'/{media_dir}')
