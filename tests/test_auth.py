from langex.core.testing import expects

from tests.common import invoke
from tests.common import reset_state
from tests.common import response_json
from tests.fixtures import signin_payload
from tests.fixtures import user_signup_payload


def auth_routes_round_trip():
  reset_state()
  signup = invoke(
    "/api/v1/auth/signup",
    "POST",
    user_signup_payload(),
  )

  signin = invoke(
    "/api/v1/auth/signin",
    "POST",
    signin_payload("user", "alice@example.com", "pw"),
  )

  signup_body = response_json(signup)
  signin_body = response_json(signin)

  return (
    signup._status_code,
    signup_body["persona"],
    bool(signup_body["token"]),
    signin._status_code,
    signin_body["profile"]["name"],
  )

auth_routes_round_trip @ expects((201, "user", True, 200, "Alice"))
