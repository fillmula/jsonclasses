from typing import Any

class Field():
  def __init__(
    self,
    field_name: str = None,
    json_field_name: str = None,
    db_field_name: str = None,
    field_types: 'Types' = None,
    assigned_default_value: Any = None
  ):
    self.field_name = field_name
    self.json_field_name = json_field_name
    self.db_field_name = db_field_name
    self.field_types = field_types
    self.assigned_default_value = assigned_default_value
