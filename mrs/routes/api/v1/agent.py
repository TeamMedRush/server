from mrs.framework.models.request import Request
from mrs.framework.models.response import Response
from mrs.framework.router import Router
from mrs.middleware.auth import auth as auth_middleware
from mrs.routes.api._helpers import auth_payload, json_body
from mrs.routes.api._helpers import require_fields
from mrs.services.agents import accept_order
from mrs.services.agents import pending_orders
from mrs.services.auth import resolve_credentials
from mrs.services.auth import sign_up
from mrs.services.auth import update_account

@Router.endpoint(
  "/api/v1/agent/account",
  pre=[auth_middleware],
  post=[],
)
async def agent_account(request: Request) -> Response:
  response = Response()

  if request.method == "POST":
    try:
      data = json_body(request)
      require_fields(data, ["email", "password"])
      result = sign_up(
        "agent",
        data["email"],
        data["password"],
        data,
      )
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
      identity = resolve_credentials(
        auth_payload(request, data),
        "agent",
      )
      result = update_account("agent", identity["auth"], data)
    except ValueError as error:
      return response.json(400, {"error": str(error)})
    except PermissionError as error:
      return response.json(401, {"error": str(error)})
    except LookupError as error:
      return response.json(404, {"error": str(error)})

    return response.json(200, {"profile": result["profile"]})

  return response.json(405, {"error": "Method Not Allowed"})

@Router.endpoint(
  "/api/v1/agent/orders/pending",
  pre=[auth_middleware],
  post=[],
)
async def agent_pending_orders(request: Request) -> Response:
  response = Response()

  if request.method != "GET":
    return response.json(405, {"error": "Method Not Allowed"})

  try:
    data = json_body(request)
    resolve_credentials(
      auth_payload(request, data),
      "agent",
    )
    orders = pending_orders()
  except ValueError as error:
    return response.json(400, {"error": str(error)})
  except PermissionError as error:
    return response.json(401, {"error": str(error)})

  return response.json(200, {"orders": orders})

@Router.endpoint(
  "/api/v1/agent/orders/:order_id/accept",
  pre=[auth_middleware],
  post=[],
)
async def agent_accept_order(request: Request) -> Response:
  response = Response()

  if request.method != "POST":
    return response.json(405, {"error": "Method Not Allowed"})

  try:
    data = json_body(request)
    identity = resolve_credentials(
      auth_payload(request, data),
      "agent",
    )
    order = accept_order(
      identity["profile"]["id"],
      request.path_params["order_id"],
    )
  except ValueError as error:
    return response.json(400, {"error": str(error)})
  except PermissionError as error:
    return response.json(401, {"error": str(error)})
  except LookupError as error:
    return response.json(404, {"error": str(error)})

  return response.json(200, {"order": order})
