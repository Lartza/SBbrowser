from datetime import datetime

from timeago import parser as parser
from timeago.excepts import ParameterUnvalid as ParameterUnvalid
from timeago.locales import timeago_template as timeago_template
from timeago.setting import DEFAULT_LOCALE as DEFAULT_LOCALE

__version__: str
__ALL__: list[str]

def total_seconds(dt: datetime) -> float: ...

SEC_ARRAY: list[float]
SEC_ARRAY_LEN: int

def format(date: datetime, now: datetime | None = None, locale: str = "en") -> str: ...
