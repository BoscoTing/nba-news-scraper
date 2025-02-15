from datetime import datetime
from sqlmodel import SQLModel


class Story(SQLModel):
    title: str
    content: str
    publish_at: datetime
