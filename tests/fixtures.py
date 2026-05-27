def user_signup_payload(
  email: str = "alice@example.com",
  password: str = "pw",
) -> dict:
  return {
    "persona": "user",
    "name": "Alice",
    "email": email,
    "password": password,
    "phone": "999",
    "age": 31,
    "home_lat": 12.5,
    "home_long": 77.5,
    "address_line_1": "Line 1",
    "city": "Bengaluru",
    "state": "Karnataka",
    "pincode": "560001",
    "country": "India",
  }


def partner_signup_payload(
  email: str = "partner@example.com",
  password: str = "pw",
) -> dict:
  return {
    "persona": "partner",
    "name": "Partner",
    "email": email,
    "password": password,
    "phone": "888",
    "lat": 12.9,
    "long": 77.6,
    "address_line_1": "Warehouse",
    "city": "Bengaluru",
    "state": "Karnataka",
    "pincode": "560002",
    "country": "India",
  }


def agent_signup_payload(
  email: str = "agent@example.com",
  password: str = "pw",
) -> dict:
  return {
    "persona": "agent",
    "name": "Agent",
    "email": email,
    "password": password,
    "phone": "777",
    "age": 25,
  }


def signin_payload(persona: str, email: str, password: str) -> dict:
  return {
    "persona": persona,
    "email": email,
    "password": password,
  }


def inventory_items(
  medicine_id: str,
  quantity: int,
  price: float,
) -> dict:
  return {
    "items": [
      {
        "medicine_id": medicine_id,
        "quantity": quantity,
        "price": price,
      }
    ]
  }


def order_items(medicine_id: str, quantity: int) -> dict:
  return {
    "items": [
      {
        "medicine_id": medicine_id,
        "quantity": quantity,
      }
    ]
  }
