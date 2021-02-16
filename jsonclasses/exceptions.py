"""JSON Class exceptions."""
from typing import Any, Type


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


class AbstractJSONClassException(Exception):
    """Abstract class should not be initialized nor serialized into database.
    When an abstract JSON class is initialized, this error should be raised.
    """

    def __init__(self, class_: Type) -> None:
        self.class_ = class_
        self.message = (f'{class_.__name__} is an abstract class and should '
                        'not be initialized')
        super().__init__(self.message)
