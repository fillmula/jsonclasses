"""
This module contains `JSONEncoder`, the encoder class for Python `json` module
that encodes JSON Classes objects.
"""
from typing import Any
from json.encoder import JSONEncoder as PythonDefaultJSONEncoder
from .jsonclass_object import JSONClassObject


class JSONEncoder(PythonDefaultJSONEncoder):
    """The JSONEncoder that works with jsonclasses objects. To dump an json
    encodable object with jsonclasses, use the system default json like this:

      from json import dumps
      from jsonclasses import JSONEncoder

      dumps(obj, cls=JSONEncoder)
    """

    def default(self, o: Any):
        return o.tojson() if hasattr(o.__class__, '__is_jsonclass__') \
            else super().default(o)
