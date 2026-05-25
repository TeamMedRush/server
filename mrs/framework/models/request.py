class Request:
  def __init__(
    self,
    addr: tuple,
    method: str,
    path: str,
    version: str,
    headers: dict,
    body: str
  ):
    self.addr = addr
    self.method = method
    self.path = path
    self.version = version
    self.headers = headers
    self.body = body
    self.path_params = {}
    self.meta = {}

