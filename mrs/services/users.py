from datetime import datetime, timezone

from mrs.database import Query, repository

def _now() -> str:
  return datetime.now(timezone.utc).isoformat()

def _normalize_country(country: str) -> str:
  if country != "India":
    raise ValueError("Country must be India")

  return country

def create_account(data: dict) -> dict:
  required = [
    "name",
    "email",
    "phone",
    "age",
    "home_lat",
    "home_long",
    "address_line_1",
    "city",
    "state",
    "pincode",
    "country",
  ]

  for field in required:
    if field not in data:
      raise ValueError(f"Missing field: {field}")

  payload = {
    "name": data["name"],
    "email": data["email"],
    "phone": data["phone"],
    "age": int(data["age"]),
    "home_lat": float(data["home_lat"]),
    "home_long": float(data["home_long"]),
    "address_line_1": data["address_line_1"],
    "address_line_2": data.get("address_line_2", ""),
    "city": data["city"],
    "state": data["state"],
    "pincode": str(data["pincode"]),
    "country": _normalize_country(data["country"]),
  }

  account_id = repository.access("users").upsert(None, payload)

  return repository.access("users").get(account_id)

def update_account(account_id: str, data: dict) -> dict:
  table = repository.access("users")
  current = table.get(account_id)

  if current is None:
    raise LookupError("User account not found")

  allowed = {
    "name",
    "email",
    "phone",
    "age",
    "home_lat",
    "home_long",
    "address_line_1",
    "address_line_2",
    "city",
    "state",
    "pincode",
    "country",
  }

  payload = {
    **current,
    **{key: value for key, value in data.items() if key in allowed and value is not None},
    "updated_at": _now(),
  }

  if "age" in payload:
    payload["age"] = int(payload["age"])

  if "home_lat" in payload:
    payload["home_lat"] = float(payload["home_lat"])

  if "home_long" in payload:
    payload["home_long"] = float(payload["home_long"])

  if "country" in payload:
    payload["country"] = _normalize_country(payload["country"])

  if "pincode" in payload:
    payload["pincode"] = str(payload["pincode"])

  if "address_line_2" not in payload:
    payload["address_line_2"] = ""

  table.upsert(account_id, payload)

  return table.get(account_id)

def book_order(user_id: str, items: list[dict]) -> dict:
  user = repository.access("users").get(user_id)

  if user is None:
    raise LookupError("User account not found")

  medicine_table = repository.access("medicines")
  inventory_table = repository.access("inventory")
  total = 0.0
  normalized_items = []

  for item in items:
    medicine_id = item.get("medicine_id")
    quantity = int(item.get("quantity", 1))

    if not medicine_id:
      raise ValueError("Missing field: medicine_id")

    if quantity <= 0:
      raise ValueError("Quantity must be greater than zero")

    medicine = medicine_table.get(medicine_id)

    if medicine is None:
      raise LookupError(f"Medicine not found: {medicine_id}")

    inventory_matches = inventory_table.search({
      "medicine_id": Query("eq", medicine_id),
    }, [])

    if not inventory_matches:
      raise LookupError(f"Inventory not found for medicine: {medicine_id}")

    inventory_row = inventory_matches[0]
    price = float(inventory_row.get("price", 0.0) or 0.0)
    available = int(inventory_row.get("quantity", 0) or 0)

    if available < quantity:
      raise LookupError(f"Insufficient inventory for medicine: {medicine_id}")

    total += price * quantity
    normalized_items.append({
      "medicine_id": medicine_id,
      "name": medicine["name"],
      "quantity": quantity,
      "price": price,
    })

  order_id = repository.access("orders").upsert(None, {
    "user_id": user_id,
    "status": "pending_assignment",
    "items": normalized_items,
    "delivery_address": {
      "home_lat": user["home_lat"],
      "home_long": user["home_long"],
      "address_line_1": user["address_line_1"],
      "address_line_2": user.get("address_line_2", ""),
      "city": user["city"],
      "state": user["state"],
      "pincode": user["pincode"],
      "country": user["country"],
    },
    "total": float(total),
  })

  return repository.access("orders").get(order_id)

def list_orders(user_id: str) -> list[dict]:
  return repository.access("orders").search({
    "user_id": Query("eq", user_id),
  }, [])

