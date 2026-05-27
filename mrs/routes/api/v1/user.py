from mrs.framework.models.request import Request
from mrs.framework.models.response import Response
from mrs.framework.router import Router
from mrs.routes.api._helpers import auth_payload, json_body, require_fields
from mrs.services.auth import resolve_credentials, sign_up, update_account
from mrs.services.users import book_order, list_orders

@Router.endpoint("/api/v1/user/account")
async def user_account(request: Request) -> Response:
  response = Response()

  if request.method == "POST":
    try:
      data = json_body(request)
      require_fields(data, ["email", "password"])
      result = sign_up("user", data["email"], data["password"], data)
    except ValueError as error:
      return response.json(400, {"error": str(error)})
    except PermissionError as error:
      return response.json(401, {"error": str(error)})
    except LookupError as error:
      return response.json(404, {"error": str(error)})

    return response.json(201, {
      "token": result["token"],
      "profile": result["profile"],
    })

  if request.method in ("PATCH", "PUT"):
    try:
      data = json_body(request)
      identity = resolve_credentials(auth_payload(request, data), "user")
      result = update_account("user", identity["auth"], data)
    except ValueError as error:
      return response.json(400, {"error": str(error)})
    except PermissionError as error:
      return response.json(401, {"error": str(error)})
    except LookupError as error:
      return response.json(404, {"error": str(error)})

    return response.json(200, {
      "profile": result["profile"],
    })

  return response.json(405, {"error": "Method Not Allowed"})

@Router.endpoint("/api/v1/user/order")
async def user_order(request: Request) -> Response:
  response = Response()

  if request.method == "POST":
    try:
      data = json_body(request)
      require_fields(data, ["items"])
      identity = resolve_credentials(auth_payload(request, data), "user")
      order = book_order(identity["profile"]["id"], data["items"])
    except ValueError as error:
      return response.json(400, {"error": str(error)})
    except PermissionError as error:
      return response.json(401, {"error": str(error)})
    except LookupError as error:
      return response.json(404, {"error": str(error)})

    return response.json(201, {"order": order})

  if request.method == "GET":
    try:
      data = json_body(request)
      identity = resolve_credentials(auth_payload(request, data), "user")
      orders = list_orders(identity["profile"]["id"])
    except ValueError as error:
      return response.json(400, {"error": str(error)})
    except PermissionError as error:
      return response.json(401, {"error": str(error)})

    return response.json(200, {"orders": orders})

  return response.json(405, {"error": "Method Not Allowed"})

