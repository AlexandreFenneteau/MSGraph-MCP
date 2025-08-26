from datetime import datetime, date
from typing import Union
from pydantic import BaseModel

class CalEvent(BaseModel):
    subject: str
    organizer_email: str
    start: datetime
    end: datetime
    is_all_day: bool


class MailInfo(BaseModel):
    from_address: str
    subject: str
    send_date_time: datetime
    body: str
    id: str
