from mrs.framework.models.request import Request
from mrs.framework.models.response import Response
from mrs.framework.router import Router
from mrs.routes.api._helpers import json_body
from mrs.services.medicines import list_medicines

@Router.endpoint("/api/v1/medicines", pre=[], post=[])
async def medicines(request: Request) -> Response:
  response = Response()

  if request.method == "GET":
    try:
      data = json_body(request)
      medicines = list_medicines(data.get("search"))
    except ValueError as error:
      return response.json(400, {"error": str(error)})

    return response.json(200, {"medicines": medicines})

  return response.json(405, {"error": "Method Not Allowed"})

