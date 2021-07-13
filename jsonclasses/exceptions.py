"""This module defines all exceptions that JSON classes uses."""
from __future__ import annotations
from typing import Any
from inspect import getmodule, getsourcelines


class UnlinkableJSONClassException(Exception):
    """This exception is raised when jsonclass objects are linked and no unique
    primary key value is found.
    """

    def __init__(self, class_: type, has_field: bool) -> None:
        """Create an exception that represents an object is not valid for
        putting into object graph, thus cannot be linked.

        Args:
            has_field (bool): Whether this class defined primary field.
            class_ (type): The jsonclass class.
        """
        self.has_field = has_field
        self.class_ = class_
        class_name = class_.__name__
        if not has_field:
            self.message = f"please define a primary field on `{class_name}`"
        else:
            self.message = (f"primary key value not found on `{class_name}` "
                            "object")
        super().__init__(self.message)


class JSONClassRedefinitionException(Exception):
    """This exception is raised when user defines a JSON class with a name that
    exists before in the same graph.
    """

    def __init__(self, new_class: type, exist_class: type) -> None:
        """Create an exception that notifies the user that a class with
        duplicated name is defined twice.

        Args:
            new_class (type): The new class which is putting on the graph.
            exist_class(type): The existing class which the user defined.
        """
        name = new_class.__name__
        original_module = getmodule(exist_class)
        assert original_module is not None
        original_file = original_module.__file__
        original_line = getsourcelines(exist_class)[1]
        new_module = getmodule(new_class)
        assert new_module is not None
        new_file = new_module.__file__
        new_line = getsourcelines(new_class)[1]
        graph = exist_class.definition.config.class_graph
        message = (f'jsonclass name conflict in graph `{graph}`: '
                   f'exist `{name}` defined at '
                   f'`{original_file}:{original_line}`, '
                   f'new `{name}` defined at `{new_file}:{new_line}`')
        super().__init__(message)


class JSONClassTypedDictRedefinitionException(Exception):
    """This exception is raised when user defines a typed dict with a name that
    exists before in the same graph.
    """

    def __init__(self, new_class: type, exist_class: type) -> None:
        """Create an exception that notifies the user that a typed dict class
        with duplicated name is defined twice.

        Args:
            new_class (type): The new class which is putting on the graph.
            exist_class(type): The existing class which the user defined.
        """
        name = new_class.__name__
        original_module = getmodule(exist_class)
        assert original_module is not None
        original_file = original_module.__file__
        original_line = getsourcelines(exist_class)[1]
        new_module = getmodule(new_class)
        assert new_module is not None
        new_file = new_module.__file__
        new_line = getsourcelines(new_class)[1]
        graph = exist_class.definition.config.class_graph
        message = (f'jsonclass typed dict name conflict in graph `{graph}`: '
                   f'exist `{name}` defined at '
                   f'`{original_file}:{original_line}`, '
                   f'new `{name}` defined at `{new_file}:{new_line}`')
        super().__init__(message)


class JSONClassNotFoundException(Exception):
    """This exception is raised when a JSON class with name is not found on a
    graph.
    """
    def __init__(self, class_name: str, graph_name: str):
        message = (f'JSON Class with name \'{class_name}\' in graph '
                   f'\'{graph_name}\' is not found.')
        super().__init__(message)


class JSONClassTypedDictNotFoundException(Exception):
    """This exception is raised when a typed dict with name is not found on a
    graph.
    """
    def __init__(self, class_name: str, graph_name: str):
        message = (f'jsonclass typed dict with name \'{class_name}\' in graph '
                   f'\'{graph_name}\' is not found.')
        super().__init__(message)


class LinkedFieldUnmatchException(Exception):
    """This exception is raised when a JSON class reference field doesn't match
    the counterpart on the other side.
    """
    def __init__(self, class1: str, field1: str, class2: str, field2: str):
        message = (f"unmatched linked field {class1}.{field1} and "
                   f"{class2}.{field2}")
        super().__init__(message)


class ObjectNotFoundException(Exception):
    """ObjectNotFoundException is designed to be raised by jsonclasses ORM
    integration implementations. Server authors and jsonclasses server
    integration authors should catch this to present error to frontend clients.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class UniqueConstraintException(Exception):
    """UniqueConstraintException is designed to be raised by JSON Classes ORM
    integration implementations. When saving objects into the database, if
    object violates the uniqueness rule, this exception should be raised.
    """

    def __init__(self, value: Any, field: str):
        self.field = field
        self.value = value
        self.message = (f'Value \'{value}\' at \'{field}\' is not unique.')
        self.keypath_messages = {
            field: self.message
        }
        super().__init__(self.message)


class ValidationException(Exception):
    """ValidationException is throwed on jsonclass object validation or on
    eager validation. Server authors and jsonclasses server integration authors
    should catch this to present error to frontend clients.
    """

    def __init__(self, keypath_messages: dict[str, str], root: Any):
        self.keypath_messages = keypath_messages
        self.message = self.formatted_keypath_messages()
        self.root = root
        super().__init__(self.message)

    def formatted_keypath_messages(self):
        """The formatted keypath message for print."""
        retval = 'Json classes validation failed:\n'
        for k, v in self.keypath_messages.items():
            retval += f'  \'{k}\': {v}\n'
        return retval


class UnauthorizedActionException(Exception):
    """UnauthorizedActionException is raised when operator checking guards are
    not passed.
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class DeletionDeniedException(Exception):
    """DeletionDeniedException is raised on jsonclass object deletion.
    """

    def __init__(self) -> None:
        self.message = 'deletion denied'
        super().__init__(self.message)


class AbstractJSONClassException(Exception):
    """Abstract class should not be initialized nor serialized into database.
    When an abstract JSON class is initialized, this error should be raised.
    """

    def __init__(self, class_: type) -> None:
        self.class_ = class_
        self.message = (f'{class_.__name__} is an abstract class and should '
                        'not be initialized')
        super().__init__(self.message)


class JSONClassResetError(Exception):
    """This error is raised when an ORM object is new and thus cannot be reset.
    """

    def __init__(self) -> None:
        self.message = 'object is new and cannot be reset'
        super().__init__(self.message)


class JSONClassResetNotEnabledError(Exception):
    """This error is raised when calling reset on an object which class doesn't
    enable `reset_all_fields`.
    """

    def __init__(self) -> None:
        self.message = 'reset called on a reset disabled object'
        super().__init__(self.message)


class JSONClassGraphMergeConflictException(Exception):
    """This exception is raised when there is an object conflict when linking
    jsonclass objects.
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(f'cannot merge graph: {self.message}')
