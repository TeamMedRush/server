from mrs.framework.models.request import Request
from mrs.framework.models.response import Response
from mrs.framework.router import Router

@Router.endpoint("/api/v1/agent/delivery/open")
async def open_delivery(request: Request) -> Response:
  response = Response()

  if "user-token" not in request.meta:
    return response.json(401, {
      "error": "Authentication required",
    })

  return response

@Router.endpoint("/api/v1/agent/delivery/:delivery_id/accept")
async def accept_delivery(request: Request) -> Response:
  response = Response()

  if "user-token" not in request.meta:
    return response.json(401, {
      "error": "Authentication required",
    })

  return response

