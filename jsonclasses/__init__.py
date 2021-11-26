"""
JSON Classes
~~~~~~~~~~~~

JSON Classes is the Modern Declarative Data Flow and Data Graph Framework for
the AI Empowered Generation.

:copyright: (c) 2020 by Fillmula Inc., Victor Teo

:license: MIT, see LICENSE for more details.
"""
# flake8: noqa: F401
from .jsonclass import jsonclass
from .jsonenum import jsonenum
from .types import types
from .typing import linkto, linkedby, linkedthru
from .encoder import JSONEncoder
from .isjsonclass import isjsonclass, isjsonobject
from .uconf import uconf
