"""This modules contains the JSON Class types marker."""
from __future__ import annotations
from typing import Callable, Any, Optional, Literal
from copy import deepcopy
from .fields import FieldDescription
from .validators import (UseForValidator, BoolValidator, ChainedValidator,
                         DateValidator, DatetimeValidator, DefaultValidator,
                         DictOfValidator, EagerValidator, EmbeddedValidator,
                         FloatValidator, IndexValidator, InstanceOfValidator,
                         IntValidator, InvalidValidator, LengthValidator,
                         LinkedByValidator, LinkedInValidator,
                         LinkedThruValidator, LinkToValidator, ListOfValidator,
                         MatchValidator, MaxValidator, MaxlengthValidator,
                         MinValidator, MinlengthValidator, NegativeValidator,
                         NonnullValidator, NullableValidator, OneOfValidator,
                         OneOfTypeValidator, PositiveValidator,
                         PresentValidator, PrimaryValidator, RangeValidator,
                         ReadonlyValidator, ReadwriteValidator,
                         RefereeValidator, ReferrerValidator,
                         RequiredValidator, SetOnSaveValidator, ShapeValidator,
                         StrValidator, StrictValidator, TransformValidator,
                         TrimValidator, TruncateValidator, UniqueValidator,
                         ValidateValidator, Validator, WriteNonnullValidator,
                         WriteonceValidator, WriteonlyValidator)

Str = str
Int = int
Float = float


