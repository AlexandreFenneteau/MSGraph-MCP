from datetime import timedelta
from typing import Optional
import httpx
import sys
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Add the src directory to Python path to enable absolute imports
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from msgraph_mcp.mg.calendar import get_events
from msgraph_mcp.models import CalEvent, MailInfo
from msgraph_mcp.mg.mail import search_email_addresses, search_mails
from msgraph_mcp.utils import get_local_datetime_str, get_next_day, get_now_dt

USER_AGENT = "msgraph_mcp"

mcp = FastMCP(
    name=USER_AGENT,
    # host="localhost",
    # port=8182,
    # streamable_http_path="/mcp",
    # sse_path="/sse",
)

@mcp.tool()
async def get_current_datetime() -> str:
    """Get the current local date and time."""
    return get_local_datetime_str()

@mcp.tool()
async def get_calendar_events_by_date_range(
    start_year: int,
    start_month: int,
    start_day: int,
    end_year: int,
    end_month: int,
    end_day: int
    ) -> list[CalEvent]:
    """Get calendar events between two specific dates."""
    events = await get_events(start_year, start_month, start_day,
                     end_year, end_month, end_day)
    return events

@mcp.tool()
async def get_upcoming_week_calendar_events() -> list[CalEvent]:
    """Get all calendar events for the upcoming week (Monday to Sunday)."""
    next_monday = get_next_day(0)
    next_next_monday = next_monday + timedelta(days=7)
    events = await get_events(next_monday.year, next_monday.month, next_monday.day,
                              next_next_monday.year, next_next_monday.month, next_next_monday.day)
    return events

@mcp.tool()
async def search_email_messages(search_term: str, n_emails: Optional[int] = 5) -> list[MailInfo]:
    """Search for emails matching a search term and return email details."""
    mails = await search_mails(search_value=search_term, top=n_emails)
    return mails

@mcp.tool()
async def extract_email_addresses_from_search(search_term: str, n_searched_messages: Optional[int] = 3) -> list[str]:
    """Extract email addresses from emails matching a search term."""
    mail_addresses = await search_email_addresses(search_value=search_term, top_mails=n_searched_messages)
    return mail_addresses

@mcp.prompt()
async def greet_user(name: str) -> str:
    return f"Make an AIKU with the initials of {name.upper()}"


if __name__ == "__main__":
    # mcp.run(transport="streamable-http")
    # mcp.run(transport="sse")
    mcp.run(transport="stdio")