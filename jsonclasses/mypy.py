# pylint: skip-file
"""JSON Class Mypy plugin for type checking JSON Class classes and objects."""
from typing import Optional, Callable, Type as TypingType, Any
from mypy.plugin import Plugin, ClassDefContext
from mypy.options import Options
from mypy.types import AnyType, TypeOfAny
from mypy.nodes import (CallExpr, LambdaExpr, MemberExpr, TempNode, TypeInfo,
                        AssignmentStmt, NameExpr, PlaceholderNode, Var)
from mypy.errorcodes import ErrorCode

JSONOBJECT_FULLNAME = 'jsonclasses.json_object.JSONObject'
TYPES_FULLNAME = 'jsonclasses.types.Types'
JSONCLASS_FULLNAME = 'jsonclasses.jsonclass.jsonclass'

ERROR_UNTYPED = ErrorCode('jsonclass-field', 'Untyped field disallowed', 'JSON Class')
ERROR_MULTIPLE_DEFAULT_VALUES = ErrorCode('jsonclass-field',
                                          'Multiple default values defined',
                                          'JSON Class')


def is_json_class_types_expr(expr: Any) -> bool:
    if isinstance(expr, NameExpr):
        return expr.fullname == 'jsonclasses.types.types'
    if isinstance(expr, MemberExpr):
        return is_json_class_types_expr(expr.expr)
    if isinstance(expr, CallExpr):
        return is_json_class_types_expr(expr.callee)
    return False


def json_class_types_default_arg_expr(expr: Any) -> Any:
    if isinstance(expr, NameExpr):
        return None
    if isinstance(expr, MemberExpr):
        return json_class_types_default_arg_expr(expr.expr)
    if isinstance(expr, CallExpr):
        if isinstance(expr.callee, MemberExpr) and expr.callee.name == 'default':
            return expr.args
        else:
            return json_class_types_default_arg_expr(expr.callee)
    return None


def transform_json_object_subclass(ctx: ClassDefContext) -> None:
    cls = ctx.cls
    for stmt in cls.defs.body:
        if not isinstance(stmt, AssignmentStmt):
            continue
        lhs = stmt.lvalues[0]
        if not isinstance(lhs, NameExpr):
            continue
        if not stmt.new_syntax:
            ctx.api.fail('Untyped fields disallowed in JSON Class body.', stmt, code=ERROR_UNTYPED)
            continue
        sym = cls.info.names.get(lhs.name)
        if sym is None:
            # This name is likely blocked by a star import. We don't need to defer because
            # defer() is already called by mark_incomplete().
            continue
        node = sym.node
        if isinstance(node, PlaceholderNode):
            # This node is not ready yet.
            return None
        assert isinstance(node, Var)
        if node.is_classvar:
            continue
        # node_type = get_proper_type(node.type)
        if is_json_class_types_expr(stmt.rvalue):
            default_expr = json_class_types_default_arg_expr(stmt.rvalue)
            if default_expr:
                if len(default_expr) > 1:
                    ctx.api.fail('Multiple default values defined.',
                                 default_expr[1], code=ERROR_MULTIPLE_DEFAULT_VALUES)
                    stmt.rvalue = TempNode(AnyType(TypeOfAny.explicit), False)
                    continue
                expr = default_expr[0]
                if not (isinstance(expr, LambdaExpr) or isinstance(expr, MemberExpr)):
                    # TODO: check callable return type
                    stmt.rvalue = expr
                else:
                    stmt.rvalue = TempNode(AnyType(TypeOfAny.explicit), False)
            else:
                stmt.rvalue = TempNode(AnyType(TypeOfAny.explicit), False)


class JSONClassesPlugin(Plugin):

    def __init__(self, options: Options) -> None:
        super().__init__(options)

    def get_base_class_hook(self, fullname: str) -> Optional[Callable[[ClassDefContext], None]]:
        sym_table_node = self.lookup_fully_qualified(fullname)
        if sym_table_node and isinstance(sym_table_node.node, TypeInfo):
            if any(instancetype.fullname == JSONOBJECT_FULLNAME for instancetype in sym_table_node.node.mro):
                return transform_json_object_subclass
        return None


def plugin(version: str) -> TypingType[Plugin]:
    """Returns the JSON Class Mypy plugin. The version argument is ignored.
    """
    return JSONClassesPlugin
