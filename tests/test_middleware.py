from langex.core.testing import expects

from tests.common import CALLS
from tests.common import invoke
from tests.common import reset_state


def router_middleware_order():
  reset_state()
  response = invoke("/tests/middleware")

  return (
    response._status_code,
    tuple(CALLS),
  )

router_middleware_order @ expects(
  (200, ("pre", "handler:pre", "post"))
)
