# """
# This module contains `PersistableJSONObject`, the abstract base class for
# interacting with ORMs.
# """
# from __future__ import annotations
# from typing import TypeVar, Union, Optional
# from datetime import datetime
# from .jsonclass import jsonclass
# from .json_object import JSONObject
# from .types import types


# @jsonclass
# class PersistableJSONObject(JSONObject):
#     """This class provides common interface for integrating with ORMs. ORM
#     integration authors should use defined fields of this class to provide an
#     unified interface and usage. Defined fields in this class are id, created_at,
#     and updated_at.
#     """

#     id: Optional[Union[str, int]] = types.oneoftype([str, int]).readonly
#     """The id string of the object. This field is readonly. A user must not set
#     an object's id through web request bodies.
#     """

#     created_at: datetime = types.datetime.readonly.default(datetime.now).required
#     """This field records when this object is created. The value of this field is
#     managed internally thus cannot be updated externally with web request bodies.
#     """

#     updated_at: datetime = types.datetime.readonly.default(datetime.now).required
#     """This field records when this object is last updated. The value of this
#     field is managed internally thus cannot be updated externally with web
#     request bodies.
#     """


# T = TypeVar('T', bound=PersistableJSONObject)
