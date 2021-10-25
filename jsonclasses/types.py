"""This modules contains the JSONClasses types modifier."""
from __future__ import annotations
from typing import Callable, Any, Optional
from datetime import date, datetime, timedelta
from enum import Enum
from copy import deepcopy
from .jobject import JObject
from .fdef import Fdef
from .keypath import new_mongoid
from .modifiers import (BoolModifier, ChainedModifier, FValModifier,
                        CompareModifier, DateModifier, DatetimeModifier,
                        DefaultModifier, DictOfModifier, EagerModifier,
                        EmbeddedModifier, EnumModifier, EqModifier, NeqModifier,
                        FloatModifier, IndexModifier, InputAllModifier,
                        InputNameModifier, InputLnameModifier, AtModifier,
                        InputValueModifier, InstanceOfModifier, ThisModifier,
                        IntModifier, InvalidModifier, LengthModifier,
                        LinkedByModifier, LinkedInModifier, GetterModifier,
                        LinkedThruModifier, LinkToModifier, ListOfModifier,
                        MatchModifier, MaxModifier, MaxlengthModifier,
                        LtModifier, MinModifier, MinlengthModifier, GtModifier,
                        NegativeModifier, NonnullModifier, NullableModifier,
                        OneOfModifier, UnionModifier, OnWriteModifier,
                        OnSaveModifier, OnUpdateModifier, OutputLnameModifier,
                        OutputNameModifier, OutputValueModifier, IsObjOfModifier,
                        PositiveModifier, PresentModifier, SetterModifier,
                        NonnegativeModifier, NonpositiveModifier,
                        PresentWithModifier, PresentWithoutModifier,
                        PreserializeModifier, PrimaryModifier, IsThisModifier,
                        RangeModifier, ReadonlyModifier, ReadwriteModifier,
                        RefereeModifier, ReferrerModifier, OneIsValidModifier,
                        RequiredModifier, ResetModifier, SetOnSaveModifier,
                        FSetOnSaveModifier, AddModifier, SubModifier,
                        DivModifier, ModModifier, MulModifier, GetOpModifier,
                        StrModifier, StrictModifier, AssignModifier,
                        TempModifier, TransformModifier, TrimModifier,
                        TruncateModifier, ValidateModifier,
                        Modifier, WriteNonnullModifier, WriteonceModifier,
                        WriteonlyModifier, DenyModifier, CascadeModifier,
                        NullifyModifier, AsopModifier,
                        AsopdModifier, UrlModifier, EmailModifier,
                        DigitModifier,AlphaModifier,NumericModifier,
                        AlnumModifier,ToTitleModifier,ToCapModifier,
                        ToLowerModifier,ToUpperModifier,RoundModifier,
                        UnresolvedModifier, AnyModifier, CeilModifier,
                        FloorModifier, BeforeModifier, AfterModifier,
                        ReverseModifier, ReplaceModifier, ReplacerModifier,
                        OddModifier, EvenModifier, AbsModifier,SplitModifier,
                        JoinModifier, AuthIdentityModifier, SaltModifier,
                        AuthByModifier, PassinModifier, CheckpwModifier,
                        ToListModifier, ToBoolModifier, ToFloatModifier,
                        ToIntModifier, ToStrModifier, RandomDigitsModifier,
                        RandomAlnumpuncsModifier, RandomAlnumsModifier,
                        RandomIntModifier, RandomFloatModifier,
                        ToBoSecModifier, ToBoMinModifier, ToBoHourModifier,
                        ToNextSecModifier, ToNextMinModifier, UploaderModifier,
                        ToNextHourModifier, CrossFetchModifier,
                        ToNextMonModifier, ToNextYearModifier, IsObjModifier,
                        ToNextDayModifier, ToBoYearModifier, ToBoMonModifier,
                        ToBoDayModifier, PadStartModifier, PadEndModifier,
                        UnqueryableModifier, QueryableModifier, PowModifier,
                        FormatDatetimeModifier, NoCopyModifier, SqrtModifier,
                        CanCModifier, CanUModifier, CanRModifier, MapModifier,
                        FilterModifier, HasPrefixModifier, HasSuffixModifier,
                        InsertAtModifier, AppendModifier, PrependModifier,
                        WrapIntoListModifier, IsPrefixOfModifier,
                        IsSuffixOfModifier, InverseModifier, UpperbondModifier,
                        LowerbondModifier)

Str = str
Int = int
Float = float
Date = date
Datetime = datetime


