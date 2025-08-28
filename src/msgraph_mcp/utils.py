from datetime import datetime, timedelta
from msgraph.generated.models.date_time_time_zone import DateTimeTimeZone
from zoneinfo import ZoneInfo

from msgraph_mcp.config import DATE_TIME_SETTINGS


TIMEZONE = ZoneInfo(DATE_TIME_SETTINGS.timezone)


def format_msgraph_datetime(msgraph_datetime: DateTimeTimeZone) -> str:
    assert msgraph_datetime.time_zone == 'UTC'
    dt = datetime.fromisoformat(msgraph_datetime.date_time + 'Z') # Add the Z to allow datetime to parse the date as UTC + 00
    return dt.astimezone(TIMEZONE)


def format_msgraph_date(msgraph_datetime: DateTimeTimeZone) -> str:
    assert msgraph_datetime.time_zone == 'UTC'
    dt = datetime.fromisoformat(msgraph_datetime.date_time + 'Z') # Add the Z to allow datetime to parse the date as UTC + 00
    return dt

def get_now_dt() -> datetime:
    return datetime.now(tz=TIMEZONE)

def get_local_datetime_str() -> str:
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    now = get_now_dt()
    now_isocal = now.isocalendar()
    return f"Weekday: {weekdays[now_isocal.weekday]}, Year: {now.year}, Month: {now.month}, Week number: {now_isocal.week}, Day: {now.day}, Hour: {now.hour}, Minute: {now.minute}"


def get_next_day(weekday: int) -> datetime:
    """Weekday: 0 -> monday, 6 -> sunday"""
    now = get_now_dt()
    days_difference = 7 - ((now.weekday() - weekday) % 7 )
    next_day_date = now.date() + timedelta(days=days_difference)

    return datetime(next_day_date.year, next_day_date.month, next_day_date.day)