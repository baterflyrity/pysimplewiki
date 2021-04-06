"""Simple HTTP 1.1 web server."""
import mimetypes
import re
import socket
import urllib
from pathlib import Path
from typing import Optional, Callable, Tuple
from urllib.parse import urlparse


def parse_request(text: str) -> Optional[str]:
	"""
	Parse HTTP request and return requested path or None.
	"""
	if (match := re.match(r'\s*GET\s+([^\s]+)', text)) is not None:
		url = urlparse(match.group(1))
		if len(url.scheme) != 0 and url.scheme != 'http':
			return None
		elif len(url.path) == 0:
			return './'
		else:
			return '.' + urllib.parse.unquote(url.path)
	else:
		return None


def generate_response(body: bytes, type: str = None) -> bytes:
	"""
	Generate HTTP 1.0 response with 200 status code, Content-Length, Content-Type and Connection: close headers.
	"""
	charset = '; charset=utf-8' if type.startswith('text') else ''
	return ('\r\n'.join([
		'HTTP/1.1 200 OK',
		f'Content-Length: {len(body)}',
		f'Content-Type: {type or "application/octet-stream"}{charset}',
		'Connection: close',
	]) + '\r\n\r\n').encode('utf-8') + body


def default_routing_callback(requested_path: Path) -> Optional[Path]:
	"""
	Default callback for requested path routing that maps direcotry paths to directory/index.html ones.
	"""
	if '.' not in requested_path.name:
		return requested_path / 'index.html'
	else:
		return requested_path


def default_response_callback(requested_path: Path) -> Optional[Tuple[bytes, str]]:
	"""
	Default callback for response that return specified file content.
	"""
	if requested_path.exists() and requested_path.is_file():
		return requested_path.read_bytes(), mimetypes.guess_type(requested_path, strict=False)[0]


def serve(directory: Path = Path.cwd(), interface: str = '0.0.0.0', port: int = 80, routing_callback: Callable[[Path], Optional[Path]] = default_routing_callback, response_callback: Callable[[Path], Optional[Tuple[bytes, str]]] = default_response_callback):
	"""
	Listen forever.

	:param directory: directory to server as web root.
	:param interface: Interface IP v4 address or resolvable name (like "127.0.0.1" or "localhost") on which to serve. Use "0.0.0.0" for all connected interfaces.
	:param port: Port on which to serve.
	:param routing_callback: routing callback that must return requested path or None.
	:param response_callback:  response body generation callback that must return bytes and MIME type or None.
	"""
	print('Starting to serve', directory, f'at http://{interface or "localhost"}:{port}')
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
		server.bind((interface, port))
		server.listen(999)
		while True:
			client, addr = server.accept()
			print('Connected by', addr)
			request = client.recv(2048)  # according to https://stackoverflow.com/a/417184 maximum url length is up to 2000 characters so 2048 bytes buffer size must be enough ro receive main path header
			requested_path = parse_request(request.decode('utf-8'))
			print('\tRequested path ', requested_path)
			requested_path = routing_callback(directory / Path(requested_path))
			print('\tRouted path ', requested_path)
			if requested_path is not None:
				if requested_path.is_relative_to(directory):
					response = response_callback(requested_path)
					if response is not None:
						client.sendall(generate_response(*response))
						print('\tSent data to client')
			print('\tDisconnecting client\r\n')
			client.close()