class Types:
    """The class of types marks object. Types marks provide necessary
    information about an json object's shape, transformation, validation,
    serialization and sanitization.
    """

    def __init__(  # pylint: disable=keyword-arg-before-vararg
        self,
        original: Optional[Types] = None,
        *args: Modifier
    ) -> None:
        if not original:
            self.fdef = Fdef()
            self.modifier = ChainedModifier()
        else:
            self.fdef = deepcopy(original.fdef)
            modifier = original.modifier
            for arg in args:
                modifier = modifier.append(arg)
                arg.define(self.fdef)
            self.modifier = modifier

    @property
    def invalid(self) -> Types:
        """Fields marked with invalid will never be valid, thus these fields
        will never pass validation.
        """
        return Types(self, InvalidModifier())

    @property
    def primary(self) -> Types:
        """Field marked with primary become the object's primary key.
        """
        return Types(self, PrimaryModifier())

    @property
    def readonly(self) -> Types:
        """Fields marked with readonly will not be able to go through
        initialization and set method. You can update value of these fields
        directly or through update method. This prevents client side to post
        data directly into these fields.

        `writeonce`, `readonly` and `writenonnull` cannot be presented
        together.
        """
        return Types(self, ReadonlyModifier())

    @property
    def writeonly(self) -> Types:
        """Fields marked with writeonly will not be available in outgoing json
        form. Users' password is a great example of writeonly.
        """
        return Types(self, WriteonlyModifier())

    @property
    def readwrite(self) -> Types:
        """Fields marked with readwrite will be presented in both inputs and
        outputs. This is the default behavior. And this specifier can be
        omitted.
        """
        return Types(self, ReadwriteModifier())

    @property
    def writeonce(self) -> Types:
        """Fields marked with writeonce can only be set once through
        initialization and set method. You can update value of these fields
        directly or through update method. This is suitable for e.g. dating app
        user gender. Gender should not be changed once set.

        `writeonce`, `readonly` and `writenonnull` cannot be presented
        together.
        """
        return Types(self, WriteonceModifier())

    @property
    def writenonnull(self) -> Types:
        """Fields marked with writenonnull can only be set to a nonnull value.
        The update method doesn't have this limitation. This prevents user from
        setting present value back into None.

        `writeonce`, `readonly` and `writenonnull` cannot be presented
        together.
        """
        return Types(self, WriteNonnullModifier())

    @property
    def internal(self) -> Types:
        """Fields marked with internal will not be accepted as input, and it
        will not be present in output. These fields are internal and hidden
        from users.
        """
        return Types(self, ReadonlyModifier(), WriteonlyModifier())

    @property
    def temp(self) -> Types:
        """Fields marked with temp won't be written into database. As soon as
        database writing happens, value of this field is cleared and set to
        None. Examples of it's use cases are authentication code validation,
        input validation, etc.
        """
        return Types(self, TempModifier())

    @property
    def index(self) -> Types:
        """Fields marked with index are picked up by ORM integrations to setup
        database column index for you. This modifier doesn't have any effect
        around transforming and validating.
        """
        return Types(self, IndexModifier(False))

    def cindex(self, index_name: str) -> Types:
        """Fields marked with cindex have compound indexes. This modifier
        doesn't have any effect around transforming and validating.
        """
        return Types(self, IndexModifier(False, index_name))

    @property
    def unique(self) -> Types:
        """Fields marked with unique are picked up by ORM integrations to setup
        database column unique index for you. This modifier doesn't have any
        effect around transforming and validating. When database engine raises
        an exception, jsonclasses's web framework integration will catch it and
        return 400 automatically.

        If you are implementing jsonclasses ORM integration, you should use
        UniqueFieldException provided by jsonclasses.excs to keep
        consistency with other jsonclasses integrations.
        """
        return Types(self, IndexModifier(True))

    def cunique(self, index_name: str) -> Types:
        """Fields marked with cunique have compound indexes. This is a unique
        index. This modifier doesn't have any effect around transforming and
        validating.
        """
        return Types(self, IndexModifier(True, index_name))

    @property
    def queryable(self) -> Types:
        """Fields marked with queryable is queryable. This is the default
        behavior.
        """
        return Types(self, QueryableModifier())

    @property
    def unqueryable(self) -> Types:
        """Fields marked with unqueryable is not queryable.
        """
        return Types(self, UnqueryableModifier())

    @property
    def embedded(self) -> Types:
        """Instance fields marked with the embedded mark is embedded into the
        hosting document for noSQL databases.
        """
        return Types(self, EmbeddedModifier())

    def getter(self, calc: Callable | Types) -> Types:
        """Getter modifier marks a field as calculated field. It's not stored.
        """
        return Types(self, GetterModifier(calc))

    def setter(self, setter: Callable | Types) -> Types:
        """Setter modifier provides setter to calculated fields.
        """
        return Types(self, SetterModifier(setter))

    @property
    def nocopy(self) -> Types:
        """NoCopy modifier marks fields is nocopy.
        """
        return Types(self, NoCopyModifier())

    @property
    def linkto(self) -> Types:
        """In a database relationship, fields marked with linkto save an id of
        the object being referenced at the local table.
        """
        return Types(self, LinkToModifier())

    def linkedby(self, foreign_key: str) -> Types:
        """In a database relationship, fields marked with linkedby find
        reference from the destination table.
        """
        return Types(self, LinkedByModifier(foreign_key))

    def linkedthru(self, foreign_key: str) -> Types:
        """In a database relationship, fields marked with linkedthru save
        relationships to a designated association table and find references
        through it.
        """
        return Types(self, LinkedThruModifier(foreign_key))

    def linkedin(self, cls: Any) -> Types:
        """In a database relationship, fields marked with linkedin save
        relationships to the table under provided class.
        """
        return Types(self, LinkedInModifier(cls))

    def referrer(self, referrer_key: str) -> Types:
        """In a many to many database relationship, fields marked with referrer
        has a provided custom key name in the association table.
        """
        return Types(self, ReferrerModifier(referrer_key))

    def referee(self, referee_key: str) -> Types:
        """In a many to many database relationship, fields marked with referee
        reference the other side of the relationship with this provided custom
        key name.
        """
        return Types(self, RefereeModifier(referee_key))

    @property
    def nullify(self) -> Types:
        """When an object is deleted, linked objects' references are set to
        null instead of deleted.
        """
        return Types(self, NullifyModifier())

    @property
    def cascade(self) -> Types:
        """When an object is deleted, linked objects with cascade relationship
        are deleted.
        """
        return Types(self, CascadeModifier())

    @property
    def deny(self) -> Types:
        """When an object is deleted, linked objects with deny relationship
        prevent this object being deleted.
        """
        return Types(self, DenyModifier())

    @property
    def str(self) -> Types:
        """Fields marked with str should be str type. This is a type modifier.
        """
        return Types(self, StrModifier())

    def match(self, pattern: Str | Callable | Types) -> Types:
        """Fields marked with match are tested againest the argument regular
        expression pattern.
        """
        return Types(self, MatchModifier(pattern))

    def oneof(self, str_list: list[Str]) -> Types:
        """This is the enum equivalent for jsonclasses. Values in the provided
        list are considered valid values.
        """
        return Types(self, OneOfModifier(str_list))

    def minlength(self, length: int | Callable | Types) -> Types:
        """The value of iterable should be longer than the provided minlength.

        Args:
          length (int): The minimum length required for the value.

        Returns:
          Types: A new types chained with this modifier.
        """
        return Types(self, MinlengthModifier(length))

    def maxlength(self, length: int | Callable | Types) -> Types:
        """The value of iterable should be shorter than the provided maxlength.

        Args:
          length (int): The maximum length required for the value.

        Returns:
          Types: A new types chained with this modifier.
        """
        return Types(self, MaxlengthModifier(length))

    def length(self, minlength: int, maxlength: Optional[int] = None) -> Types:
        """Fields marked with length should have a length which is between the
        two arguments. If only one argument is provided, the value length
        should be exactly that length.

        Args:
          minlength (int): The minimum length required for the value.
          maxlength (Optional[int]): The maximum length required for the value.

        Returns:
          Types: A new types chained with this modifier.
        """
        return Types(self, LengthModifier(minlength, maxlength))

    def add(self, by: int | float | Callable | Types) -> Types:
        """This modifier adds int or float value to original value

        """
        return Types(self, EagerModifier(), AddModifier(by))

    def sub(self, by: int | float | Callable | Types) -> Types:
        """This modifier for Int or float value subs original value
        """
        return Types(self, EagerModifier(), SubModifier(by))

    def mul(self, by: int | float | Callable | Types) -> Types:
        """This modifier for Int or float value muls by original value
        """
        return Types(self, EagerModifier(), MulModifier(by))

    def pow(self, by: int | float | Callable | Types) -> Types:
        """This modifer is used to transform the value of the int or float value
        to the power of the original value
        """
        return Types(self, EagerModifier(), PowModifier(by))

    def div(self, by: int | float | Callable | Types) -> Types:
        """This modifier for Int or float value divs by original value
        """
        return Types(self, EagerModifier(), DivModifier(by))

    def mod(self, by: int | float | Callable | Types) -> Types:
        """This modifier for Int or float value mods original value
        """
        return Types(self, EagerModifier(), ModModifier(by))

    def map(self, validate_callable: Callable) -> Types:
        """This modifier is used to getting a map object of the results
        """
        return Types(self, EagerModifier(), MapModifier(validate_callable))

    def filter(self, validate_callable: Callable) -> Types:
        """This modifier is used to filter the given sequence
        """
        return Types(self, EagerModifier(), FilterModifier(validate_callable))

    def hasprefix(self, validate_prefix: str | list[str | int] | Callable | Types) -> Types:
        """Hasprefix modifier validates if a string is prefix of another string
        or a list is prefix of another list
        """
        return Types(self, HasPrefixModifier(validate_prefix))

    def hassuffix(self, validate_suffix: str | list[str | int] | Callable | Types) -> Types:
        """Hassuffix modifier validates if a string is suffix of another string
        or a list is suffix of another list
        """
        return Types(self, HasSuffixModifier(validate_suffix))

    def isprefixof(self, prefix: str | list[str | int] | Callable | Types) -> Types:
        """Hassuffix modifier validates if a string is suffix of another string
        or a list is suffix of another list
        """
        return Types(self, IsPrefixOfModifier(prefix))

    def issuffixof(self, suffix: str | list[str | int] | Callable | Types) -> Types:
        """Hassuffix modifier validates if a string is suffix of another string
        or a list is suffix of another list
        """
        return Types(self, IsSuffixOfModifier(suffix))

    def insertat(self, item: Any | Callable | Types, index: int | Callable | Types) -> Types:
        """
        """
        return Types(self, EagerModifier(), InsertAtModifier(item, index))

    def prepend(self, item: str | int | float | Callable | Types) -> Types:
        """
        """
        return Types(self, EagerModifier(), PrependModifier(item))

    def append(self, item: str | int | float | Callable | Types) -> Types:
        """
        """
        return Types(self, EagerModifier(), AppendModifier(item))

    def upperbond(self, max_value: int | float | Callable | Types) -> Types:
        """Decrease the value of the field to upperbond if the value of the
        field is larger than upperbond.
        """
        return Types(self, EagerModifier(), UpperbondModifier(max_value))

    def lowerbond(self, min_value: int | float | Callable | Types) -> Types:
        """Increase the value of the field to lowerbond if the value of the
        field is smaller than lowerbond.
        """
        return Types(self, EagerModifier(), LowerbondModifier(min_value))

    @property
    def inverse(self) -> Types:
        """Change the value to false if value is true, vice versa.
        """
        return Types(self, EagerModifier(), InverseModifier())

    @property
    def wrapintolist(self) -> Types:
        """
        """
        return Types(self, WrapIntoListModifier())

    @property
    def sqrt(self) -> Types:
        """This modifier is used to transform the square root of any number.
        """
        return Types(self, EagerModifier(), SqrtModifier())

    @property
    def url(self) -> Types:
        """Fields marked with url should be valid url string.
        """
        return Types(self, UrlModifier())

    @property
    def digit(self) -> Types:
        """Values of fields marked with digit should be valid digit string.
        """
        return Types(self, DigitModifier())

    @property
    def alpha(self) -> Types:
        """Values of fields marked with alpha should be valid alpha string.
        """
        return Types(self, AlphaModifier())

    @property
    def numeric(self) -> Types:
        """Values of fields marked with numeric should be valid numeric string.
        """
        return Types(self, NumericModifier())

    @property
    def email(self) -> Types:
        """Values of fields marked with email should be valid email format.
        """
        return Types(self, EmailModifier())

    @property
    def alnum(self) -> Types:
        """Values fields marked with alnum should be valid alnum strings.
        """
        return Types(self, AlnumModifier())

    @property
    def int(self) -> Types:
        """Fields marked with int should be int type. This is a type modifier.
        """
        return Types(self, IntModifier())

    @property
    def odd(self) -> Types:
        """Fields marked with int should be odd. This is a int type modifier.
        """
        return Types(self, OddModifier())

    @property
    def even(self) -> Types:
        """Fields marked with int should be even. This is a int type modifier.
        """
        return Types(self, EvenModifier())

    @property
    def float(self) -> Types:
        """Fields marked with float should be float type. This is a type
        modifier.
        """
        return Types(self, FloatModifier())

    def min(self, value: Float | Callable | Types) -> Types:
        """Fields marked with min are tested again this value. Values less than
        the argument value are considered invalid.
        """
        return Types(self, MinModifier(value))

    def max(self, value: Float | Callable | Types) -> Types:
        """Fields marked with max are tested again this value. Values greater
        than the argument value are considered invalid.
        """
        return Types(self, MaxModifier(value))

    def lte(self, value: Float | Callable | Types) -> Types:
        """Fields marked with lte are tested again this value. Values greater
        than the argument value are considered invalid.
        """
        return Types(self, MaxModifier(value))

    def gte(self, value: Float | Callable | Types) -> Types:
        """Fields marked with gte are tested again this value. Values less than
        the argument value are considered invalid.
        """
        return Types(self, MinModifier(value))

    def lt(self, value: Float | Callable | Types) -> Types:
        """Fields marked with lt are tested again this value. Values greater
        or equal than the argument value are considered invalid.
        """
        return Types(self, LtModifier(value))

    def gt(self, value: Float | Callable | Types) -> Types:
        """Fields marked with gt are tested again this value. Values less than
        or equal than the argument value are considered invalid.
        """
        return Types(self, GtModifier(value))


    def range(self, min_value: Float | Callable | Types, max_value: Float | Callable | Types) -> Types:
        """Fields marked with range are tested again argument values. Only
        values between the arguments range are considered valid.
        """
        return Types(self, RangeModifier(min_value, max_value))

    @property
    def negative(self) -> Types:
        """Fields marked with negative should have a value less than zero.
        """
        return Types(self, NegativeModifier())

    @property
    def positive(self) -> Types:
        """Fields marked with negative should have a value greater than zero.
        """
        return Types(self, PositiveModifier())

    @property
    def nonnegative(self) -> Types:
        """Fields marked with nonnegative should have a value greater than or
        equal to zero.
        """
        return Types(self, NonnegativeModifier())

    @property
    def nonpositive(self) -> Types:
        """Fields marked with nonnegative should have a value less than or
        equal to zero.
        """
        return Types(self, NonpositiveModifier())

    @property
    def bool(self) -> Types:
        """Fields marked with bool should be bool type. This is a type modifier.
        """
        return Types(self, BoolModifier())

    @property
    def date(self) -> Types:
        """Fields marked with date should be date type. This is a type modifier.
        """
        return Types(self, DateModifier())

    @property
    def datetime(self) -> Types:
        """Fields marked with datetime should be datetime type. This is a type
        modifier.
        """
        return Types(self, DatetimeModifier())

    def before(self, point: Date | Datetime | Callable | Types) -> Types:
        """InputDate should be before the date. This is a date modifier
        """
        return Types(self, BeforeModifier(point))

    def after(self, point: Date | Datetime | Callable | Types) -> Types:
        """InputDate should be after the date. This is a date modifier
        """
        return Types(self, AfterModifier(point))

    @property
    def tobosec(self) -> Types:
        """This modifier empty the microsecond in datetime.
        """
        return Types(self, EagerModifier(), ToBoSecModifier())

    @property
    def tobomin(self) -> Types:
        """This modifier empty the microsecond and second in datetime
        """
        return Types(self, EagerModifier(), ToBoMinModifier())

    @property
    def tobohour(self) -> Types:
        """This modifier empty microsecond, second and minute in datetime
        """
        return Types(self, EagerModifier(), ToBoHourModifier())

    @property
    def tonextsec(self) -> Types:
        """This modifier Go to the next second in datetime
        """
        return Types(self, EagerModifier(), ToNextSecModifier())

    @property
    def tonextmin(self) -> Types:
        """This modifier Go to the next minute in datetime
        """
        return Types(self, EagerModifier(), ToNextMinModifier())

    @property
    def tonexthour(self) -> Types:
        """This modifier Go to the next hour in datetime
        """
        return Types(self, EagerModifier(), ToNextHourModifier())

    @property
    def tonextyear(self) -> Types:
        """This modifier Go to the next year in datetime or in date
        """
        return Types(self, EagerModifier(), ToNextYearModifier())

    @property
    def tonextmon(self) -> Types:
        """This modifier Go to the next month in datetime or in date
        """
        return Types(self, EagerModifier(), ToNextMonModifier())

    @property
    def tonextday(self) -> Types:
        """This modifier Go to the next day in datetime or in date
        """
        return Types(self, EagerModifier(), ToNextDayModifier())

    @property
    def toboyear(self) -> Types:
        """This modifier empty microsecond, second, minute, hour, day and month
        in datetime or empty day, month in date
        """
        return Types(self, EagerModifier(), ToBoYearModifier())

    @property
    def tobomon(self) -> Types:
        """This modifier empty microsecond, second, minute, hour and day in
        datetime or empty day in date
        """
        return Types(self, EagerModifier(), ToBoMonModifier())

    @property
    def toboday(self) -> Types:
        """This modifier empty microsecond, second, minute and hour in
        datetime or return date directly
        """
        return Types(self, EagerModifier(), ToBoDayModifier())

    def fmtd(self, format: str | Callable | Types) -> Types:
        """This modifier format datetime or date value.
        """
        return Types(self, FormatDatetimeModifier(format))

    def enum(self, enum_class: type[Enum] | str) -> Types:
        """Fields marked with enum should be enum value of provided enum type.
        This is a type modifier.
        """
        return Types(self, EnumModifier(enum_class))

    @property
    def inputall(self) -> Types:
        """Inputall makes enum field to accept all kinds of acceptable enum
        values in any forms.
        """
        return Types(self, InputAllModifier())

    @property
    def inputlname(self) -> Types:
        """Inputlname makes enum field to accept enum's lowercase name as
        input.
        """
        return Types(self, InputLnameModifier())

    @property
    def inputname(self) -> Types:
        """Inputlname makes enum field to accept enum's uppercase name as
        input.
        """
        return Types(self, InputNameModifier())

    @property
    def inputvalue(self) -> Types:
        """Inputlname makes enum field to accept enum's value as input.
        """
        return Types(self, InputValueModifier())

    @property
    def outputlname(self) -> Types:
        """Outputlname makes enum field to output lowercase name as display
        value.
        """
        return Types(self, OutputLnameModifier())

    @property
    def outputname(self) -> Types:
        """Outputname makes enum field to output uppercase name as display
        value.
        """
        return Types(self, OutputNameModifier())

    @property
    def outputvalue(self) -> Types:
        """Outputvalue makes enum field to output value as display value.
        """
        return Types(self, OutputValueModifier())

    def listof(self, item_types: Any) -> Types:
        """Fields marked with listof should be a list of the given type. This
        is a type modifier.
        """
        return Types(self, ListOfModifier(item_types))

    def dictof(self, item_types: Any) -> Types:
        """Fields marked with listof should be a str keyed dict of the given
        type. This is a type modifier.
        """
        return Types(self, DictOfModifier(item_types))

    @property
    def strict(self) -> Types:
        """Object fields marked with strict disallow undefined keys.
        """
        return Types(self, StrictModifier())

    def objof(self, jcls: Any) -> Types:
        """Fields marked with objof are objects of given class.
        """
        return Types(self, InstanceOfModifier(jcls))

    def union(self, type_list: list[Any]) -> Types:
        """Fields marked with union accepts value from these types.
        """
        return Types(self, UnionModifier(type_list))

    @property
    def any(self) -> Types:
        """Fields marked with any can be any value.
        """
        return Types(self, AnyModifier())

    @property
    def required(self) -> Types:
        """Fields marked with required are invalid when value is None.

        Returns:
          Types: A new types chained with this modifier.
        """
        return Types(self, RequiredModifier())

    @property
    def nullable(self) -> Types:
        """Fields marked with nullable can be None. This is the default
        behavior even without this modifier. It's the opposite to required
        modifier. Values inside lists have implicitly required modifier. Use
        this to allow null or None values inside lists.

        Returns:
          Types: A new types chained with this modifier.
        """
        return Types(self, NullableModifier())

    @property
    def present(self) -> Types:
        """When validating, field marked with present, can not pass validation
        if it has a None value. This is useful for foreign key fields to do
        required validation.
        """
        return Types(self, PresentModifier())

    def presentwith(self, referring_key: str) -> Types:
        """Fields marked with presentwith modifier are forced presented if
        referring field is present. If referring field has None value, this
        field's value is optional. If referring field has non None value, value
        of this field is required.
        """
        return Types(self, PresentWithModifier(referring_key))

    def presentwithout(self, referring_keys: Str | list[Str]) -> Types:
        """Fields marked with presentwithout modifier are forced presented if
        referring field is not present. If referring field has None value, this
        field's value should be present. If referring field has non None value,
        value of this field is not forced to be present.
        """
        return Types(self, PresentWithoutModifier(referring_keys))

    def validate(self, validator: Callable | Types) -> Types:
        """The validate field mark takes a modifier callable as its sole
        argument. Use this to define custom field value validations.

        Args:
            validator (Callable): The validate callable takes up to 2
            arguments, which are value and context. Returning None or True
            means the value is valid, while returning a str message or False
            means validation failed.

        Returns:
            Types: A new types chained with this modifier.
        """
        return Types(self, ValidateModifier(validator))

    def vmsg(self, validator: Callable | Types, message: str) -> Types:
        """The validate field mark takes a modifier callable as its sole
        argument. Use this to define custom field value validations.

        Args:
            validator (Callable | Types): The validate callable takes up to 2
            arguments, which are value and context. Returning None or True
            means the value is valid, while returning a str message or False
            means validation failed.
            msg (str): The error message to be outputted.

        Returns:
            Types: A new types chained with this modifier.
        """
        return Types(self, ValidateModifier(validator, message))

    def compare(self, compare_callable: Callable) -> Types:
        """The compare field mark takes a modifier callable as its sole
        argument. If value of compared fields are changed, this modifier is
        called with 2 to 5 arguments.

        Args:
            compare_callable (Callable): The compare callable. Arg 1 is the old
            value, arg 2 is the new value, arg 3 is key path, arg 4 is the
            object, arg 5 is the context. Returning None means the value is
            valid, while returning a str message means validation failed.

        Returns:
            Types: A new types chained with this modifier.
        """
        return Types(self,
                     ResetModifier(),
                     CompareModifier(compare_callable))

    # transformers

    def default(self, value: Any) -> Types:
        """During initialization, if values of fields with default are not
        provided. The default value is used instead of leaving blank.

        Args:
          value (any): The default value of this field. If the value is
          callable, it's return value is used.

        Returns:
          Types: A new types chained with this modifier.
        """
        return Types(self, DefaultModifier(value))

    def truncate(self, max_length: Int | Callable | Types) -> Types:
        """During initialization and set, if string value is too long, it's
        truncated to argument max length.

        Args:
          max_length (int): The allowed max length of the field value.

        Returns:
          Types: A new types chained with this modifier.
        """
        return Types(self, EagerModifier(), TruncateModifier(max_length))

    @property
    def trim(self) -> Types:
        """This modifier will trim string value. Remove leading and trailing
        whitespaces.

        Returns:
            Types: A new types chained with this modifier.
        """
        return Types(self, EagerModifier(), TrimModifier())

    @property
    def totitle(self) -> Types:
        """This modifier titlizes string.

        Returns:
            Types: A new types chained with this modifier.
        """
        return Types(self, EagerModifier(), ToTitleModifier())

    @property
    def tocap(self) -> Types:
        """This modifier capitalizes string.

        Returns:
            Types: A new types chained with this modifier.
        """
        return Types(self, EagerModifier(), ToCapModifier())

    @property
    def tolower(self) -> Types:
        """This modifier lowercasefies string.

        Returns:
            Types: A new types chained with this modifier.
        """
        return Types(self, EagerModifier(), ToLowerModifier())

    @property
    def toupper(self) -> Types:
        """This modifier uppercasefies string.

        Returns:
            Types: A new types chained with this modifier.
        """
        return Types(self, EagerModifier(), ToUpperModifier())

    def padstart(self, char: str | Callable | Types, length: int | Callable | Types) -> Types:
        """This modifier padstart string.

        Returns:
            Types: A new types chained with this modifier.
        """
        return Types(self, EagerModifier(), PadStartModifier(char, length))

    def padend(self, char: str | Callable | Types, length: int | Callable | Types) -> Types:
        """This modifier padstart string.

        Returns:
            Types: A new types chained with this modifier.
        """
        return Types(self, EagerModifier(), PadEndModifier(char, length))

    @property
    def tolist(self) -> Types:
        """This modifier transforms value into list.

        Returns:
            Types: A new types chained with this modifier.
        """
        return Types(self, EagerModifier(), ToListModifier())

    @property
    def tobool(self) -> Types:
        """This modifier transforms value into bool.

        Returns:
            Types: A new types chained with this modifier.
        """
        return Types(self, EagerModifier(), ToBoolModifier())

    @property
    def tofloat(self) -> Types:
        """This modifier transforms value into float.

        Returns:
            Types: A new types chained with this modifier.
        """
        return Types(self, EagerModifier(), ToFloatModifier())

    @property
    def toint(self) -> Types:
        """This modifier transforms value into int.

        Returns:
            Types: A new types chained with this modifier.
        """
        return Types(self, EagerModifier(), ToIntModifier())

    @property
    def tostr(self) -> Types:
        """This modifier transforms value into str.

        Returns:
            Types: A new types chained with this modifier.
        """
        return Types(self, EagerModifier(), ToStrModifier())

    def replace(self, old: Str | Callable | Types, new: Str | Callable | Types) -> Types:
        """Replace modifier replaces occurance with substitutions.
        """
        return Types(self, EagerModifier(), ReplaceModifier(old, new))

    def replacer(self, reg: Str | Callable | Types, rep: Str | Callable | Types) -> Types:
        """Replacer modifier replaces occurance matches regular expression with
        replacement string.
        """
        return Types(self, EagerModifier(), ReplacerModifier(reg, rep))

    def split(self, sep: Str | Callable | Types) -> Types:
        """Split modifier splits string into a list of strings.
        """
        return Types(self, EagerModifier(), SplitModifier(sep))

    def join(self, sep: Str | Callable | Types) -> Types:
        """Join modifier concatenates a list of strings into a single string.
        """
        return Types(self, EagerModifier(), JoinModifier(sep))

    @property
    def salt(self) -> Types:
        """Salt modifier add salt to a string.
        """
        return Types(self, EagerModifier(), SaltModifier())

    @property
    def round(self) -> Types:
        """This modifier rounds number value.

        Returns:
            Types: A new types chained with this modifier.
        """
        return Types(self, EagerModifier(), RoundModifier())

    @property
    def ceil(self) -> Types:
        """This modifier ceil number value.

        Returns:
            Types: A new types chained with this modifier.
        """
        return Types(self, EagerModifier(), CeilModifier())

    @property
    def floor(self) -> Types:
        """This modifier floor number value.

        Returns:
            Types: A new types chained with this modifier.
        """
        return Types(self, EagerModifier(), FloorModifier())

    @property
    def abs(self) -> Types:
        """This modifier abs number value.

        Returns:
            Types: A new types chained with this modifier.
        """
        return Types(self, EagerModifier(), AbsModifier())

    def transform(self, transformer: Callable | Types) -> Types:
        """This mark applies transfromer on the value. When value is None, the
        transformer is not called. This class barely means to transform. Use
        default mark with a callable to assign calculated default value.

        Args:
          transformer (Callable): This transformer function takes one argument
          which is the current value of the field.

        Returns:
          Types: A new types chained with this modifier.
        """
        return Types(self, EagerModifier(), TransformModifier(transformer))

    def reverse(self) -> Types:
        """This modifier reverse iterable value

        Returns:
            Types: A new types chained with this modifier.
        """
        return Types(self, EagerModifier(), ReverseModifier())

    def uploader(self, uploader: Callable | str) -> Types:
        """Uploader is barely a syntax alias for transformer. Uploaded files
        can be processed through a transformer and get url attached to this
        object.

        Args:
            uploader (Callable | str): An uploader name or a transformer
            callable.

        Returns:
            Types: A new types chained with this modifier.
        """
        return Types(self, EagerModifier(), UploaderModifier(uploader))

    def asop(self, asop_transformer: Callable) -> Types:
        """Asop modifier assigns transformed operator value to this field. When
        the operator is not present, a ValidationException is raised.

        Args:
            asop_transformer (Callable): This transformer function takes 1 to
            3 arguments. The first one is the opeartor, the second one is the
            value of the field, the third is the transforming context.

        Returns:
            Types: A new types chained with this modifier.
        """
        return Types(self, AsopModifier(asop_transformer))

    @property
    def asopd(self) -> Types:
        """Asopd modifier assigns operator value directly to this field without
        any transforming. When the operator  is not present, a
        ValidationException is raised.

        Returns:
            Types: A new types chained with this modifier.
        """
        return Types(self, AsopdModifier())

    def setonsave(self, setter: Callable) -> Types:
        """Setonsave modifier marks a field to be updated just before
        serializing into the database if this field is modified and to be
        serialized.

        Args:
          setter (Callable): This setter function takes zero or one argument
          which is the current value of the field.

        Returns:
          Types: A new types chained with this modifier.
        """
        return Types(self, PreserializeModifier(), SetOnSaveModifier(setter))

    def fsetonsave(self, setter: Callable) -> Types:
        """Fsetonsave modifier marks a field to be updated just before
        serializing into the database regardless of this field is modified.

        Args:
          setter (Callable): This setter function takes zero or one argument
          which is the current value of the field.

        Returns:
          Types: A new types chained with this modifier.
        """
        return Types(self, PreserializeModifier(), FSetOnSaveModifier(setter))

    def onsave(self, callback: Callable) -> Types:
        """Onsave inserts a callback into the modifier chain. If save action
        is triggered, the callback is called with the current value.

        Args:
            callback (Callable): This callback function takes one argument
            which is the current value of the field.

        Returns:
            Types: A new types chained with this modifier.
        """
        return Types(self, OnSaveModifier(callback))

    def onupdate(self, callback: Callable) -> Types:
        """Onupdate is a callback modifier. If value updated when saving, this
        callback is called with the current value or both values.

        Args:
            callback (Callable): A callable which takes arguments.

        Returns:
            Types: A new types chained with this modifier.
        """
        return Types(self, ResetModifier(), OnUpdateModifier(callback))

    def onwrite(self, callback: Callable) -> Types:
        """Onwrite is a callback modifier. Whenever a new value is being
        serialized into the database, this is called.

        Args:
            callback (Callable): A callable which takes arguments.

        Returns:
            Types: A new types chained with this modifier.
        """
        return Types(self, OnWriteModifier(callback))

    @property
    def nonnull(self) -> Types:
        """This modifier is a instructional transformer designated for dictof
        and listof. This is not a modifier. To mark a field is required and
        should not be null, use `required` instead. This transformer should
        be used right before dictof and listof, to given an instruction of not
        leaving null for the field.

        Returns:
          Types: A new types chained with this modifier.
        """
        return Types(self, NonnullModifier())

    # compound

    @property
    def mongoid(self: Types) -> Types:
        """This modifier assigns a default bson object id to the field.
        """
        return Types(self, DefaultModifier(lambda: new_mongoid()))

    @property
    def tscreated(self: Types) -> Types:
        """This modifier adds a default current time to the field.
        """
        return Types(self, DefaultModifier(datetime.now))

    @property
    def tsupdated(self: Types) -> Types:
        """This modifier adds a default current time and a set on save.
        """
        return Types(self,
                     DefaultModifier(datetime.now),
                     PreserializeModifier(),
                     SetOnSaveModifier(lambda: datetime.now()))

    def umininterval(self: Types, interval: timedelta) -> Types:
        """This modifier compares old and new value against the time interval.
        """
        def compare_callable(old: datetime, new: datetime):
            if new >= old + interval:
                return None
            return 'time interval too short'
        return Types(self,
                     ResetModifier(),
                     CompareModifier(compare_callable))

    # authorization

    @property
    def authidentity(self: Types) -> Types:
        """Fields marked with authidentity are used for authorization.
        """
        return Types(self, AuthIdentityModifier())

    def authby(self: Types, checker: Types) -> Types:
        """Fields marked with authby are used for authorization.
        """
        return Types(self, AuthByModifier(checker))

    @property
    def authbycheckpw(self: Types) -> Types:
        """This is a shortcut to `authby(types.checkpw(types.passin))`.
        """
        return Types(self, AuthByModifier(types.checkpw(types.passin)))


    def canc(self, checker: Callable | Types) -> Types:
        """CanC modifier validates value against the operator object user
        passed in. This modifier is special and doesn't bypass None value. If
        the operator is not present, this modifier fails.

        Args:
            checker (Callable | Types): The checker takes 1 to 4 arguments. The
            first is the operator object, the second is the object being
            operated, the third is the value of the field, the fourth is the
            validating context. Returning None or True means the value is
            valid, while returning a str message or False means validation
            failed.

        Returns:
            Types: A new types chained with this modifier.
        """
        return Types(self, CanCModifier(checker))

    def canu(self, checker: Callable | Types) -> Types:
        """CanU modifier validates value against the operator object user
        passed in. This modifier is special and doesn't bypass None value. If
        the operator is not present, this modifier fails.

        Args:
            checker (Callable | Types): The checker takes 1 to 4 arguments. The
            first is the operator object, the second is the object being
            operated, the third is the value of the field, the fourth is the
            validating context. Returning None or True means the value is
            valid, while returning a str message or False means validation
            failed.

        Returns:
            Types: A new types chained with this modifier.
        """
        return Types(self, CanUModifier(checker))

    def canw(self, checker: Callable | Types) -> Types:
        """CanW modifier validates value against the operator object user
        passed in. This modifier is special and doesn't bypass None value. If
        the operator is not present, this modifier fails.

        Args:
            checker (Callable | Types): The checker takes 1 to 4 arguments. The
            first is the operator object, the second is the object being
            operated, the third is the value of the field, the fourth is the
            validating context. Returning None or True means the value is
            valid, while returning a str message or False means validation
            failed.

        Returns:
            Types: A new types chained with this modifier.
        """
        return Types(self, CanCModifier(checker), CanUModifier(checker))

    def canr(self, checker: Callable | Types) -> Types:
        """CanR modifier validates value against the operator object user
        passed in. This modifier is special and doesn't bypass None value. If
        the operator is not present, this modifier fails.

        Args:
            checker (Callable | Types): The checker takes 1 to 4 arguments. The
            first is the operator object, the second is the object being
            operated, the third is the value of the field, the fourth is the
            validating context. Returning None or True means the value is
            valid, while returning a str message or False means validation
            failed.

        Returns:
            Types: A new types chained with this modifier.
        """
        return Types(self, CanRModifier(checker))

    # calc pipeline

    @property
    def passin(self: Types) -> Types:
        """Pass in modifier users passin value as the result.
        """
        return Types(self, EagerModifier(), PassinModifier())

    def checkpw(self: Types, against: Types) -> Types:
        """Checkpw modifier uses bcrypt's checkpw function to validate str
        value.
        """
        return Types(self, CheckpwModifier(against))

    def randomdigits(self: Types, length: int | Callable | Types) -> Types:
        """Random digits modifier generates a random digits string of length.
        """
        return Types(self, RandomDigitsModifier(length))

    def randomalnums(self: Types, length: Int | Callable | Types) -> Types:
        """Random alnums modifier generates a random alnums string of length.
        """
        return Types(self, RandomAlnumsModifier(length))

    def randomalnumpuncs(self: Types, length: int | Callable | Types) -> Types:
        """Random alnumpuncs modifier generates a random alnumpuncs string of
        length.
        """
        return Types(self, RandomAlnumpuncsModifier(length))

    def randomint(self: Types, min_value: int | float | Callable | Types,
                    max_value: int | float | Callable | Types) -> Types:
        """Random int modifier generates a random int value."""
        return Types(self, RandomIntModifier(min_value, max_value))

    def randomfloat(self: Types, min_value: int | float | Callable | Types,
                    max_value: int | float | Callable | Types) -> Types:
        """Random float modifier generates a random float value."""
        return Types(self, EagerModifier(), RandomFloatModifier(min_value, max_value))

    def crossfetch(self, cn: str, sk: str, fk: Optional[str] = None) -> Types:
        """Fetch a class with value matches this object's value at key.
        """
        return Types(self, CrossFetchModifier(cn, sk, fk))

    def fval(self: Types, field_name: str | Callable | Types) -> Types:
        """Get value at field from a JSONClass object.
        """
        return Types(self, FValModifier(field_name))

    def eq(self: Types, val: Any | Callable | Types) -> Types:
        """Eq modifier validates value by equal testing.
        """
        return Types(self, EqModifier(val))

    def neq(self: Types, val: Any | Types | Callable) -> Types:
        """Neq modifier validates value by unequal testing.
        """
        return Types(self, NeqModifier(val))

    @property
    def this(self: Types) -> Types:
        """Get the owner object of this field.
        """
        return Types(self, ThisModifier())

    def at(self: Types, index: Any | Callable | Types) -> Types:
        """At modifier returns result with subscription index.
        """
        return Types(self, AtModifier(index))

    def assign(self: Types, name: str, value: Any | Types | Callable) -> Types:
        """Assign value to name of object.
        """
        return Types(self, AssignModifier(name, value))

    @property
    def isthis(self: Types) -> Types:
        """Check whether the current value is the owner object.
        """
        return Types(self, IsThisModifier())

    def oneisvalid(self: Types, subroutines: list[Callable | Types]) -> Types:
        """One is valid is valid if one of subroutines is valid.
        """
        return Types(self, OneIsValidModifier(subroutines))

    def isobj(self: Types, getter: Types) -> Types:
        """Valid if objects are equal.
        """
        return Types(self, IsObjModifier(getter))

    def isobjof(self: Types, cls: type[JObject] | str) -> Types:
        """Valid if the value is object of a class.
        """
        return Types(self, IsObjOfModifier(cls))

    @property
    def getop(self: Types) -> Types:
        """Get the operator of this action.
        """
        return Types(self, GetOpModifier())

    # internal

    def _unresolved(self: Types, arg: Str) -> Types:
        """This modifier marks unresolved status. This is used internally. Do
        not use this.
        """
        return Types(self, UnresolvedModifier(arg))


types = Types()
"""The root of the types modifier. To mark an field with type annotation,
accessor annotation, modifier annotation and transformer annotation, use types
like this:

  @jsonclass
  class MyObject:
    enabled: bool = types.bool.readonly.required
    password: str = types.str.writeonly.length(8, 16).salt.required
"""
