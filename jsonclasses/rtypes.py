"""This modules contains `TypesResolver`, the types definition normalizer and
auto synthenizer. This is used for figuring out a JSON class field's types
definition.
"""
from __future__ import annotations
from typing import (
    Any, ForwardRef, Union, Annotated, get_args, get_origin, TYPE_CHECKING
)
from datetime import date, datetime
from enum import Enum
from re import match, split
if TYPE_CHECKING:
    from .types import Types


def apply_link_specifier(types: Types, specifier: str) -> Types:
    """
    This method completes custom annotated linked fields into types.

    Args:
        types (Types): The original types.
        specifier (str): The string specifier which specifies link \
            relationship.

    Returns:
        Types: The types with link specifier applied.
    """
    from .fdef import FieldType
    if match("^linkto", specifier):
        return types.linkto
    elif match("^linkedby\\('", specifier):
        match_data = match("^linkedby\\('(.+)'\\)", specifier)
        assert match_data is not None
        fk = match_data.group(1)
        if types.fdef.field_type == FieldType.LIST:
            return types.nonnull.linkedby(fk)
        else:
            return types.linkedby(fk)
    elif match("^linkedthru\\('", specifier):
        match_data = match("^linkedthru\\('(.+)'\\)", specifier)
        assert match_data is not None
        fk = match_data.group(1)
        return types.nonnull.linkedthru(fk)
    else:
        raise TypeError(f"wrong format of link specifier '{specifier}'")

def merge_back_dicts(args: list[str]) -> list[str]:
    """This method is used for union arguments parsing. When union contains
    dict, dict is separated wrongly by split method. This function merge
    dicts back.

    Args:
        args (list[str]): A list of string tokens.

    Returns:
        list[str]: The renovated string tokens.
    """
    retval = []
    do_not_push_next = False
    for idx, arg in enumerate(args):
        if do_not_push_next:
            do_not_push_next = False
            continue
        if match('^[Dd]ict\\[', arg):
            retval.append(arg + ', ' + args[idx + 1])
            do_not_push_next = True
        else:
            retval.append(arg)
    return retval

def str_to_types(any_types: str, opt: bool = False) -> Types:
    """
    Convert user specified string described types to types.

    Args:
        any_types (str): The user specified string described types.
        jconf (JConf): The configuration of the field's owner class.
        optional (bool): Whether the types is optional.

    Returns:
        Types: A types which describes the field.
    """
    from .types import types
    if any_types == 'str':
        return types.str if opt else types.str.required
    elif any_types == 'int':
        return types.int if opt else types.int.required
    elif any_types == 'float':
        return types.float if opt else types.float.required
    elif any_types == 'bool':
        return types.bool if opt else types.bool.required
    elif any_types == 'date':
        return types.date if opt else types.date.required
    elif any_types == 'datetime':
        return types.datetime if opt else types.datetime.required
    elif any_types.startswith('Union['):
        match_data = match('Union\\[(.*)\\]', any_types)
        assert match_data is not None
        all_item_types = match_data.group(1)
        types_to_build_union = split(", *", all_item_types)
        types_to_build_union = merge_back_dicts(types_to_build_union)
        results = []
        for t in types_to_build_union:
            results.append(str_to_types(t, True))
        oneoftype = types.oneoftype(results)
        return oneoftype if opt else oneoftype.required
    elif any_types.startswith('Optional['):
        match_data = match('Optional\\[(.*)\\]', any_types)
        assert match_data is not None
        item_type = match_data.group(1)
        return str_to_types(item_type, True)
    elif match('[Ll]ist\\[', any_types):
        match_data = match('[Ll]ist\\[(.*)\\]', any_types)
        assert match_data is not None
        item_type = match_data.group(1)
        list_type = types.listof(str_to_types(item_type))
        return list_type if opt else list_type.required
    elif match('[Dd]ict\\[', any_types):
        match_data = match('[Dd]ict\\[.+, *(.*)\\]', any_types)
        assert match_data is not None
        item_type = match_data.group(1)
        dict_type = types.dictof(str_to_types(item_type))
        return dict_type if opt else dict_type.required
    elif any_types.startswith('Annotated['):
        match_data = match('(Annotated)\\[(.+), *(.+)\\]', any_types)
        assert match_data is not None
        instance_type = match_data.group(2)
        link_specifier = match_data.group(3)
        types = str_to_types(instance_type, opt)
        return apply_link_specifier(types, link_specifier)
    else:
        return types._unresolved(any_types)
        # graph = jconf.cgraph
        # if graph.has(any_types):
        #     definition = graph.fetch(any_types)
        #     instance_type = types.instanceof(definition.cls)
        #     return instance_type if opt else instance_type.required
        # elif graph.has_dict(any_types):
        #     dict_cls = graph.fetch_dict(any_types)
        #     shape_type = types.nonnull.shape(dict_cls)
        #     return shape_type if opt else shape_type.required
        # elif graph.has_enum(any_types):
        #     enum_cls = graph.fetch_enum(any_types)
        #     type = types.enum(enum_cls)
        #     return type if opt else type.required
        # elif isinstance(any_types, str):
        #     instance_type = types.instanceof(any_types)
        #     return instance_type if opt else instance_type.required

