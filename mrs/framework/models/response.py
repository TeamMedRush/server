from json import dumps

from langex.core.classes import langex_class
from langex.core.functions import autosig

@langex_class
class Response:
  def __init__(self):
    self._body = ""
    self._status_code = 200
    self._content_type = "text/plain"

  @autosig
  def body(self, body: bytes):
    self._body = body

    return self

  @autosig
  def status(self, code: int):
    self._status_code = code

    return self

  @autosig
  def content_type(self, content_type: str):
    self._content_type = content_type

    return self

  @autosig
  def generate(self):
    reasons = {
      200: "OK",
      201: "Created",
      400: "Bad Request",
      401: "Unauthorized",
      404: "Not Found",
      405: "Method Not Allowed",
      409: "Conflict",
      500: "Internal Server Error",
    }

    status = (
      "HTTP/1.1 "
      + str(self._status_code)
      + " "
      + reasons.get(self._status_code, "OK")
      + "\r\n"
    )

    content_type = "Content-Type: " + self._content_type + "\r\n"
    content_length = (
      "Content-Length: "
      + str(len(self._body))
      + "\r\n"
    )

    connection = "Connection: close\r\n"
    body = b"\r\n" + self._body

    return b"".join([
      status.encode(),
      content_type.encode(),
      content_length.encode(),
      connection.encode(),
      body
    ])

  @autosig
  def text(self, status_code: int, text: str):
    self.status(status_code)
    self.body(text.encode())
    self.content_type("text/plain")

    return self

  @autosig
  def json(self, status_code: int, data: dict):
    self.status(status_code)
    self.body(dumps(data).encode())
    self.content_type("application/json")

    return self

