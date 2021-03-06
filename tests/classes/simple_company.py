from __future__ import annotations
from jsonclasses import jsonclass


@jsonclass(class_graph='simplecompany')
class SimpleCompany:
    name: str
    number_of_employees: int
