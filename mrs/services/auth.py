from uuid import uuid4

from mrs.database import Query, repository
from mrs.services import agents, partners, users

PERSONA_TABLES = {
  "user": "users",
  "customer": "users",
  "agent": "agents",
  "partner": "partners",
}

def normalize_persona(persona: str) -> str:
  persona = (persona or "").strip().lower()

  if persona not in PERSONA_TABLES:
    raise ValueError("Invalid persona")

  return "user" if persona == "customer" else persona

def _profile_table(persona: str) -> str:
  return PERSONA_TABLES[normalize_persona(persona)]

def _auth_table():
  return repository.access("auth")

def _profile_service(persona: str):
  persona = normalize_persona(persona)

  if persona == "user":
    return users

  if persona == "agent":
    return agents

  return partners

def _token() -> str:
  return uuid4().hex

def _find_auth(persona: str, email: str):
  matches = _auth_table().search({
    "persona": Query("eq", normalize_persona(persona)),
    "email": Query("eq", email),
  }, [])

  if not matches:
    return None

  return matches[0]

def _find_auth_by_email(email: str):
  matches = _auth_table().search({
    "email": Query("eq", email),
  }, [])

  if not matches:
    return None

  return matches[0]

def _find_auth_by_token(token: str):
  matches = _auth_table().search({
    "token": Query("eq", token),
  }, [])

  if not matches:
    return None

  return matches[0]

def _profile(persona: str, profile_id: str):
  table = _profile_table(persona)

  return repository.access(table).get(profile_id)

def sign_up(persona: str, email: str, password: str, data: dict) -> dict:
  persona = normalize_persona(persona)

  if _find_auth_by_email(email) is not None:
    raise ValueError("Account already exists")

  profile_service = _profile_service(persona)
  profile = profile_service.create_account(data)
  token = _token()
  auth_id = _auth_table().upsert(None, {
    "persona": persona,
    "profile_table": _profile_table(persona),
    "profile_id": profile["id"],
    "email": email,
    "phone": profile["phone"],
    "password": password,
    "token": token,
  })

  auth = _auth_table().get(auth_id)

  return {
    "auth": auth,
    "profile": profile,
    "token": token,
  }

def sign_in(persona: str, email: str, password: str) -> dict:
  persona = normalize_persona(persona)
  auth = _find_auth(persona, email)

  if auth is None or auth["password"] != password:
    raise PermissionError("Invalid credentials")

  token = _token()
  _auth_table().upsert(auth["id"], {
    "token": token,
    "password": password,
  })

  auth = _auth_table().get(auth["id"])
  profile = _profile(persona, auth["profile_id"])

  return {
    "auth": auth,
    "profile": profile,
    "token": token,
  }

def authenticate(persona: str, email: str, password: str) -> dict:
  persona = normalize_persona(persona)
  auth = _find_auth(persona, email)

  if auth is None or auth["password"] != password:
    raise PermissionError("Invalid credentials")

  profile = _profile(persona, auth["profile_id"])

  return {
    "auth": auth,
    "profile": profile,
  }

def authenticate_token(token: str, persona: str | None = None) -> dict:
  auth = _find_auth_by_token(token)

  if auth is None:
    raise PermissionError("Invalid credentials")

  if persona is not None and normalize_persona(persona) != auth["persona"]:
    raise PermissionError("Invalid credentials")

  profile = _profile(auth["persona"], auth["profile_id"])

  return {
    "auth": auth,
    "profile": profile,
  }

def resolve_credentials(payload: dict, persona: str | None = None) -> dict:
  token = payload.get("token")

  if token:
    return authenticate_token(token, persona)

  if persona is None:
    raise PermissionError("Invalid credentials")

  email = payload.get("email")
  password = payload.get("password")

  if not email or not password:
    raise PermissionError("Invalid credentials")

  return authenticate(persona, email, password)

def update_account(persona: str, auth: dict, data: dict) -> dict:
  persona = normalize_persona(persona)
  profile_service = _profile_service(persona)

  if "email" in data and data["email"]:
    existing = _find_auth_by_email(data["email"])

    if existing is not None and existing["id"] != auth["id"]:
      raise ValueError("Account already exists")

  profile = profile_service.update_account(auth["profile_id"], data)
  auth_updates = {}

  if "email" in profile:
    auth_updates["email"] = profile["email"]

  if "phone" in profile:
    auth_updates["phone"] = profile["phone"]

  if "password" in data and data["password"]:
    auth_updates["password"] = data["password"]

  if auth_updates:
    _auth_table().upsert(auth["id"], auth_updates)

  auth = _auth_table().get(auth["id"])

  return {
    "auth": auth,
    "profile": profile,
  }

def profile_for_token(token: str, persona: str | None = None) -> dict:
  identity = authenticate_token(token, persona)

  return identity["profile"]

