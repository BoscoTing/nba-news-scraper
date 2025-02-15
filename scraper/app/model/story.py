from datetime import datetime

from sqlmodel import Column, Field, SQLModel
from sqlalchemy import DateTime, SmallInteger
from pydantic import HttpUrl


class StoryBase(SQLModel):
    title: str
    content: str
    publish_at: datetime


class ScrapedStory(StoryBase):
    url: HttpUrl


class Story(ScrapedStory, table=True):
    id: int = Field(
            default=None, 
            sa_column=Column(
                SmallInteger, 
                autoincrement=True, 
                primary_key=True,
                unique=True,
            )
        )
    url: str
    created_at: datetime = Field(
        default=datetime.now(),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
