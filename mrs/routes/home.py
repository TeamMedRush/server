from mrs.framework.models.request import Request
from mrs.framework.models.response import Response
from mrs.framework.router import Router

@Router.endpoint("/")
async def get_home(_: Request) -> Response:
  response = Response()
  response.text(200, "Hello, MedRush Server!")

  return response

