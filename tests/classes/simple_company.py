from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass(class_graph='simplecompany')
class SimpleCompany:
    name: str = types.str.length(2, 10).required
    number_of_employees: int = types.int.min(0).required
