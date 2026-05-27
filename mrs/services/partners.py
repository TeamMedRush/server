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
    "lat",
    "long",
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
    "lat": float(data["lat"]),
    "long": float(data["long"]),
    "address_line_1": data["address_line_1"],
    "address_line_2": data.get("address_line_2", ""),
    "city": data["city"],
    "state": data["state"],
    "pincode": str(data["pincode"]),
    "country": _normalize_country(data["country"]),
  }

  account_id = repository.access("partners").upsert(None, payload)

  return repository.access("partners").get(account_id)

def update_account(account_id: str, data: dict) -> dict:
  table = repository.access("partners")
  current = table.get(account_id)

  if current is None:
    raise LookupError("Partner account not found")

  allowed = {
    "name",
    "email",
    "phone",
    "lat",
    "long",
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

  if "lat" in payload:
    payload["lat"] = float(payload["lat"])

  if "long" in payload:
    payload["long"] = float(payload["long"])

  if "country" in payload:
    payload["country"] = _normalize_country(payload["country"])

  if "pincode" in payload:
    payload["pincode"] = str(payload["pincode"])

  if "address_line_2" not in payload:
    payload["address_line_2"] = ""

  table.upsert(account_id, payload)

  return table.get(account_id)

def get_inventory(partner_id: str) -> list[dict]:
  return repository.access("inventory").search({
    "partner_id": Query("eq", partner_id),
  }, [])

def set_inventory_items(partner_id: str, items: list[dict]) -> list[dict]:
  table = repository.access("inventory")
  updated = []

  for item in items:
    medicine_id = item.get("medicine_id")
    quantity = item.get("quantity")

    if not medicine_id:
      raise ValueError("Missing field: medicine_id")

    if quantity is None:
      raise ValueError("Missing field: quantity")

    matches = table.search({
      "partner_id": Query("eq", partner_id),
      "medicine_id": Query("eq", medicine_id),
    }, ["id"])

    inventory_id = matches[0]["id"] if matches else None
    payload = {
      "partner_id": partner_id,
      "medicine_id": medicine_id,
      "quantity": int(quantity),
      "price": float(item["price"]) if item.get("price") is not None else 0.0,
    }

    if inventory_id is not None:
      current = table.get(inventory_id) or {}

      if "price" not in item and current.get("price") is not None:
        payload["price"] = float(current["price"])

    inventory_id = table.upsert(inventory_id, payload)
    updated.append(table.get(inventory_id))

  return updated

