from sqlmodel import SQLModel

from app.model.story import Story, ScrapedStory
from app.core.db import get_db
from app.core.logger import logger


class Storage:
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