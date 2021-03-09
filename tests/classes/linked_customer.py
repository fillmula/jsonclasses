from __future__ import annotations
from typing import TYPE_CHECKING
from jsonclasses import jsonclass, Link, linkedthru
if TYPE_CHECKING:
    from tests.classes.linked_product import LinkedProduct


@jsonclass
class LinkedCustomer:
    name: str
    products: Link[list[LinkedProduct], linkedthru('customers')]
