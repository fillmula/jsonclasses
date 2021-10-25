from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass(class_graph='grouptemplate')
class Group:
    id: int = types.int.primary
    name: str
    template: Template = types.objof('Template').linkedby('group').present


@jsonclass(class_graph='grouptemplate')
class Template:
    id: int = types.int.primary
    name: str
    group: Group = types.linkto.objof('Group').required
