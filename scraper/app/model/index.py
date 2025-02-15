from sqlmodel import SQLModel
from pydantic import HttpUrl


class StoryPreview(SQLModel):
    title: str
    url: HttpUrl


class Index(SQLModel):
    data: list[StoryPreview]
