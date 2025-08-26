from datetime import datetime

from ..utils import format_msgraph_date, format_msgraph_datetime
from .client import GRAPH_CLIENT
from ..models import CalEvent

async def get_events(start_year: int, start_month: int, start_day: int,
                     end_year: int, end_month: int, end_day: int) -> list[CalEvent]:
    """
    Retrieve calendar events within a specified date range.
    
    This function queries Microsoft Graph API to fetch calendar events from the user's
    primary calendar within the specified date range. Only non-cancelled events are
    returned. The function handles both all-day events and timed events, formatting
    their dates/times appropriately.
    
    Args:
        start_year (int): The year of the start date (e.g., 2025)
        start_month (int): The month of the start date (1-12)
        start_day (int): The day of the start date (1-31)
        end_year (int): The year of the end date (e.g., 2025)
        end_month (int): The month of the end date (1-12)
        end_day (int): The day of the end date (1-31)
    
    Returns:
        list[CalEvent]: A list of CalEvent objects containing event details including:
                       - subject: Event title/subject
                       - organizer_email: Email address of the event organizer
                       - is_all_day: Boolean indicating if it's an all-day event
                       - start: Event start time (formatted as date for all-day, datetime for timed)
                       - end: Event end time (formatted as date for all-day, datetime for timed)
    
    Example:
        >>> # Get events for the first week of September 2025
        >>> events = await get_events(2025, 9, 1, 2025, 9, 7)
        >>> print(f"Found {len(events)} events")
        >>> for event in events:
        ...     print(f"{event.subject} - {event.start}")
    
    Note:
        - Cancelled events are automatically filtered out
        - All-day events use date formatting, timed events use datetime formatting
        - The date range is inclusive of both start and end dates
    """
    cal_view = GRAPH_CLIENT.me.calendar_view
    cal_events = await cal_view.get(
        cal_view.CalendarViewRequestBuilderGetRequestConfiguration(
            query_parameters=cal_view.CalendarViewRequestBuilderGetQueryParameters(
                start_date_time=datetime(start_year, start_month, start_day).isoformat(),
                end_date_time=datetime(end_year, end_month, end_day).isoformat(),
            )
        )
    )

    events = []
    for graph_event in cal_events.value:
        if not graph_event.is_cancelled:
            events.append(
                CalEvent(
                    subject=graph_event.subject,
                    organizer_email=graph_event.organizer.email_address.address,
                    is_all_day=graph_event.is_all_day,
                    start=format_msgraph_date(graph_event.start) if graph_event.is_all_day else format_msgraph_datetime(graph_event.start),
                    end=format_msgraph_date(graph_event.end) if graph_event.is_all_day else format_msgraph_datetime(graph_event.end)
                )
            )
    return events