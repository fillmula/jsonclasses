from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass
class AlphaAnalysis:
    product_name: str = types.str.alpha.required

