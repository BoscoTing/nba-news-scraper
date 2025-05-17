from datetime import datetime
from zoneinfo import ZoneInfo


from sqlmodel import Column, Field, SQLModel
from sqlalchemy import DateTime, SmallInteger, VARCHAR
from pydantic import HttpUrl, field_validator

db_timezone = ZoneInfo('UTC')


class StoryBase(SQLModel):
    title: str
    content: str
    published_at: datetime


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
    url: str = Field(
        min_length=23,
        max_length=50,
        sa_column=Column(
            VARCHAR,
            nullable=False,
            unique=True,
        )
    )
    published_at: datetime = Field(
        default=None, 
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            index=True,
        )
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(db_timezone), 
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        )
    )

    @field_validator("url", mode="before")
    def convert_url_to_str(cls, value):
        if isinstance(value, HttpUrl):
            return str(value)
        return value
