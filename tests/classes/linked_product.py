from __future__ import annotations
from typing import TYPE_CHECKING
from jsonclasses import jsonclass, Link, linkedthru
if TYPE_CHECKING:
    from tests.classes.linked_customer import LinkedCustomer


@jsonclass
class LinkedProduct:
    name: str
    customers: Link[list[LinkedCustomer], linkedthru('products')]
