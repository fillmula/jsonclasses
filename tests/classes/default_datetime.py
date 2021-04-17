from datetime import datetime
from jsonclasses import jsonclass, types


@jsonclass
class DefaultDatetime:
    value: datetime = types.datetime.default(datetime(2000, 1, 20))
