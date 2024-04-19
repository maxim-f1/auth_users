import datetime


DATE_FORMAT: str = '%d-%m-%Y'
TIME_FORMAT: str = '%H:%M:%S'
FULL_FORMAT: str = '%d-%m-%YT%H:%M:%S'


def get_now_with_delta(
        days: int | float = 0,
        seconds: int | float = 0,
        microseconds: int | float = 0,
        milliseconds: int | float = 0,
        minutes: int | float = 0,
        hours: int | float = 0,
        weeks: int | float = 0,
        is_date: bool = False,
) -> datetime.date | datetime.datetime:
    delta = datetime.timedelta(
        days=days,
        seconds=seconds,
        microseconds=microseconds,
        milliseconds=milliseconds,
        minutes=minutes,
        hours=hours,
        weeks=weeks
    )
    if is_date:
        return (datetime.datetime.now(datetime.UTC) + delta).date()
    return datetime.datetime.strptime(
        (datetime.datetime.now(datetime.UTC) + delta).strftime(FULL_FORMAT), FULL_FORMAT
    )
