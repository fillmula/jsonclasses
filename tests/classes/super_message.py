from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SuperMessage:
    name: str = types.str.vmsg(types.length(6), "MUST 666").required
