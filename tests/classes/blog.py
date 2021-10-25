from __future__ import annotations
from typing import Optional
from datetime import datetime
from jsonclasses import jsonclass, types


@jsonclass(class_graph='blog')
class User:
    id: int = types.int.primary.required
    name: str
    posts: list[Post] = types.nonnull.listof('Post').linkedby('user').required
    comments: list[Comment] = types.listof('Comment').linkedby('commenter') \
                                   .required
    updated_at: datetime = types.datetime.tsupdated.required


@jsonclass(class_graph='blog')
class Post:
    id: int = types.int.primary.required
    name: str
    user: User = types.linkto.objof('User').required
    comments: list[Comment] = types.listof('Comment').linkedby('post').required
    updated_at: datetime = types.datetime.tsupdated.required



@jsonclass(class_graph='blog')
class Comment:
    id: int = types.int.primary.required
    content: str
    post: Post = types.linkto.objof('Post').required
    parent: Optional[Comment] = types.linkto.objof('Comment')
    children: list[Comment] = types.listof('Comment').linkedby('parent') \
                                   .required
    commenter: User = types.linkto.objof('User').required
    updated_at: datetime = types.datetime.tsupdated.required
