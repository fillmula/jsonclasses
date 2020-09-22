"""module for chained validator."""
from __future__ import annotations
from typing import List, Dict, Any, Optional
from functools import reduce
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator
from ..utils.eager_validator_index_after_index import eager_validator_index_after_index
from ..utils.last_eager_validator_index import last_eager_validator_index
from ..contexts import ValidatingContext, TransformingContext


class ChainedValidator(Validator):
    """Chained validator has a series of validators chained."""

    def __init__(self, validators: Optional[List[Validator]] = None) -> None:
        self.validators = validators or []

    def append(self, *args: Validator) -> ChainedValidator:
        """Append validators to this chained validator chain."""
        return ChainedValidator([*self.validators, *args])

    def validate(self, context: ValidatingContext) -> None:
        root = context.root if context.root is not None else context.value
        keypath_messages: Dict[str, str] = {}
        start_validator_index = last_eager_validator_index(self.validators)
        for validator in self.validators[start_validator_index:]:
            try:
                validator_context = ValidatingContext(
                    value=context.value,
                    keypath=context.keypath,
                    root=root,
                    all_fields=context.all_fields,
                    config=context.config)
                validator.validate(validator_context)
            except ValidationException as exception:
                keypath_messages.update(exception.keypath_messages)
                if not context.all_fields:
                    break
        if len(keypath_messages) > 0:
            raise ValidationException(keypath_messages, root)

    def _validate_and_transform(self,
                                validator: Validator,
                                context: ValidatingContext) -> Any:
        """Validate as transform."""
        validator.validate(context)
        transforming_context = TransformingContext(
            value=context.value,
            keypath=context.keypath,
            root=context.root,
            all_fields=context.all_fields,
            config=context.config)
        return validator.transform(transforming_context)

    def _build_context(self,
                       value: Any,
                       keypath: str,
                       root: Any,
                       all_fields: bool,
                       config: Config) -> ValidatingContext:
        return ValidatingContext(value=value,
                                 keypath=keypath,
                                 root=root,
                                 all_fields=all_fields,
                                 config=config)

    def _build_t_context(self,
                       value: Any,
                       keypath: str,
                       root: Any,
                       all_fields: bool,
                       config: Config) -> TransformingContext:
        return TransformingContext(value=value,
                                 keypath=keypath,
                                 root=root,
                                 all_fields=all_fields,
                                 config=config)

    # flake8: noqa: E501
    def transform(self, context: TransformingContext) -> Any:
        curvalue = context.value
        index = 0
        next_index = eager_validator_index_after_index(self.validators, index)
        while next_index is not None:
            validators = self.validators[index:next_index]
            curvalue = reduce(lambda v, validator: self._validate_and_transform(
                validator, self._build_context(v, context.keypath, context.root, context.all_fields, context.config)), validators, curvalue)
            index = next_index + 1
            next_index = eager_validator_index_after_index(self.validators, index)
        curvalue = reduce(lambda v, validator: validator.transform(
            self._build_t_context(v, context.keypath, context.root, context.all_fields, context.config)), self.validators[index:], curvalue)
        return curvalue

    def tojson(self, value: Any, config: Config) -> Any:
        return reduce(lambda v, validator: validator.tojson(v, config), self.validators, value)
