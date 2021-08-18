from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass
class DigitProductId:
    product_name: str
    product_id: str = types.str.digit.required

