"""module for fsetonsave modifier."""
from __future__ import annotations
from .setonsave_modifier import SetOnSaveModifier
from ..fdef import Fdef


class FSetOnSaveModifier(SetOnSaveModifier):
    """Force set on save modifier updates or sets value on save regardless of
    modified or not.
    """

    def define(self, fdef: Fdef) -> None:
        fdef._force_set_on_save = True
