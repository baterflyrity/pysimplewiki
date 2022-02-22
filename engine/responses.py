import mimetypes
from engine.path import Path


class Response:


	def __init__(self, code: int, text: str):
		self.text = text
		self.code = code

	def __str__(self) -> str:
		return f'HTTP/1.1 {self.code} {self.text}'

	def __bytes__(self) -> bytes:
		return str(self).encode('utf-8')


class RedirectResponse(Response):


	def __init__(self, url: str):
		super().__init__(301, 'Moved Permanently')
		self.url = url

	def __str__(self) -> str:
		return super().__str__() + f'\r\nLocation: {self.url}'


class NotFoundResponse(Response):


	def __init__(self):
		super().__init__(404, 'Not Found')


class DataResponse(Response):


	def __init__(self, data: bytes, mime: str = 'application/octet-stream'):
		super().__init__(200, 'OK')
		self.mime = mime
		self.data = data

	def __str__(self) -> str:
		return super().__str__() + f'\r\nContent-Length: {len(self.data)}\r\nConnection: close\r\nContent-Type: {self.mime}{"; charset=utf-8" if self.mime.startswith("text") else ""}'

	def __bytes__(self):
		return super().__bytes__() + b'\r\n\r\n' + self.data


class FileResponse(DataResponse):


	def __init__(self, file: Path):
		if not file.is_file():
			raise ValueError(f'Can not read file at {file}.')
		super().__init__(file.read_bytes(), mimetypes.guess_type(file, strict=False)[0])


class ServerErrorReponse(Response):


	def __init__(self):
		super().__init__(500, 'Internal Server Error')

class BadRequestReponse(Response):


	def __init__(self):
		super().__init__(400, 'Bad Request')
