from mrs.database.model import Query, Repository, Table

COMMON_COLUMNS = {
  "id": str,
  "created_at": str,
  "updated_at": str,
}

SCHEMA = {
  "auth": {
    **COMMON_COLUMNS,
    "persona": str,
    "profile_table": str,
    "profile_id": str,
    "email": str,
    "phone": str,
    "password": str,
    "token": str,
  },
  "agents": {
    **COMMON_COLUMNS,
    "name": str,
    "email": str,
    "phone": str,
    "age": int,
  },
  "partners": {
    **COMMON_COLUMNS,
    "name": str,
    "email": str,
    "phone": str,
    "lat": float,
    "long": float,
    "address_line_1": str,
    "address_line_2": str,
    "city": str,
    "state": str,
    "pincode": str,
    "country": str,
  },
  "users": {
    **COMMON_COLUMNS,
    "name": str,
    "email": str,
    "phone": str,
    "age": int,
    "home_lat": float,
    "home_long": float,
    "address_line_1": str,
    "address_line_2": str,
    "city": str,
    "state": str,
    "pincode": str,
    "country": str,
  },
  "medicines": {
    **COMMON_COLUMNS,
    "name": str,
    "description": str,
    "requires_prescription": bool,
  },
  "inventory": {
    **COMMON_COLUMNS,
    "partner_id": str,
    "medicine_id": str,
    "quantity": int,
    "price": float,
  },
  "orders": {
    **COMMON_COLUMNS,
    "user_id": str,
    "partner_id": str,
    "agent_id": str,
    "status": str,
    "items": list,
    "delivery_address": dict,
    "total": float,
  },
  "medicine_requests": {
    **COMMON_COLUMNS,
    "customer_id": str,
    "name": str,
    "notes": str,
    "status": str,
  },
}

def setup_database() -> Repository:
  repository = Repository()

  for name, cols in SCHEMA.items():
    if name not in repository.tables:
      repository.register(Table(name, cols))

  return repository

repository = setup_database()
__all__ = [
  "Query",
  "Repository",
  "SCHEMA",
  "Table",
  "repository",
  "setup_database",
]

