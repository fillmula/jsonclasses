from datetime import date, datetime, timedelta
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

    dby: Optional[date] = types.date.toboyear
    dtby: Optional[datetime] = types.datetime.toboyear
    sby: Optional[Any] = types.any.toboyear

    dbmth: Optional[date] = types.date.tobomon
    dtbmth: Optional[datetime] = types.datetime.tobomon
    sbmth: Optional[Any] = types.any.tobomon

    dbd: Optional[date] = types.date.toboday
    dtbd: Optional[datetime] = types.datetime.toboday
    sbd: Optional[Any] = types.any.toboday

    dny: Optional[date] = types.date.tonextyear
    dtny: Optional[datetime] = types.datetime.tonextyear
    sny: Optional[Any] = types.any.tonextyear

    dnmth: Optional[date] = types.date.tonextmon
    dtnmth: Optional[datetime] = types.datetime.tonextmon
    snmth: Optional[Any] = types.any.tonextmon

    dnd: Optional[date] = types.date.tonextday
    dtnd: Optional[datetime] = types.datetime.tonextday
    snd: Optional[Any] = types.any.tonextday
