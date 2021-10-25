"""This modules contains `rtypes`, the utility for converting arbitrary types
input into valid types definition.
"""
from __future__ import annotations
from typing import (
    Any, ForwardRef, Union, Annotated, get_args, get_origin, TYPE_CHECKING
)
from datetime import date, datetime
from enum import Enum
from re import match, split
from .excs import UnresolvedTypeNameException
if TYPE_CHECKING:
    from .types import Types
    from .cgraph import CGraph


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
    from .fdef import FType
    if match("^linkto", specifier):
        return types.linkto
    elif match("^linkedby\\('", specifier):
        match_data = match("^linkedby\\('(.+)'\\)", specifier)
        assert match_data is not None
        fk = match_data.group(1)
        if types.fdef._ftype == FType.LIST:
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

def union_split(arg: str) -> list[str]:
    result = ['']
    depth = 0
    for c in arg:
        match c:
            case '[':
                depth += 1
                result[-1] += c
            case ']':
                depth -= 1
                result[-1] += c
            case '|':
                if depth < 1:
                    result.append('')
                else:
                    result[-1] += c
            case _:
                result[-1] += c
    return [r.strip() for r in result]

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

def str_to_types(anytypes: str, opt: bool = False) -> Types:
    """
    Convert user specified string described types to types.

    Args:
        anytypes (str): The user specified string described types.
        jconf (JConf): The configuration of the field's owner class.
        optional (bool): Whether the types is optional.

    Returns:
        Types: A types which describes the field.
    """
    from .types import types
    if anytypes == 'str':
        return types.str if opt else types.str.required
    elif anytypes == 'int':
        return types.int if opt else types.int.required
    elif anytypes == 'float':
        return types.float if opt else types.float.required
    elif anytypes == 'bool':
        return types.bool if opt else types.bool.required
    elif anytypes == 'date':
        return types.date if opt else types.date.required
    elif anytypes == 'datetime':
        return types.datetime if opt else types.datetime.required
    elif anytypes == 'Any':
        return types.any if opt else types.any.required
    else:
        union_args = union_split(anytypes)
        if len(union_args) == 1:
            if anytypes.startswith('Union['):
                match_data = match('^Union\\[(.*)\\]', anytypes)
                assert match_data is not None
                all_item_types = match_data.group(1)
                types_to_build_union = split(", *", all_item_types)
                types_to_build_union = merge_back_dicts(types_to_build_union)
                results = []
                for t in types_to_build_union:
                    results.append(str_to_types(t, True))
                union = types.union(results)
                return union if opt else union.required
            elif anytypes.startswith('Optional['):
                match_data = match('^Optional\\[(.*)\\]', anytypes)
                assert match_data is not None
                item_type = match_data.group(1)
                return str_to_types(item_type, opt=True)
            elif match('^[Ll]ist\\[', anytypes):
                match_data = match('[Ll]ist\\[(.*)\\]', anytypes)
                assert match_data is not None
                item_type = match_data.group(1)
                list_type = types.listof(str_to_types(item_type))
                return list_type if opt else list_type.required
            elif match('^[Dd]ict\\[', anytypes):
                match_data = match('[Dd]ict\\[.+, *(.*)\\]', anytypes)
                assert match_data is not None
                item_type = match_data.group(1)
                dict_type = types.dictof(str_to_types(item_type))
                return dict_type if opt else dict_type.required
            elif anytypes.startswith('Annotated['):
                match_data = match('^(Annotated)\\[(.+), *(.+)\\]', anytypes)
                assert match_data is not None
                instance_type = match_data.group(2)
                link_specifier = match_data.group(3)
                types = str_to_types(instance_type, opt)
                return apply_link_specifier(types, link_specifier)
            else:
                return types._unresolved(anytypes) if opt else types._unresolved(anytypes).required
        else:
            union_results = [r for r in union_args if r != 'None']
            if len(union_args) != len(union_results):
                opt = True
            if len(union_results) == 1:
                return str_to_types(union_results[0], opt)
            else:
                results = []
                for t in union_results:
                    results.append(str_to_types(t, True))
                union = types.union(results)
                return union if opt else union.required


def to_types(anytypes: Any, opt: bool = False) -> Types:
    """
    Convert any types that user specified to types.

    Args:
        anytypes (Any): The user specified any types.
        jconf (JConf): The configuration of the field's owner class.
        opt (bool): Whether the types is optional.

    Returns:
        Types: A types which describes the field.
    """
    from .types import types
    if isinstance(anytypes, str):
        return str_to_types(anytypes)
    elif anytypes is str:
        return types.str if opt else types.str.required
    elif anytypes is int:
        return types.int if opt else types.int.required
    elif anytypes is float:
        return types.float if opt else types.float.required
    elif anytypes is bool:
        return types.bool if opt else types.bool.required
    elif anytypes is date:
        return types.date if opt else types.date.required
    elif anytypes is datetime:
        return types.datetime if opt else types.datetime.required
    elif anytypes is Any:
        return types.any if opt else types.any.required
    elif get_origin(anytypes) is list:
        list_type = types.listof(get_args(anytypes)[0])
        return list_type if opt else list_type.required
    elif get_origin(anytypes) is dict:
        dict_type = types.dictof(get_args(anytypes)[1])
        return dict_type if opt else dict_type.required
    elif get_origin(anytypes) == Union:
        required: bool = True
        types_to_build_union: list[Any] = []
        args = get_args(anytypes)
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
            union = types.union(results)
            return union if not required else union.required
    elif get_origin(anytypes) == Annotated:
        annotated_args = get_args(anytypes)
        len_args = len(annotated_args)
        if len_args != 2:
            raise TypeError(('wrong number of arguments passed to Annotated, '
                            f'expect 2, got {len_args}'))
        types = to_types(annotated_args[0], opt)
        return apply_link_specifier(types, annotated_args[1])
    elif isinstance(anytypes, type) and issubclass(anytypes, Enum):
        enum_type = types.enum(anytypes)
        return enum_type if opt else enum_type.required
    elif hasattr(anytypes, '__is_jsonclass__'):
        instance_type = types.objof(anytypes)
        return instance_type if opt else instance_type.required
    elif isinstance(anytypes, ForwardRef):
        return str_to_types(anytypes.__forward_arg__)
    else:
        raise ValueError(f'{anytypes} is not a valid JSON Class type.')


def rtypes(anytypes: Any) -> Types:
    """
    Get field types from any types that users can specify.

    If the provided `anytypes` is a `Types` object, it itself is returned.
    Otherwise, a synthesized default types is returned.

    Args:
        anytypes (Any): The user specified any types.

    Returns:
        Types: A types which describes the field.
    """
    from .types import Types
    if isinstance(anytypes, Types):
        return anytypes
    return to_types(anytypes)


def rnamedtypes(types: Types, cgraph: CGraph, cname: str) -> Types:
    """
    Resolve unresolved named types after JSONClasses with references are fully
    loaded.

    Args:
        types (Types): The unresolved string name types.

    Returns:
        Types: a types which is fully resolved.
    """
    if not types.fdef._unresolved_name:
        return types
    name = types.fdef._unresolved_name
    if cgraph.has(name):
        cdef = cgraph.fetch(name)
        types = types.objof(cdef.cls)
    elif cgraph.has_enum(name):
        enumcls = cgraph.fetch_enum(name)
        types = types.enum(enumcls)
    else:
        raise UnresolvedTypeNameException(
            f"Unfound type named '{name}' in class '{cname}'.")
    types.fdef._unresolved = False
    types.fdef._unresolved_name = None
    return types
