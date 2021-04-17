from datetime import date
from jsonclasses import jsonclass, types


@jsonclass
class DefaultDate:
    value: date = types.datetime.default(date(2000, 1, 20))
