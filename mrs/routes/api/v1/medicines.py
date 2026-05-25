from json import loads

from mrs.framework.models.request import Request
from mrs.framework.models.response import Response
from mrs.framework.router import Router

@Router.endpoint("/api/v1/medicines/request")
async def request_medicine(request: Request) -> Response:
  response = Response()

  if request.method != "POST":
    return response.json(405, {
      "error": "Method Not Allowed"
    })

  try:
    data = loads(request.body())
  except Exception as _:
    return response.json(400, {
      "error": "Invalid JSON"
    })

  return response

