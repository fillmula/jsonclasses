from __future__ import annotations
from typing import Annotated, TYPE_CHECKING
from jsonclasses import jsonclass, linkedthru
if TYPE_CHECKING:
    from tests.classes.linked_customer import LinkedCustomer


@jsonclass
class LinkedProduct:
    name: str
    customers: Annotated[list[LinkedCustomer], linkedthru('products')]
