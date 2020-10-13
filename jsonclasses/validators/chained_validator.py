"""module for chained validator."""
from __future__ import annotations
from typing import Any, Optional
from ..exceptions import ValidationException
from .validator import Validator
from .eager_validator import EagerValidator
from ..contexts import ValidatingContext, TransformingContext, ToJSONContext


class ChainedValidator(Validator):
    """Chained validator has a series of validators chained."""

    def __init__(self, validators: Optional[list[Validator]] = None) -> None:
        self.validators = validators or []

    def append(self, *args: Validator) -> ChainedValidator:
        """Append validators to this chained validator chain."""
        return ChainedValidator([*self.validators, *args])

    def _eager_validator_index_after_index(self,
                                           vs: list[Validator],
                                           index: int) -> Optional[int]:
        """This function returns the first eager validator index after given
        index.

        Args:
        vs (list[Validator]): A list of validators usually from chained
        validator.
        index (int): The starting index to begin search with.

        Returns:
        Optional[int]: The found index or None.
        """
        try:
            return vs.index(next(v for v in vs[index:]
                        if isinstance(v, EagerValidator)))
        except StopIteration:
            return None

    def _last_eager_validator_index(self,
                                    vs: list[Validator]) -> Optional[int]:
        """This function returns the last eager validator index.

        Args:
        vs (list[Validator]): A list of validators usually from chained
        validator.

        Returns:
        Optional[int]: The found index or None.
        """
        try:
            return max([i for (i, v) in enumerate(vs)
                    if isinstance(v, EagerValidator)])
        except ValueError:
            return None

    def validate(self, context: ValidatingContext) -> None:
        keypath_messages: dict[str, str] = {}
        start_validator_index = self._last_eager_validator_index(
                self.validators)
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
        next_index = self._eager_validator_index_after_index(
                self.validators, index)
        while next_index is not None:
            validators = self.validators[index:next_index]
            for validator in validators:
                curvalue = self._validate_and_transform(
                    validator,
                    context.new(value=curvalue))
            index = next_index + 1
            next_index = self._eager_validator_index_after_index(
                    self.validators, index)
        validators = self.validators[index:]
        for validator in validators:
            curvalue = validator.transform(context.new(value=curvalue))
        return curvalue

    def tojson(self, context: ToJSONContext) -> Any:
        value = context.value
        for validator in self.validators:
            value = validator.tojson(context.new(value=value))
        return value

    def serialize(self, context: TransformingContext) -> Any:
        value = context.value
        for validator in self.validators:
            value = validator.serialize(context.new(value=value))
        return value
