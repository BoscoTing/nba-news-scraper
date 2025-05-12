from sqlmodel import SQLModel, select

from app.model.story import Story, ScrapedStory
from app.core.db import get_db
from app.core.logger import logger


class Storage:
    def filter_existing_urls(self, urls: list[str]) -> tuple[list[str], list[str]]:
        """
        Check which URLs exist in database and return both existing and new URLs.
        Returns a tuple of (existing_urls, new_urls)
        """
        with get_db() as session:
            statement = (
                select(Story.url)
                .where(Story.url.in_(urls))
            )
            existing_urls = session.exec(statement).all()

            new_urls = [u for u in urls if u not in existing_urls]
            return existing_urls, new_urls

    def save_stories_batch(
        self,
        scraped_stories: list[ScrapedStory]
    ) -> bool:
        with get_db() as session:
            for scraped_story in scraped_stories:
                story = Story.model_validate(scraped_story)

                session.add(story)
                session.commit()

                logger.debug(f"Saved: {story.title}")
            return True
