from langex.core.functions import autosig

from mrs.framework.models.request import Request

def analyse_headers(header_text: str) -> dict:
  lines = header_text.split("\r\n")
  headers = {}
  headers["other"] = []

  for line in lines:
    if ": " not in line:
      headers["other"].append(line)
      continue

    key, value = line.split(": ", 1)
    headers[key] = value

  return headers

@autosig
def analyse_request(addr: tuple, headers: dict, body: bytes) -> Request:
  method, path, version = headers["other"][0].split(" ")

  return Request(addr, method, path, version, headers, body)

