"""This modules contains utilities to convert arbitrary type into JSON Class
field types object.
"""
from __future__ import annotations
from typing import (Type, Any, TypeVar, Optional, Union, List, get_args,
                    get_origin, TYPE_CHECKING)
from datetime import date, datetime
from re import match, split
from .graph import get_registered_class
if TYPE_CHECKING:
    from .types import Types
    from .json_object import JSONObject
    T = TypeVar('T', bound=JSONObject)


def str_to_types(argtype: str,
                 graph_sibling: Type[T] = None,
                 optional: bool = False) -> Types:
    """Convert user specified string type to Types object."""
    from .types import types
    if argtype == 'str':
        return types.str if optional else types.str.required
    elif argtype == 'int':
        return types.int if optional else types.int.required
    elif argtype == 'float':
        return types.float if optional else types.float.required
    elif argtype == 'bool':
        return types.bool if optional else types.bool.required
    elif argtype == 'date':
        return types.date if optional else types.date.required
    elif argtype == 'datetime':
        return types.datetime if optional else types.datetime.required
    elif argtype.startswith('Union['):
        match_data = match('Union\\[(.*)\\]', argtype)
        assert match_data is not None
        all_item_types = match_data.group(1)
        types_to_build_union = split(", *", all_item_types)  # TODO: Dict is not supported this way
        results = []
        for t in types_to_build_union:
            results.append(str_to_types(t, graph_sibling, True))
        oneoftype = types.oneoftype(results)
        return oneoftype if optional else oneoftype.required
    elif argtype.startswith('Optional['):
        match_data = match('Optional\\[(.*)\\]', argtype)
        assert match_data is not None
        item_type = match_data.group(1)
        return str_to_types(item_type, graph_sibling, True)
    elif argtype.startswith('List['):
        match_data = match('List\\[(.*)\\]', argtype)
        assert match_data is not None
        item_type = match_data.group(1)
        list_type = types.listof(str_to_types(item_type, graph_sibling))
        return list_type if optional else list_type.required
    elif argtype.startswith('Dict['):
        match_data = match('Dict\\[.+, ?(.*)\\]', argtype)
        assert match_data is not None
        item_type = match_data.group(1)
        dict_type = types.dictof(str_to_types(item_type, graph_sibling))
        return dict_type if optional else dict_type.required
    else:
        instance_type = types.instanceof(
            get_registered_class(argtype, sibling=graph_sibling))
        return instance_type if optional else instance_type.required


def to_types(argtype: Any,
             graph_sibling: Optional[Type[T]] = None,
             optional: bool = False) -> Types:
    """Convert arbitrary user specified type to Types object."""
    from .json_object import JSONObject
    from .types import types
    if isinstance(argtype, str):
        return str_to_types(argtype, graph_sibling)
    elif argtype is str:
        return types.str if optional else types.str.required
    elif argtype is int:
        return types.int if optional else types.int.required
    elif argtype is float:
        return types.float if optional else types.float.required
    elif argtype is bool:
        return types.bool if optional else types.bool.required
    elif argtype is date:
        return types.date if optional else types.date.required
    elif argtype is datetime:
        return types.datetime if optional else types.datetime.required
    elif get_origin(argtype) == Union:
        required: bool = True
        types_to_build_union: List[Any] = []
        args = get_args(argtype)
        for arg in args:
            if type(None) == arg:
                required = False
            else:
                types_to_build_union.append(arg)
        if len(types_to_build_union) == 1:
            return to_types(types_to_build_union[0],
                            graph_sibling,
                            not required)
        else:
            results = []
            for t in types_to_build_union:
                results.append(to_types(t, graph_sibling, True))
            oneoftype = types.oneoftype(results)
            return oneoftype if not required else oneoftype.required
    elif get_origin(argtype) is list:
        list_type = types.listof(get_args(argtype)[0])
        return list_type if optional else list_type.required
    elif get_origin(argtype) is dict:
        dict_type = types.dictof(get_args(argtype)[1])
        return dict_type if optional else dict_type.required
    elif issubclass(argtype, JSONObject):
        instance_type = types.instanceof(argtype)
        return instance_type if optional else instance_type.required
    else:
        raise ValueError(f'{argtype} is not a valid JSON Class type.')


def resolve_types(arbitrary_type: Any, graph_sibling: Type[T] = None) -> Types:
    """Get desired JSON Class field types object from arbitrary types that
    users can specify.

    If the provided `arbitrary_type` is a `Types` object, itself is returned.
    Otherwise, a synthesized default types is returned.

    Returns:
        Types: A Types object dedicated for this provided type expression.
    """
    from .types import Types
    if isinstance(arbitrary_type, Types):
        return arbitrary_type
    return to_types(arbitrary_type, graph_sibling)
