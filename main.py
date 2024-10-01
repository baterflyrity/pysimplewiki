from typing import Annotated

import typer
from rich import print

from engine.settings import settings

__version__ = '0.2.0'

from engine.webserver import serve

app = typer.Typer(add_completion=False)


def validate_port(port: int) -> int:
	"""
	Check whether port index is valid.
	"""
	if not (0 < port <= 65535):
		raise typer.BadParameter('Port value must be in range from 1 to 65535.')
	return port


def show_version(value: bool):
	"""
	Print version information and exit.
	"""
	if value:
		typer.echo(f"Simple Wiki {__version__}")
		raise typer.Exit()


@app.command()
def cli(
		interface: Annotated[str, typer.Option('--interface', '-i', help='Interface IP v4 address or resolvable name (like "127.0.0.1" or "localhost") on which to serve wiki. Default value is "0.0.0.0" for all connected interfaces. Overwrites config.json.', show_default=True, envvar='WIKI_INTERFACE')] = settings['interface'],
		port: Annotated[int, typer.Option('--port', '-p', help='Port on which to serve wiki. Default value is 80 for all connected interfaces. Overwrites config.json.', callback=validate_port, show_default=True, envvar='WIKI_PORT')] = settings['port'],
		version: Annotated[bool, typer.Option("--version", callback=show_version, is_eager=True, help=show_version.__doc__)] = False,
		debug: Annotated[bool, typer.Option('--debug', help='Print more information about errors.', show_default=True, envvar='DEBUG')] = False,
):
	"""
	Run wiki server.
	"""
	try:
		serve(interface=interface, port=port)
	except Exception as e:
		print(f'[red]{e}[/]')
		if debug:
			raise
		typer.Exit(-1)


if __name__ == '__main__':
	app()
