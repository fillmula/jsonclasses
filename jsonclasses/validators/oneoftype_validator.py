"""module for oneoftype validator."""
from typing import List, Any
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator


class OneOfTypeValidator(Validator):
    """One of type validator validates value against a list of available types.
    """

    def __init__(self, type_list: List[Any]) -> None:
        self.type_list = type_list

    def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
        if value is None:
            return
        from ..fields import collection_argument_type_to_types
        for raw_type in self.type_list:
            types = collection_argument_type_to_types(raw_type)
            try:
                types.validator.validate(value=value,
                                         key_path=key_path,
                                         root=root,
                                         all_fields=all_fields,
                                         config=config)
                return
            except ValidationException:
                continue
        raise ValidationException(
            {key_path: f'Value \'{value}\' at \'{key_path}\' should be one of type {self.type_list}.'},
            root
        )
