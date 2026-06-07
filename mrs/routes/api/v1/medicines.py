from mrs.framework.models.request import Request
from mrs.framework.models.response import Response
from mrs.framework.router import Router
from mrs.routes.api._helpers import json_body
from mrs.services.medicines import (
  get_medicine,
  list_medicines,
  list_categories,
)

@Router.endpoint("/api/v1/medicines", pre=[], post=[])
async def medicines(request: Request) -> Response:
  response = Response()

  if request.method == "GET":
    try:
      data = json_body(request)
      medicines = list_medicines(
        search=data.get("search"),
        category=data.get("category"),
      )
    except ValueError as error:
      return response.json(400, {"error": str(error)})

    return response.json(200, {"medicines": medicines})

  return response.json(405, {"error": "Method Not Allowed"})

@Router.endpoint("/api/v1/medicines/categories", pre=[], post=[])
async def medicines_categories(request: Request) -> Response:
  response = Response()

  if request.method == "GET":
    categories = list_categories()
    return response.json(200, {"categories": categories})

  return response.json(405, {"error": "Method Not Allowed"})

@Router.endpoint("/api/v1/medicines/:id", pre=[], post=[])
async def medicine_detail(request: Request) -> Response:
  response = Response()

  if request.method == "GET":
    medicine_id = request.path_params.get("id")
    medicine = get_medicine(medicine_id)

    if medicine is None:
      return response.json(404, {"error": "Medicine not found"})

    return response.json(200, {"medicine": medicine})

  return response.json(405, {"error": "Method Not Allowed"})


