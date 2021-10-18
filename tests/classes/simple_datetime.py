from __future__ import annotations
from datetime import date, datetime
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SimpleDatetime:
    fmtdt: Optional[datetime] = types.datetime.fmtd("%Y年%m月%d日 %H:%M:%S")
    fmtd: Optional[date] = types.date.fmtd("%Y年%m月%d日")
    fmtdts: Optional[str] = types.str.fmtd("%Y年%m月%d日 %H:%M:%S")
    fmtds: Optional[str] = types.str.fmtd("%Y年%m月%d日")

    cfmtdt: Optional[datetime] = types.datetime.fmtd(lambda: "%Y年%m月%d日 %H:%M:%S")
    tfmtdt: Optional[datetime] = types.datetime.fmtd(types.default("%Y年%m月%d日 %H:%M:%S"))
