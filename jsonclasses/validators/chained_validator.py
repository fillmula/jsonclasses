"""module for chained validator."""
from __future__ import annotations
from typing import List, Dict, Any, Optional
from ..exceptions import ValidationException
from .validator import Validator
from ..utils.eager_validator_index_after_index import eager_validator_index_after_index
from ..utils.last_eager_validator_index import last_eager_validator_index
from ..contexts import ValidatingContext, TransformingContext, ToJSONContext


class ChainedValidator(Validator):
    """Chained validator has a series of validators chained."""

    def __init__(self, validators: Optional[List[Validator]] = None) -> None:
        self.validators = validators or []

    def append(self, *args: Validator) -> ChainedValidator:
        """Append validators to this chained validator chain."""
        return ChainedValidator([*self.validators, *args])

    def validate(self, context: ValidatingContext) -> None:
        keypath_messages: Dict[str, str] = {}
        start_validator_index = last_eager_validator_index(self.validators)
        for validator in self.validators[start_validator_index:]:
            try:
                validator.validate(context)
            except ValidationException as exception:
                keypath_messages.update(exception.keypath_messages)
                if not context.all_fields:
                    break
        if len(keypath_messages) > 0:
            raise ValidationException(keypath_messages, context.root)

    def _validate_and_transform(self,
                                validator: Validator,
                                context: TransformingContext) -> Any:
        """Validate as transform."""
        validator.validate(context.validating_context())
        return validator.transform(context)

    # flake8: noqa: E501
    def transform(self, context: TransformingContext) -> Any:
        curvalue = context.value
        index = 0
        next_index = eager_validator_index_after_index(self.validators, index)
        while next_index is not None:
            validators = self.validators[index:next_index]
            for validator in validators:
                curvalue = self._validate_and_transform(
                    validator,
                    context.new(value=curvalue))
            index = next_index + 1
            next_index = eager_validator_index_after_index(self.validators, index)
        validators = self.validators[index:]
        for validator in validators:
            curvalue = validator.transform(context.new(value=curvalue))
        return curvalue

    def tojson(self, context: ToJSONContext) -> Any:
        value = context.value
        for validator in self.validators:
            value = validator.tojson(context.new(value=value))
        return value
