from copy import deepcopy

from datetime import datetime, timezone

from uuid import uuid4

from langex.core.classes import langex_class, singleton
from langex.core.functions import autosig

class Query:
  def __init__(self, operator: str, value: object):
    self.operator = operator
    self.value = value

  def matches(self, value: object) -> bool:
    if self.operator in ("=", "==", "eq"):
      return value == self.value

    if self.operator in ("!=", "ne"):
      return value != self.value

    if self.operator in (">", "gt"):
      return value > self.value

    if self.operator in (">=", "gte"):
      return value >= self.value

    if self.operator in ("<", "lt"):
      return value < self.value

    if self.operator in ("<=", "lte"):
      return value <= self.value

    if self.operator == "in":
      return value in self.value

    if self.operator == "contains":
      try:
        return self.value in value
      except Exception as _:
        return False

    if self.operator == "exists":
      return (value is not None) == bool(self.value)

    raise ValueError(f"Unsupported query operator: {self.operator}")

@langex_class
class Table:
  def __init__(self, name: str, cols: dict[str, type] | None = None):
    self.name = name
    self.cols: dict[str, type] = cols or {}
    self.rows: dict[str, dict] = {}

  def _now(self) -> str:
    return datetime.now(timezone.utc).isoformat()

  def _validate_cols(self, data: dict):
    unknown_cols = set(data) - set(self.cols)

    if unknown_cols:
      raise KeyError(f"Unknown column(s) for {self.name}: {', '.join(sorted(unknown_cols))}")

    for col, value in data.items():
      expected_type = self.cols[col]

      if value is not None and not isinstance(value, expected_type):
        raise TypeError(f"{self.name}.{col} must be {expected_type.__name__}")

  def _match(self, row: dict, query: dict[str, Query]) -> bool:
    for col, condition in query.items():
      if col not in self.cols:
        raise KeyError(f"Unknown column for {self.name}: {col}")

      if not condition.matches(row.get(col)):
        return False

    return True

  @autosig
  def get(self, id: str) -> dict | None:
    row = self.rows.get(id)

    if row is None:
      return None

    return deepcopy(row)

  @autosig
  def search(
    self,
    query: dict[str, Query],
    fields: list[str]
  ) -> list[dict]:
    for field in fields:
      if field not in self.cols:
        raise KeyError(f"Unknown field for {self.name}: {field}")

    results = []

    for row in self.rows.values():
      if not self._match(row, query):
        continue

      if not fields:
        results.append(deepcopy(row))
        continue

      results.append({field: deepcopy(row.get(field)) for field in fields})

    return results

  @autosig
  def upsert(self, id: str | None, data: dict) -> str | None:
    if id is None:
      id = uuid4().hex

    current = self.rows.get(id, {})
    row = {
      **current,
      **deepcopy(data),
      "id": id,
      "updated_at": self._now(),
    }

    if "created_at" in self.cols and "created_at" not in row:
      row["created_at"] = row["updated_at"]

    self._validate_cols(row)
    self.rows[id] = row

    return id

  @autosig
  def remove(self, id: str) -> bool:
    if id not in self.rows:
      return False

    del self.rows[id]

    return True

@singleton
class Repository:
  def __init__(self):
    self.tables: dict[str, Table] = {}

  def register(self, table: Table):
    self.tables[table.name] = table

    return table

  def access(self, table: str) -> Table:
    if table not in self.tables:
      raise KeyError(f"No table: {table}")

    return self.tables[table]

