from langex.core.testing import expects

from mrs.services.medicines import create_medicine

from tests.common import invoke
from tests.common import reset_state
from tests.common import response_json
from tests.fixtures import agent_signup_payload
from tests.fixtures import inventory_items
from tests.fixtures import order_items
from tests.fixtures import partner_signup_payload
from tests.fixtures import user_signup_payload


def order_assignment_flow():
  reset_state()
  user_signup = invoke(
    "/api/v1/auth/signup",
    "POST",
    user_signup_payload(),
  )

  partner_signup = invoke(
    "/api/v1/auth/signup",
    "POST",
    partner_signup_payload(),
  )

  agent_signup = invoke(
    "/api/v1/auth/signup",
    "POST",
    agent_signup_payload(),
  )

  user_body = response_json(user_signup)
  partner_body = response_json(partner_signup)
  agent_body = response_json(agent_signup)
  medicine = create_medicine("Paracetamol")
  inventory = invoke(
    "/api/v1/partner/inventory",
    "PUT",
    inventory_items(medicine["id"], 4, 12.5),
    {"token": partner_body["token"]},
  )

  order = invoke(
    "/api/v1/user/order",
    "POST",
    order_items(medicine["id"], 2),
    {"token": user_body["token"]},
  )

  pending = invoke(
    "/api/v1/agent/orders/pending",
    "GET",
    None,
    {"token": agent_body["token"]},
  )

  order_body = response_json(order)
  pending_body = response_json(pending)
  accept = invoke(
    f"/api/v1/agent/orders/{order_body['order']['id']}/accept",
    "POST",
    {},
    {"token": agent_body["token"]},
  )

  accept_body = response_json(accept)

  return (
    user_signup._status_code,
    partner_signup._status_code,
    agent_signup._status_code,
    inventory._status_code,
    order._status_code,
    order_body["order"]["total"],
    len(pending_body["orders"]),
    accept._status_code,
    accept_body["order"]["status"],
    accept_body["order"]["agent_id"] == agent_body["profile"]["id"],
  )

order_assignment_flow @ expects(
  (201, 201, 201, 200, 201, 25.0, 1, 200, "accepted", True)
)
