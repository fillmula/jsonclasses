# from dataclasses import dataclass
# from typing import Optional
# from .reference_map import resolve_class

# @dataclass
# class TypeDefinition():
#   field_type: str # str, int, float, bool, date, datetime, listof, dictof, shape, instanceof
#   storage: str # embedded, linkedby, linkto
#   foreign_key: Optional[str]


# def type_definition(chained_validator: 'ChainedValidator'):

#   StrValidator = resolve_class('StrValidator')
#   IntValidator = resolve_class('IntValidator')
#   FloatValidator = resolve_class('FloatValidator')
#   BoolValidator = resolve_class('BoolValidator')
#   DateValidator = resolve_class('DateValidator')
#   DatetimeValidator = resolve_class('DatetimeValidator')
#   ListOfValidator = resolve_class('ListOfValidator')
#   DictOfValidator = resolve_class('DictOfValidator')
#   ShapeValidator = resolve_class('ShapeValidator')
#   InstanceOfValidator = resolve_class('InstanceOfValidator')
#   IndexValidator = resolve_class('IndexValidator')
#   NullableValidator = resolve_class('NullableValidator')
#   UniqueValidator = resolve_class('UniqueValidator')
#   ReadonlyValidator = resolve_class('ReadonlyValidator')
#   WriteonceValidator = resolve_class('WriteonceValidator')
#   WriteonlyValidator = resolve_class('WriteonlyValidator')
#   RequiredValidator = resolve_class('RequiredValidator')


#   field_type: Optional[str] = None
#   storage: str = 'embedded'
#   foreign_key: Optional[str] = None
#   index: bool = False
#   unique: bool = False
#   read_limitation: str = 'none'
#   write_limitation: str = 'none'
#   collection_nullable: bool = False
#   inner_type_shape: dict = {}
#   inner_type: Any = None

#   validators = chained_validator.validators
#   for validator in validators:
#     if isinstance(validator, StrValidator):
#       field_type = 'str'
#     elif isinstance(validator, IntValidator):
#       field_type = 'int'
#     elif isinstance(validator, FloatValidator):
#       field_type = 'float'
#     elif isinstance(validator, BoolValidator):
#       field_type = 'bool'
#     elif isinstance(validator, DateValidator):
#       field_type = 'date'
#     elif isinstance(validator, DatetimeValidator):
#       field_type = 'datetime'
#     elif isinstance(validator, ListOfValidator):
#       field_type = 'listof'
#     elif isinstance(validator, DictOfValidator):
#       field_type = 'dictof'
#     elif isinstance(validator, ShapeValidator):
#       field_type = 'shape'
#       inner_type_shape = validator.types
#     elif isinstance(validator, InstanceOfValidator):
#       field_type = 'instanceof'
#     elif isinstance(validator, IndexValidator):
#       index = True
#     elif isinstance(validator, UniqueValidator):
#       unique = True
#     elif isinstance(validator, WriteonlyValidator):
#       read_limitation = 'writeonly'
#     elif isinstance(validator, ReadonlyValidator):
#       write_limitation = 'readonly'
#     elif isinstance(validator, WriteonceValidator):
#       write_limitation = 'writeonce'
#     elif isinstance(validator, NullableValidator):
#       collection_nullable = True
