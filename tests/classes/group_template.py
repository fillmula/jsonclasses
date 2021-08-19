from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass(cgraph='grouptemplate')
class Group:
    id: int = types.int.primary
    name: str
    template: Template = types.instanceof('Template').linkedby('group').present


@jsonclass(cgraph='grouptemplate')
class Template:
    id: int = types.int.primary
    name: str
    group: Group = types.linkto.instanceof('Group').required
