from typing import Callable, Dict, Type

from engine.pages import FilePage, IPage, SearchPage, SectionPage
from engine.requests import IRequest, PageRequest, RedirectedRequest, ResourceRequest, RootRequest, SearchRequest, SectionRequest
from engine.responses import DataResponse, FileResponse, RedirectResponse, Response, ServerErrorReponse

RequestHandler = Callable[[IRequest], Response]


class RequestTypeHandler(Dict[Type[IRequest], RequestHandler]):
	"Handlers by request type are assigned to this as dict."

	def __init__(self, handlers: Dict[Type[IRequest], RequestHandler] = None):
		defaults = {
			RedirectedRequest: self._handle_redirect,
			ResourceRequest:   self._handle_resource,
			SearchRequest:     self._handle_search,
			PageRequest:       self._handle_article,
			SectionRequest:    self._handle_section,
		}
		if handlers:
			defaults.update(handlers)
		super().__init__(defaults)

	def __call__(self, request: IRequest) -> Response:
		key = type(request)
		if key in self:
			return self[key](request)
		return ServerErrorReponse()

	def _handle_redirect(self, request: RedirectedRequest) -> RedirectResponse:
		return RedirectResponse(request.url)

	def _handle_resource(self, request: ResourceRequest) -> FileResponse:
		return FileResponse(request.path)

	def _handle_page(self, request: RootRequest, t_page: Type[IPage]) -> DataResponse:
		return t_page(request).render()

	def _handle_search(self, request: SearchRequest) -> DataResponse:
		return self._handle_page(request, SearchPage)

	def _handle_article(self, request: PageRequest) -> DataResponse:
		return self._handle_page(request, FilePage)

	def _handle_section(self, request: SectionRequest) -> DataResponse:
		return self._handle_page(request, SectionPage)


handle_request_by_type = RequestTypeHandler()
