from mrs.framework.models.request import Request
from mrs.framework.models.response import Response
from mrs.framework.router import Router
from mrs.routes.api._helpers import json_body, require_fields
from mrs.services.auth import sign_in, sign_up

@Router.endpoint("/api/v1/auth/signup")
async def auth_signup(request: Request) -> Response:
  response = Response()

  if request.method != "POST":
    return response.json(405, {"error": "Method Not Allowed"})

  try:
    data = json_body(request)
    require_fields(data, ["persona", "email", "password"])
    result = sign_up(data["persona"], data["email"], data["password"], data)
  except ValueError as error:
    return response.json(400, {"error": str(error)})
  except PermissionError as error:
    return response.json(401, {"error": str(error)})
  except LookupError as error:
    return response.json(404, {"error": str(error)})

  return response.json(201, {
    "token": result["token"],
    "persona": result["auth"]["persona"],
    "profile": result["profile"],
  })

@Router.endpoint("/api/v1/auth/signin")
async def auth_signin(request: Request) -> Response:
  response = Response()

  if request.method != "POST":
    return response.json(405, {"error": "Method Not Allowed"})

  try:
    data = json_body(request)
    require_fields(data, ["persona", "email", "password"])
    result = sign_in(data["persona"], data["email"], data["password"])
  except ValueError as error:
    return response.json(400, {"error": str(error)})
  except PermissionError as error:
    return response.json(401, {"error": str(error)})
  except LookupError as error:
    return response.json(404, {"error": str(error)})

  return response.json(200, {
    "token": result["token"],
    "persona": result["auth"]["persona"],
    "profile": result["profile"],
  })

