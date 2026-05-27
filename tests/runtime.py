import asyncio
import json

from mrs.database import repository
from mrs.framework.models.request import Request
from mrs.framework.models.response import Response
from mrs.framework.router import Router
from mrs.routes import load_routes

load_routes()

CALLS = []


def reset_state():
  for table in repository.tables.values():
    table.rows.clear()

  CALLS.clear()


def invoke(
  path: str,
  method: str = "GET",
  payload=None,
  headers=None,
):
  body = b""

  if payload is not None:
    body = json.dumps(payload).encode()

  request = Request(
    ("127.0.0.1", 1),
    method,
    path,
    "HTTP/1.1",
    headers or {},
    body,
  )

  return asyncio.run(Router.process(request))


def response_json(response: Response):
  return json.loads(response._body.decode())


def track_pre(request: Request) -> Request:
  CALLS.append("pre")
  request.meta["phase"] = "pre"

  return request


def track_post(request: Request) -> Request:
  CALLS.append("post")
  request.meta["phase"] = "post"

  return request


@Router.endpoint(
  "/tests/middleware",
  pre=[track_pre],
  post=[track_post],
)
async def middleware_probe(request: Request) -> Response:
  CALLS.append(f"handler:{request.meta['phase']}")

  return Response().text(200, "ok")
