from time import sleep
from typing import Annotated

import typer

from engine.logging import logger
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
		restart: Annotated[bool, typer.Option('--restart', help='Self-restart on critical error.', show_default=True, envvar='WIKI_RESTART')] = False,

):
	"""
	Run wiki server.
	"""
	while True:
		try:
			logger.info('Starting Simple Wiki...')
			serve(interface=interface, port=port, buble_sigint=True)
		except KeyboardInterrupt:
			raise typer.Exit(0)
		except Exception as e:
			logger.critical(f'Critical error: {e}')
			logger.exception(e)
			if debug:
				raise
			if not restart:
				raise typer.Exit(-1)
		logger.info('Restarting in 5 seconds...')
		sleep(5)


if __name__ == '__main__':
	app()
