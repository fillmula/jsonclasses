from __future__ import annotations
from jsonclasses import jsonclass
from tests.funcs.yet_another_key_transformer import yet_another_key_transformer


@jsonclass(class_graph='simplecompany', camelize_json_keys=False,
           strict_input=False, key_transformer=yet_another_key_transformer,
           validate_all_fields=True, soft_delete=True, abstract=True,
           reset_all_fields=True)
class SimpleEmployee:
    name: str
    age: int
