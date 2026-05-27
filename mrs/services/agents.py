from datetime import datetime, timezone

from mrs.database import Query, repository

def _now() -> str:
  return datetime.now(timezone.utc).isoformat()

def create_account(data: dict) -> dict:
  required = ["name", "email", "phone", "age"]

  for field in required:
    if field not in data:
      raise ValueError(f"Missing field: {field}")

  payload = {
    "name": data["name"],
    "email": data["email"],
    "phone": data["phone"],
    "age": int(data["age"]),
  }

  account_id = repository.access("agents").upsert(None, payload)

  return repository.access("agents").get(account_id)

def update_account(account_id: str, data: dict) -> dict:
  table = repository.access("agents")
  current = table.get(account_id)

  if current is None:
    raise LookupError("Agent account not found")

  allowed = {"name", "email", "phone", "age"}
  payload = {
    **current,
    **{
      key: value

      for key, value in data.items()
      if key in allowed and value is not None
    },
    "updated_at": _now(),
  }

  if "age" in payload:
    payload["age"] = int(payload["age"])

  table.upsert(account_id, payload)

  return table.get(account_id)

def pending_orders() -> list[dict]:
  return repository.access("orders").search({
    "status": Query("eq", "pending_assignment"),
  }, [])

def accept_order(agent_id: str, order_id: str) -> dict:
  agents_table = repository.access("agents")

  if agents_table.get(agent_id) is None:
    raise LookupError("Agent account not found")

  orders = repository.access("orders")
  order = orders.get(order_id)

  if order is None:
    raise LookupError("Order not found")

  if order["status"] != "pending_assignment":
    raise ValueError("Order is not pending assignment")

  orders.upsert(order_id, {
    "agent_id": agent_id,
    "status": "accepted",
  })

  return orders.get(order_id)

