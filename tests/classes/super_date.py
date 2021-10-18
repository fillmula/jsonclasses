from datetime import date, datetime
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SuperDate:
    dbd: Optional[date] = types.date.before(date(2020, 4, 3))
    dbdt: Optional[date] = types.date.before(datetime(2020, 4, 3, 0, 0))
    dtbdt: Optional[datetime] = types.datetime.before(datetime(2020, 4, 3, 0, 0))
    dtbd: Optional[datetime] = types.datetime.before(date(2020, 4, 3))

    dad: Optional[date] = types.date.after(date(2020, 4, 3))
    dadt: Optional[date] = types.date.after(datetime(2020, 4, 3, 0, 0))
    dtadt: Optional[datetime] = types.datetime.after(datetime(2020, 4, 3, 0, 0))
    dtad: Optional[datetime] = types.datetime.after(date(2020, 4, 3))

    dbcd: Optional[date] = types.date.before(lambda: date(2020, 4, 3))
    dbtd: Optional[date] = types.date.before(types.default(date(2020, 4, 3)))

    dacd: Optional[date] = types.date.after(lambda: date(2020, 4, 3))
    datd: Optional[date] = types.date.after(types.default(date(2020, 4, 3)))
