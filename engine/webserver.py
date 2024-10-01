"""Simple HTTP 1.1 web server."""
import os
import re
import socket
import sys
import urllib
from typing import Optional
from urllib.parse import urlparse

from engine.handler import RequestHandler, handle_request_by_type
from engine.logging import logger
from engine.path import Path
from engine.responses import BadRequestReponse, NotFoundResponse, Response, ServerErrorReponse
from engine.router import BadRequestedPath, FileSystemRouter, Router


def _parse_request_path(text: str) -> Optional[Path]:
	"""
	Parse HTTP request and return requested path or None.
	"""
	if (match := re.match(r'\s*GET\s+([^\s]+)', text)) is not None:
		url = urlparse(match.group(1))
		if len(url.scheme) != 0 and url.scheme != 'http':
			return
		if len(url.path) == 0:
			return Path('./')
		return Path('.' + urllib.parse.unquote(url.path))


def _process_request(request: str, *, router: Router, handle: RequestHandler) -> Response:
	try:
		if (requested_path := _parse_request_path(request)) is None:
			return NotFoundResponse()
		logger.info('\tRequested path ', requested_path)
		try:
			routed_request = router(requested_path)
		except BadRequestedPath as ex:
			logger.warning('\tRequest error', str(ex))
			logger.exception(ex)
			return BadRequestReponse()
		if routed_request is None:
			return NotFoundResponse()
		logger.info('\tRouted to ', str(routed_request))
		return handle(routed_request)
	except Exception as ex:
		logger.warning('\tError', str(ex))
		logger.exception(ex)
		if os.getenv('DEBUG', False):
			raise
		return ServerErrorReponse()


def serve(interface: str = '0.0.0.0', port: int = 80, router: Router = FileSystemRouter(), handle: RequestHandler = handle_request_by_type, buble_sigint: bool = False):
	"""
	Listen forever.

	:param interface: Interface IP v4 address or resolvable name (like "127.0.0.1" or "localhost") on which to serve. Use "0.0.0.0" for all connected interfaces.
	:param port: Port on which to serve.
	:param router: routing callback that must return requested path or None for 404 Error.
	:param handle:  response body generation callback.
	"""
	logger.info(f'Hosting at http://{interface or "localhost"}:{port} of {Path.cwd().resolve().absolute()}.')
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
		server.settimeout(1)
		server.bind((interface, port))
		server.listen(999)
		try:
			while True:
				try:
					client, addr = server.accept()
					logger.info('Connected by', addr)
					request = client.recv(2048)  # according to https://stackoverflow.com/a/417184 maximum url length is up to 2000 characters so 2048 bytes buffer size must be enough ro receive main path header
					response = _process_request(request.decode('utf-8'), router=router, handle=handle)
					logger.debug('\tSending response', response.code, response.text)
					client.sendall(bytes(response))
					logger.debug('\tDisconnecting client\r\n')
					client.close()
				except TimeoutError:
					logger.debug('Timed out')
				except Exception as e:
					logger.warning(f'Error while processing request: {e}')
					logger.exception(e)
		except KeyboardInterrupt:
			logger.info('Exit')
			if buble_sigint:
				raise


if __name__ == '__main__':
	logger.info('Using first and second arguments as interface and port.')
	interface = sys.argv[1] if len(sys.argv) >= 2 else '0.0.0.0'
	port = int(sys.argv[2]) if len(sys.argv) >= 3 else 80
	serve(interface=interface, port=port)
