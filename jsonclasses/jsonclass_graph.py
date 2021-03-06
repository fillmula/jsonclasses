"""This module defineds the JSON class mapping graph."""
from __future__ import annotations
from typing import Union, final, TYPE_CHECKING

from .config import Config
from .keypath_utils import reference_key
from .exceptions import (JSONClassRedefinitionException,
                         JSONClassNotFoundException)
if TYPE_CHECKING:
    from .class_definition import ClassDefinition


@final
class JSONClassGraph:
    """JSON classes are defined on class graphs. Classes in the same graph
    share default configurations and can interoperate with each other. A class
    is guaranteed to have a unique name in it's graph. Different graphs serve
    as different naming spaces.
    """

    _graph_map: dict[str, JSONClassGraph] = {}
    """The graph map on which graph objects are stored."""

    _initialized_map: dict[str, bool] = {}
    """The map on which graphs' initialization status are recorded."""

    def __new__(cls: type[JSONClassGraph], name: str) -> JSONClassGraph:
        """The `JSONClassGraph` class returns a shared graph object by it's
        name.
        """
        if not cls._graph_map.get(name):
            cls._graph_map[name] = super(JSONClassGraph, cls).__new__(cls)
        return cls._graph_map.get(name)

    def __init__(self: JSONClassGraph, name: str) -> JSONClassGraph:
        """Find a class graph by it's name. A new one is created if it's not
        exist.

        Args:
            name (str): The name of the graph.
        """
        if self.__class__._initialized_map.get(name):
            return
        self._name: str = name
        self._map: dict[str, ClassDefinition] = {}
        self._default_config = Config(class_graph=self.name,
                                      camelize_json_keys=True,
                                      camelize_db_keys=True,
                                      strict_input=True,
                                      key_transformer=reference_key,
                                      validate_all_fields=False,
                                      soft_delete=False,
                                      abstract=False,
                                      reset_all_fields=False)
        self.__class__._initialized_map[name] = True
        return None

    def __repr__(self) -> str:
        return f'[{self._name}]'

    @property
    def name(self: JSONClassGraph) -> str:
        """The name of this class graph."""
        return self._name

    @property
    def default_config(self: JSONClassGraph) -> Config:
        """The default configuration used on this class graph."""
        return self._default_config

    def put(self: JSONClassGraph, class_definition: ClassDefinition) -> None:
        """Put a class onto this class graph.

        Args:
            class_ (type): The JSON class which will be put onto this graph.

        Raises:
            JSONClassRedefinitionException: This exception is raised if a \
                new class with existing name is defined.
        """
        exist_definition = self._map.get(class_definition.name)
        if exist_definition:
            raise JSONClassRedefinitionException(class_definition.cls,
                                                 exist_definition.cls)
        self._map[class_definition.name] = class_definition

    def fetch(self: JSONClassGraph,
              name_or_class: Union[str, type]) -> ClassDefinition:
        """Fetch a class by it's name from this class graph.

        Args:
            name_or_class (Union[str, type]): The name of the class to be \
                fetched or the class itself.

        Raises:
            JSONClassNotFoundException: This exception is raised if a class \
                definition with `name` is not found.
        """
        if isinstance(name_or_class, type):
            name = name_or_class.__name__
        else:
            name = name_or_class
        try:
            return self._map[name]
        except KeyError:
            raise JSONClassNotFoundException(name, self.name)
