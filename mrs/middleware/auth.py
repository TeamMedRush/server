from mrs.framework.models.request import Request

def auth(request: Request) -> Request:
  token = (
    request.headers.get("user-token")
    or request.headers.get("token")
    or request.headers.get("Authorization")
    or request.headers.get("authorization")
  )

  if token:
    request.meta["token"] = token
    request.meta["user-token"] = token

  return request

