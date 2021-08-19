from __future__ import annotations
from typing import Annotated, TYPE_CHECKING
from jsonclasses import jsonclass, linkedthru
if TYPE_CHECKING:
    from tests.classes.linked_product import LinkedProduct


@jsonclass
class LinkedCustomer:
    name: str
    products: Annotated[list[LinkedProduct], linkedthru('customers')]