def to_types(any_types: Any, opt: bool = False) -> Types:
    """
    Convert any types that user specified to types.

    Args:
        any_types (Any): The user specified any types.
        jconf (JConf): The configuration of the field's owner class.
        opt (bool): Whether the types is optional.

    Returns:
        Types: A types which describes the field.
    """
    from .types import types
    if isinstance(any_types, str):
        return str_to_types(any_types)
    elif any_types is str:
        return types.str if opt else types.str.required
    elif any_types is int:
        return types.int if opt else types.int.required
    elif any_types is float:
        return types.float if opt else types.float.required
    elif any_types is bool:
        return types.bool if opt else types.bool.required
    elif any_types is date:
        return types.date if opt else types.date.required
    elif any_types is datetime:
        return types.datetime if opt else types.datetime.required
    elif get_origin(any_types) is list:
        list_type = types.listof(get_args(any_types)[0])
        return list_type if opt else list_type.required
    elif get_origin(any_types) is dict:
        dict_type = types.dictof(get_args(any_types)[1])
        return dict_type if opt else dict_type.required
    elif get_origin(any_types) == Union:
        required: bool = True
        types_to_build_union: list[Any] = []
        args = get_args(any_types)
        for arg in args:
            if type(None) == arg:
                required = False
            else:
                types_to_build_union.append(arg)
        if len(types_to_build_union) == 1:
            return to_types(types_to_build_union[0], not required)
        else:
            results = []
            for t in types_to_build_union:
                results.append(to_types(t, True))
            oneoftype = types.oneoftype(results)
            return oneoftype if not required else oneoftype.required
    elif get_origin(any_types) == Annotated:
        annotated_args = get_args(any_types)
        len_args = len(annotated_args)
        if len_args != 2:
            raise TypeError(('wrong number of arguments passed to Link, '
                            f'expect 2, got {len_args}'))
        types = to_types(annotated_args[0], opt)
        return apply_link_specifier(types, annotated_args[1])
    elif isinstance(any_types, type) and issubclass(any_types, dict):
        anno_dict: dict[str, Any] = any_types.__annotations__
        item_types: dict[str, Types] = {}
        for k, t in anno_dict.items():
            item_types[k] = to_types(t)
        raw_shape_types = types.nonnull.shape(item_types)
        return raw_shape_types if opt else raw_shape_types.required
    elif isinstance(any_types, type) and issubclass(any_types, Enum):
        enum_type = types.enum(any_types)
        return enum_type if opt else enum_type.required
    elif hasattr(any_types, '__is_jsonclass__'):
        instance_type = types.instanceof(any_types)
        return instance_type if opt else instance_type.required
    elif isinstance(any_types, ForwardRef):
        return str_to_types(any_types.__forward_arg__)
    else:
        raise ValueError(f'{any_types} is not a valid JSON Class type.')


def rtypes(anytypes: Any) -> Types:
    """
    Get field types from any types that users can specify.

    If the provided `anytypes` is a `Types` object, it itself is returned.
    Otherwise, a synthesized default types is returned.

    Args:
        anytypes (Any): The user specified any types.
        anyowner (Any): The configuration of the field's owner class.

    Returns:
        Types: A types which describes the field.
    """
    from .types import Types
    if isinstance(anytypes, Types):
        return anytypes
    return to_types(anytypes)