class Types:
    """The class of types marks object. Types marks provide necessary information
    about an json object's shape, transformation, validation, serialization and
    sanitization.
    """

    def __init__(  # pylint: disable=keyword-arg-before-vararg
        self,
        original: Optional[Types] = None,
        *args: Validator
    ) -> None:
        if not original:
            self.fdesc = FieldDescription()
            self.validator = ChainedValidator()
        else:
            self.fdesc = deepcopy(original.fdesc)
            validator = original.validator
            for arg in args:
                validator = validator.append(arg)
                arg.define(self.fdesc)
            self.validator = validator

    @property
    def invalid(self) -> Types:
        """Fields marked with invalid will never be valid, thus these fields
        will never pass validation.
        """
        return Types(self, InvalidValidator())

    @property
    def primary(self) -> Types:
        """Field marked with primary become the object's primary key.
        """
        return Types(self, PrimaryValidator())

    def usefor(self, usage: str) -> Types:
        """Field marked with usefor are queried by JSON Class and it's ORM
        implementations to get user designated fields to perform special
        actions.
        """
        return Types(self, UseForValidator(usage))

    def timestamp(self,
                  usage: Literal['created', 'updated', 'deleted']) -> Types:
        """Field marked with timestamp are special timestamp marks. JSON Class
        and it's ORM implementations use this information to perform special
        actions on timestamp fields.
        """
        return Types(self, UseForValidator(f'{usage}_at'))

    @property
    def readonly(self) -> Types:
        """Fields marked with readonly will not be able to go through
        initialization and set method. You can update value of these fields
        directly or through update method. This prevents client side to post data
        directly into these fields.

        `writeonce`, `readonly` and `writenonnull` cannot be presented
        together.
        """
        return Types(self, ReadonlyValidator())

    @property
    def writeonly(self) -> Types:
        """Fields marked with writeonly will not be available in outgoing json form.
        Users' password is a great example of writeonly.
        """
        return Types(self, WriteonlyValidator())

    @property
    def readwrite(self) -> Types:
        """Fields marked with readwrite will be presented in both inputs and outputs.
        This is the default behavior. And this specifier can be omitted.
        """
        return Types(self, ReadwriteValidator())

    @property
    def writeonce(self) -> Types:
        """Fields marked with writeonce can only be set once through initialization
        and set method. You can update value of these fields directly or through
        update method. This is suitable for e.g. dating app user gender. Gender
        should not be changed once set.

        `writeonce`, `readonly` and `writenonnull` cannot be presented
        together.
        """
        return Types(self, WriteonceValidator())

    @property
    def writenonnull(self) -> Types:
        """Fields marked with writenonnull can only be set to a nonnull value.
        The update method doesn't have this limitation. This prevents user from
        setting present value back into None.

        `writeonce`, `readonly` and `writenonnull` cannot be presented
        together.
        """
        return Types(self, WriteNonnullValidator())

    @property
    def internal(self) -> Types:
        """Fields marked with internal will not be accepted as input, and it
        will not be present in output. These fields are internal and hidden
        from users.
        """
        return Types(self, ReadonlyValidator(), WriteonlyValidator())

    @property
    def index(self) -> Types:
        """Fields marked with index are picked up by ORM integrations to setup
        database column index for you. This marker doesn't have any effect
        around transforming and validating.
        """
        return Types(self, IndexValidator())

    @property
    def unique(self) -> Types:
        """Fields marked with unique are picked up by ORM integrations to setup
        database column unique index for you. This marker doesn't have any effect
        around transforming and validating. When database engine raises an
        exception, jsonclasses's web framework integration will catch it and return
        400 automatically.

        If you are implementing jsonclasses ORM integration, you should use
        UniqueFieldException provided by jsonclasses.exceptions to keep consistency
        with other jsonclasses integrations.
        """
        return Types(self, UniqueValidator())

    @property
    def embedded(self) -> Types:
        """Instance fields marked with the embedded mark is embedded into the
        hosting document for noSQL databases.
        """
        return Types(self, EmbeddedValidator())

    @property
    def linkto(self) -> Types:
        """In a database relationship, fields marked with linkto save an id of
        the object being referenced at the local table.
        """
        return Types(self, LinkToValidator())

    def linkedby(self, foreign_key: str) -> Types:
        """In a database relationship, fields marked with linkedby find reference
        from the destination table.
        """
        return Types(self, LinkedByValidator(foreign_key))

    def linkedthru(self, foreign_key: str) -> Types:
        """In a database relationship, fields marked with linkedthru save
        relationships to a designated association table and find references through
        it.
        """
        return Types(self, LinkedThruValidator(foreign_key))

    def linkedin(self, cls: Any) -> Types:
        """In a database relationship, fields marked with linkedin save
        relationships to the table under provided class.
        """
        return Types(self, LinkedInValidator(cls))

    def referrer(self, referrer_key: str) -> Types:
        """In a many to many database relationship, fields marked with referrer has
        a provided custom key name in the association table.
        """
        return Types(self, ReferrerValidator(referrer_key))

    def referee(self, referee_key: str) -> Types:
        """In a many to many database relationship, fields marked with referee
        reference the other side of the relationship with this provided custom key
        name.
        """
        return Types(self, RefereeValidator(referee_key))

    @property
    def str(self) -> Types:
        """Fields marked with str should be str type. This is a type marker.
        """
        return Types(self, StrValidator())

    def match(self, pattern: Str) -> Types:
        """Fields marked with match are tested againest the argument regular
        expression pattern.
        """
        return Types(self, MatchValidator(pattern))

    def oneof(self, str_list: list[Str]) -> Types:
        """This is the enum equivalent for jsonclasses. Values in the provided list
        are considered valid values.
        """
        return Types(self, OneOfValidator(str_list))

    def minlength(self, length: int) -> Types:
        """Values at fields marked with minlength should have a length which is not
        less than length.

        Args:
          length (int): The minimum length required for the value.

        Returns:
          Types: A new types chained with this marker.
        """
        return Types(self, MinlengthValidator(length))

    def maxlength(self, length: int) -> Types:
        """Values at fields marked with maxlength should have a length which is not
        greater than length.

        Args:
          length (int): The minimum length required for the value.

        Returns:
          Types: A new types chained with this marker.
        """
        return Types(self, MaxlengthValidator(length))

    def length(self, minlength: int, maxlength: Optional[int] = None) -> Types:
        """Fields marked with length should have a length which is between the two
        arguments. If only one argument is provided, the value length should be
        exactly that length.

        Args:
          minlength (int): The minimum length required for the value.
          maxlength (Optional[int]): The maximum length required for the value.

        Returns:
          Types: A new types chained with this marker.
        """
        return Types(self, LengthValidator(minlength, maxlength))

    @property
    def int(self) -> Types:
        """Fields marked with int should be int type. This is a type marker.
        """
        return Types(self, IntValidator())

    @property
    def float(self) -> Types:
        """Fields marked with float should be float type. This is a type marker.
        """
        return Types(self, FloatValidator())

    def min(self, value: Float) -> Types:
        """Fields marked with min are tested again this value. Values less than
        the argument value are considered invalid.
        """
        return Types(self, MinValidator(value))

    def max(self, value: Float) -> Types:
        """Fields marked with max are tested again this value. Values greater than
        the argument value are considered invalid.
        """
        return Types(self, MaxValidator(value))

    def range(self, min_value: Float, max_value: Float) -> Types:
        """Fields marked with range are tested again argument values. Only values
        between the arguments range are considered valid.
        """
        return Types(self, RangeValidator(min_value, max_value))

    @property
    def negative(self) -> Types:
        """Fields marked with negative should have a value less than zero.
        """
        return Types(self, NegativeValidator())

    @property
    def positive(self) -> Types:
        """Fields marked with negative should have a value greater than zero.
        """
        return Types(self, PositiveValidator())

    @property
    def bool(self) -> Types:
        """Fields marked with bool should be bool type. This is a type marker.
        """
        return Types(self, BoolValidator())

    @property
    def date(self) -> Types:
        """Fields marked with date should be date type. This is a type marker.
        """
        return Types(self, DateValidator())

    @property
    def datetime(self) -> Types:
        """Fields marked with datetime should be datetime type. This is a type
        marker.
        """
        return Types(self, DatetimeValidator())

    def listof(self, item_types: Any) -> Types:
        """Fields marked with listof should be a list of the given type. This is a
        type marker.
        """
        return Types(self, ListOfValidator(item_types))

    def dictof(self, item_types: Any) -> Types:
        """Fields marked with listof should be a str keyed dict of the given type.
        This is a type marker.
        """
        return Types(self, DictOfValidator(item_types))

    def shape(self, item_types_map: dict[Str, Any]) -> Types:
        """Fields marked with shape are objects shaped with given shape. This is a
        type marker.
        """
        return Types(self, ShapeValidator(item_types_map))

    @property
    def strict(self) -> Types:
        """Shape fields marked with strict disallow undefined keys.
        """
        return Types(self, StrictValidator())

    def instanceof(self, json_object_class: Any) -> Types:
        """Fields marked with instance of are objects of given class.
        """
        return Types(self, InstanceOfValidator(json_object_class))

    def oneoftype(self, type_list: list[Any]) -> Types:
        """Fields marked with oneoftype accepts value from these types.
        """
        return Types(self, OneOfTypeValidator(type_list))

    @property
    def required(self) -> Types:
        """Fields marked with required are invalid when value is not presented aka
        None.

        Returns:
          Types: A new types chained with this marker.
        """
        return Types(self, RequiredValidator())

    @property
    def nullable(self) -> Types:
        """Fields marked with nullable can be None. This is the default
        behavior even without this marker. It's the opposite to required
        marker. Values inside lists have implicitly required marker. Use this
        to allow null or None values inside lists.

        Returns:
          Types: A new types chained with this marker.
        """
        return Types(self, NullableValidator())

    @property
    def present(self) -> Types:
        """When validating, field marked with present, can not pass validation
        if it has a None value. This is useful for foreign key fields to do
        required validation.
        """
        return Types(self, PresentValidator())

    def validate(self, validate_callable) -> Types:
        """The validate field mark takes a validator callable as its sole argument.
        Use this to define custom field value validations.

        Args:
          validate_callable (Callable): The validate callable tasks 3 arguments,
          value, key_path, and root. Returning None means the value is valid, while
          returning a str message means the validation failed.

        Returns:
          Types: A new types chained with this marker.
        """
        return Types(self, ValidateValidator(validate_callable))

    # transformers

    def default(self, value: Any) -> Types:
        """During initialization, if values of fields with default are not provided.
        The default value is used instead of leaving blank.

        Args:
          value (any): The default value of this field. If the value is callable,
          it's return value is used.

        Returns:
          Types: A new types chained with this marker.
        """
        return Types(self, DefaultValidator(value))

    def truncate(self, max_length: Int) -> Types:
        """During initialization and set, if string value is too long, it's
        truncated to argument max length.

        Args:
          max_length (int): The allowed max length of the field value.

        Returns:
          Types: A new types chained with this marker.
        """
        return Types(self, TruncateValidator(max_length))

    @property
    def trim(self) -> Types:
        """This marker will trim string value. Remove leading and trailing
        whitespaces.

        Returns:
            Types: A new types chained with this marker.
        """
        return Types(self, TrimValidator())

    def transform(self, transformer: Callable) -> Types:
        """This mark applies transfromer on the value. When value is None, the
        transformer is not called. This class barely means to transform. Use
        default mark with a callable to assign calculated default value.

        Args:
          transformer (Callable): This transformer function takes one argument
          which is the current value of the field.

        Returns:
          Types: A new types chained with this marker.
        """
        return Types(self, EagerValidator(), TransformValidator(transformer))

    def setonsave(self, setter: Callable) -> Types:
        """Setonsave marker marks a field to be updated just before serializing
        into the database if this field is modified and to be serialized.

        Args:
          setter (Callable): This setter function takes zero or one argument
          which is the current value of the field.

        Returns:
          Types: A new types chained with this marker.
        """
        return Types(self, SetOnSaveValidator(setter))

    @property
    def nonnull(self) -> Types:
        """This marker is a instructional transformer designated for shape, dictof
        and listof. This is not a validator. To mark a field is required and should
        not be null, use `required` instead. This transformer should be used right
        before shape, dictof and listof, to given an instruction of not leaving
        null for the field.

        Returns:
          Types: A new types chained with this marker.
        """
        return Types(self, NonnullValidator())


types = Types()
"""The root of the types marker. To mark an field with type annotation,
accessor annotation, validator annotation and transformer annotation, use types
like this:

  @jsonclass
  class MyObject(JSONObject):
    my_field_one: bool = types.bool.readonly.required
    my_field_two: password = types.bool.writeonly.length(8, 16).transform(salt\
).required
"""
