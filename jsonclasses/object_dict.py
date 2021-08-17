"""The dot notation accessible dict."""
from __future__ import annotations
from typing import Any
from .owned_dict import OwnedDict


class ObjectDict(OwnedDict):

    def __getattr__(self, name):
        try:
            return super().__getattr__(name)
        except Exception:
            return self[name]

    def __setattr__(self, name: str, value: Any) -> None:
        if name in self.keys():
            self[name] = value
        else:
            super().__setattr__(name, value)
