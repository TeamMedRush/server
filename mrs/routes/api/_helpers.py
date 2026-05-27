from json import loads

from mrs.framework.models.request import Request

def json_body(request: Request) -> dict:
  body = request.body

  if body in (None, "", b""):
    return {}

  if isinstance(body, bytes):
    body = body.decode()

  if isinstance(body, str):
    return loads(body)

  if isinstance(body, dict):
    return body

  raise ValueError("Invalid JSON")

def require_fields(data: dict, fields: list[str]):
  for field in fields:
    if field not in data or data[field] in (None, ""):
      raise ValueError(f"Missing field: {field}")

def auth_payload(request: Request, data: dict | None = None) -> dict:
  payload = {
    "token": (
      request.meta.get("token")
      or request.meta.get("auth-token")
      or request.meta.get("user-token")
    ),
  }

  if data is None:
    data = {}

  payload["token"] = payload["token"] or data.get("token")
  payload["email"] = data.get("current_email", data.get("email"))
  payload["password"] = data.get(
    "current_password",
    data.get("password"),
  )

  return payload

