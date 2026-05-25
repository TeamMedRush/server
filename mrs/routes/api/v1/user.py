from mrs.framework.models.request import Request
from mrs.framework.models.response import Response
from mrs.framework.router import Router

@Router.endpoint("/api/v1/user/order")
async def create_order(request: Request) -> Response:
  response = Response()

  if "user-token" not in request.meta:
    return response.json(401, {
      "error": "Authentication required",
    })

  if request.method != "POST":
    return response.json(405, {"error": "Method Not Allowed"})

  return response

