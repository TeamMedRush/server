from mrs.framework.models.request import Request
from mrs.framework.models.response import Response
from mrs.framework.router import Router
from mrs.routes.api._helpers import auth_payload, json_body
from mrs.routes.api._helpers import require_fields
from mrs.services.auth import resolve_credentials
from mrs.services.auth import sign_up
from mrs.services.auth import update_account
from mrs.services.partners import get_inventory
from mrs.services.partners import set_inventory_items

from mrs.middleware.auth import auth as auth_middleware

@Router.endpoint(
  "/api/v1/partner/account",
  pre=[auth_middleware],
  post=[],
)

async def partner_account(request: Request) -> Response:
  response = Response()

  if request.method == "POST":
    try:
      data = json_body(request)
      require_fields(data, ["email", "password"])
      result = sign_up(
        "partner",
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
        "partner",
      )

      result = update_account("partner", identity["auth"], data)
    except ValueError as error:
      return response.json(400, {"error": str(error)})
    except PermissionError as error:
      return response.json(401, {"error": str(error)})
    except LookupError as error:
      return response.json(404, {"error": str(error)})

    return response.json(200, {"profile": result["profile"]})

  return response.json(405, {"error": "Method Not Allowed"})

@Router.endpoint(
  "/api/v1/partner/inventory",
  pre=[auth_middleware],
  post=[],
)

async def partner_inventory(request: Request) -> Response:
  response = Response()

  try:
    data = json_body(request)
    identity = resolve_credentials(
      auth_payload(request, data),
      "partner",
    )

  except ValueError as error:
    return response.json(400, {"error": str(error)})
  except PermissionError as error:
    return response.json(401, {"error": str(error)})

  if request.method == "GET":
    inventory = get_inventory(identity["profile"]["id"])

    return response.json(200, {"inventory": inventory})

  if request.method == "PUT":
    try:
      items = data.get("items")

      if not isinstance(items, list):
        raise ValueError("Missing field: items")

      inventory = set_inventory_items(
        identity["profile"]["id"],
        items,
      )

    except ValueError as error:
      return response.json(400, {"error": str(error)})
    except LookupError as error:
      return response.json(404, {"error": str(error)})

    return response.json(200, {"inventory": inventory})

  return response.json(405, {"error": "Method Not Allowed"})

