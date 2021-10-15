from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SuperPermissionUser:
    id: int = types.int.primary.required
    code: int = types.int.required
    articles: list[SuperPermissionArticle] = types.listof('SuperPermissionArticle').linkedby('user')


@jsonclass
class SuperPermissionArticle:
    id: int = types.int.primary.required
    code: int = types.int.required
    user: SuperPermissionUser = types.objof('SuperPermissionUser').linkto
    title: str = types.str.canc(types.getop.fval('code').eq(types.this.fval('code'))).required
    content: str = types.str.canr(types.getop.fval('code').eq(types.this.fval('code'))).required
    content2: Optional[str] = types.str.canu(types.getop.isobj(types.this.fval('user')))
