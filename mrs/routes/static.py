from os.path import isfile

from mrs.framework.models.request import Request
from mrs.framework.models.response import Response
from mrs.framework.router import Router

@Router.endpoint("/static/*resource_path")
async def get_static_asset(request: Request) -> Response:
  response = Response()
  response.status(200)
  resource_path = request.path_params.get("resource_path", "")
  resource_path = "/".join(resource_path)
  resource_path = f"static/{resource_path}"

  if not isfile(resource_path):
    response.status(404)
    response.content_type("text/plain")
    response.body(b"File not found")

    return response

  with open(resource_path, "rb") as resource_file:
    if resource_path.endswith(".css"):
      response.content_type("text/css")
    elif resource_path.endswith(".js"):
      response.content_type("application/javascript")
    elif resource_path.endswith(".png"):
      response.content_type("image/png")
    elif resource_path.endswith(".jpg") or resource_path.endswith(".jpeg"):
      response.content_type("image/jpeg")
    else:
      response.content_type("application/octet-stream")

    response.body(resource_file.read())

  return response

@Router.endpoint("/favicon.ico")
async def get_favicon(request: Request) -> Response:
  response = Response()
  response.status(200)

  with open("static/icon.png", "rb") as icon_file:
    response.content_type("image/png")
    response.body(icon_file.read())

  return response

