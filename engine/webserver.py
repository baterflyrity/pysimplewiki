"""Simple HTTP 1.1 web server."""
import re
import socket
import urllib
from typing import Callable, Optional
from urllib.parse import urlparse

from engine.responses import BadRequestReponse, FileResponse, NotFoundResponse, Response, ServerErrorReponse
from engine.router import FileSystemRouter, Router
from engine.path import Path

RequestHandle = Callable[[Path], Response]


def _parse_request_path(text: str) -> Optional[Path]:
	"""
	Parse HTTP request and return requested path or None.
	"""
	if (match := re.match(r'\s*GET\s+([^\s]+)', text)) is not None:
		url = urlparse(match.group(1))
		if len(url.scheme) != 0 and url.scheme != 'http':
			return
		elif len(url.path) == 0:
			return Path('./')
		else:
			return Path('.' + urllib.parse.unquote(url.path))


def _process_request(request: str, *, router: Router, handle: RequestHandle, check_directory: bool) -> Response:
	try:
		if (requested_path := _parse_request_path(request)) is None:
			return NotFoundResponse()
		print('\tRequested path ', requested_path)
		if (routed_path := router(requested_path)) is None:
			return NotFoundResponse()
		print('\tRouted path ', routed_path)
		if check_directory and not routed_path.is_relative_to(Path.cwd()):
			return BadRequestReponse()
		return handle(routed_path)
	except Exception as ex:
		print('\tError', ex)
		return ServerErrorReponse()


def serve(interface: str = '0.0.0.0', port: int = 80, router: Router = FileSystemRouter(), handle: RequestHandle = FileResponse, check_directory: bool = True):
	"""
	Listen forever.

	:param interface: Interface IP v4 address or resolvable name (like "127.0.0.1" or "localhost") on which to serve. Use "0.0.0.0" for all connected interfaces.
	:param port: Port on which to serve.
	:param router: routing callback that must return requested path, or url string for redirection or None for 404 Error.
	:param handle:  response body generation callback that must return bytes and MIME type or None.
	"""
	print(f'Hosting at http://{interface or "localhost"}:{port} of {Path.cwd().absolute()}.')
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
		server.bind((interface, port))
		server.listen(999)
		try:
			while True:
				client, addr = server.accept()
				print('Connected by', addr)
				request = client.recv(2048)  # according to https://stackoverflow.com/a/417184 maximum url length is up to 2000 characters so 2048 bytes buffer size must be enough ro receive main path header
				response = _process_request(request.decode('utf-8'), router=router, handle=handle, check_directory=check_directory)
				print('\tSending response', response.code, response.text)
				client.sendall(bytes(response))
				print('\tDisconnecting client\r\n')
				client.close()
		except KeyboardInterrupt:
			print('Exit')
