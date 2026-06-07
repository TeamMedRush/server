from mrs.framework.analyser import analyse_headers, analyse_request
from mrs.framework.models.request import Request
from mrs.framework.router import Router

from asyncio import (
  StreamReader,
  StreamWriter,
  start_server,
  Lock, run,
)

connections = 0
counter_lock = Lock()
INTERNAL_SERVER_ERROR_RESPONSE = b"""\r
HTTP/1.1 500 Internal Server Error\r
Content-Type: text/plain\r
Content-Length: 21\r
Connection: close\r

Internal Server Error
"""

async def _create_request(addr: tuple, reader: StreamReader) -> bytes:
  headers = await reader.readuntil(b"\r\n\r\n")
  headers = analyse_headers(headers.decode())
  body = b""

  if "Content-Length" in headers:
    content_length = int(headers["Content-Length"])
    body = await reader.readexactly(content_length)

  return analyse_request(addr, headers, body)

async def _on_request(request: Request) -> bytes:
  try:
    response = await Router.process(request)
  except Exception as e:
    print("error processing request:", e.with_traceback(None))

    return INTERNAL_SERVER_ERROR_RESPONSE

  return response.generate()

async def _write_response(writer: StreamWriter, response: bytes):
  writer.write(response)
  await writer.drain()
  writer.close()
  await writer.wait_closed()

async def _handle(reader, writer):
  global connections

  async with counter_lock:
    connections += 1

  try:
    addr = writer.get_extra_info("peername")
    request = await _create_request(addr, reader)
    response = await _on_request(request)
    await _write_response(writer, response)
  finally:
    async with counter_lock:
      connections -= 1

async def _start_server():
  host = "0.0.0.0"
  port = 8000
  import sys
  server = await start_server(
    _handle, host, port, reuse_port=(sys.platform != "win32")
  )

  print(f"Active: http://{host}:{port}")

  async with server:
    await server.serve_forever()

def serve():
  run(_start_server())

