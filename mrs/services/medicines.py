from mrs.database import Query, repository

def create_medicine(
  name: str,
  description: str = "",
  requires_prescription: bool = False,
) -> dict:
  medicine_id = repository.access("medicines").upsert(None, {
    "name": name,
    "description": description,
    "requires_prescription": requires_prescription,
  })

  return repository.access("medicines").get(medicine_id)

def list_medicines(search: str | None = None) -> list[dict]:
  query = {}

  if search:
    query["name"] = Query("contains", search)

  return repository.access("medicines").search(query, [])

