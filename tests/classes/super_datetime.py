from datetime import datetime, timedelta
from typing import Any, Optional
from jsonclasses import jsonclass, types

@jsonclass
class SuperDateTime:
    dtbs: Optional[datetime] = types.datetime.tobosec
    stbs: Optional[Any] = types.any.tobosec

    dtbm: Optional[datetime] = types.datetime.tobomin
    stbm: Optional[Any] = types.any.tobomin

    dtbh: Optional[datetime] = types.datetime.tobohour
    stbh: Optional[Any] = types.any.tobohour

    dtns: Optional[datetime] = types.datetime.tonextsec
    stns: Optional[Any] = types.any.tonextsec

    dtnm: Optional[datetime] = types.datetime.tonextmin
    stnm: Optional[Any] = types.any.tonextmin

    dtnh: Optional[datetime] = types.datetime.tonexthour
    stnh: Optional[Any] = types.any.tonexthour
