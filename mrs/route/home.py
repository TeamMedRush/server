from mrs.framework.models.request import Request
from mrs.framework.models.response import Response
from mrs.framework.router import Router

@Router.endpoint("/")
async def get_home(_: Request) -> Response:
  response = Response()
  response.status(200)
  response.content_type("text/plain")
  response.body(b"Hello, MedRush Server!")

  return response

