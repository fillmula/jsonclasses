from __future__ import annotations
from jsonclasses.keypath import identical_key
from jsonclasses import jsonclass
from tests.funcs.yet_another_key_transformer import yet_another_key_transformer


@jsonclass(class_graph='simplecompany', input_key_strategy=identical_key,
           output_key_strategy=identical_key,
           strict_input=False,
           ref_name_strategy=yet_another_key_transformer,
           validate_all_fields=True, abstract=True,
           reset_all_fields=True)
class SimpleEmployee:
    name: str
    age: int
