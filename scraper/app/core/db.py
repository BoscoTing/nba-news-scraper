from collections.abc import Generator
from contextlib import contextmanager

from sqlmodel import Session, create_engine

from app.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

@contextmanager
def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def init_db(session: Session) -> None:
    from sqlmodel import SQLModel
    from app.model.story import Story

    SQLModel.metadata.create_all(engine)
