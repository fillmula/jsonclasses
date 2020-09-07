from typing import Any
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator
from ..utils.nonnull_note import NonnullNote

class NonnullValidator(Validator):

  def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    pass

  def transform(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config):
    return NonnullNote() if value is None else value
