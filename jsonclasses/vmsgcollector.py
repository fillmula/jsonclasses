from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .jobject import JObject


class VMsgCollector:

    def __init__(self: VMsgCollector) -> None:
        self.msgs: dict[str, str] = {}

    def receive(self: VMsgCollector, msgs: dict[str, str]) -> None:
        self.msgs.update(msgs)

    @property
    def messages(self: VMsgCollector) -> dict[str, str]:
        return self.msgs

    @property
    def has_msgs(self: VMsgCollector) -> bool:
        return len(self.msgs) > 0
