from langex.core.classes import singleton
from langex.core.functions import autosig

from mrs.framework.models.request import Request
from mrs.framework.models.response import Response

class _PathMatchResult:
  def __init__(self):
    self.is_match = False
    self.params = {}

  def success(self):
    self.is_match = True

  def add_param(self, name: str, value: str):
    self.params[name] = value

@autosig
def _match_path(pattern: str, path: str) -> _PathMatchResult:
  pattern_parts = pattern.strip("/").split("/")
  path_parts = path.strip("/").split("/")
  result = _PathMatchResult()
  idx = 0

  while idx < len(pattern_parts) and idx < len(path_parts):
    pattern_part = pattern_parts[idx]
    path_part = path_parts[idx]
    idx += 1

    if pattern_part.startswith(":"):
      result.add_param(pattern_part[1:], path_part)
      continue

    if pattern_part.startswith("*"):
      result.add_param(pattern_part[1:], path_parts[idx - 1:])
      result.success()

      return result

    if pattern_part != path_part:
      return result

  if len(pattern_parts) == len(path_parts):
    result.success()

  return result

class _EndpointManager:
  def __init__(self):
    self.endpoints = []

  def add(
    self,
    path: str,
    handler,
    precalls,
    postcalls,
  ):
    self.endpoints.append((path, handler, precalls, postcalls))

    return handler

  def get(self, request: Request):
    for path, handler, precalls, postcalls in self.endpoints:
      if not _match_path(path, request.path).is_match:
        continue

      request.path_params = _match_path(path, request.path).params

      return handler, precalls, postcalls

    return None

@singleton
class Router:
  def __init__(self):
    self.epmgr = _EndpointManager()

  def endpoint(self, path: str, /, *, pre, post):
    def decorator(handler):
      return self.epmgr.add(path, handler, pre, post)

    return decorator

  async def process(self, request: Request) -> Response:
    matched = self.epmgr.get(request)

    if matched is None:
      response = Response()
      response.status(404)
      response.body(b"Not Found")
      response.content_type("text/plain")

      return response

    handler, precalls, postcalls = matched

    try:
      for middleware in precalls:
        request = middleware(request)

      response = await handler(request)
    except Exception as e:
      response = Response()
      response.status(500)
      response.body(f"Internal Server Error: \n{str(e)}".encode())
      response.content_type("text/plain")
    finally:
      for middleware in postcalls:
        request = middleware(request)

    return response
