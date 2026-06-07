from mrs.database import Query, repository

CATEGORIES = [
  "most_bought",
  "generic",
  "prescription_required",
  "otc",
  "ayurvedic",
  "personal_care",
  "vitamins_supplements",
  "baby_care",
  "first_aid",
  "chronic_care",
]

CATEGORY_LABELS = {
  "most_bought": "Most Bought",
  "generic": "Generic Medicines",
  "prescription_required": "Prescription Required",
  "otc": "Over The Counter",
  "ayurvedic": "Ayurvedic",
  "personal_care": "Personal Care",
  "vitamins_supplements": "Vitamins & Supplements",
  "baby_care": "Baby Care",
  "first_aid": "First Aid",
  "chronic_care": "Chronic Care",
}

def create_medicine(
  name: str,
  description: str = "",
  requires_prescription: bool = False,
  category: str = "otc",
  manufacturer: str = "",
  price: float = 0.0,
  discount_price: float = 0.0,
  image_url: str = "",
  dosage_form: str = "",
  pack_size: str = "",
  in_stock: bool = True,
) -> dict:
  medicine_id = repository.access("medicines").upsert(None, {
    "name": name,
    "description": description,
    "requires_prescription": requires_prescription,
    "category": category,
    "manufacturer": manufacturer,
    "price": price,
    "discount_price": discount_price,
    "image_url": image_url,
    "dosage_form": dosage_form,
    "pack_size": pack_size,
    "in_stock": in_stock,
  })

  return repository.access("medicines").get(medicine_id)

def get_medicine(medicine_id: str) -> dict | None:
  return repository.access("medicines").get(medicine_id)

def list_medicines(
  search: str | None = None,
  category: str | None = None,
) -> list[dict]:
  query = {}

  if search:
    query["name"] = Query("contains", search)

  if category:
    query["category"] = Query("eq", category)

  return repository.access("medicines").search(query, [])

def list_categories() -> list[dict]:
  return [
    {"key": key, "label": CATEGORY_LABELS[key]}
    for key in CATEGORIES
  ]


