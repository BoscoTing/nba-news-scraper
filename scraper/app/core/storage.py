from app.model.story import Story, ScrapedStory
from app.core.db import get_db
from app.core.logger import logger
from sqlmodel import select


class Storage:

    def save_stories_batch(
        self,
        scraped_stories: list[ScrapedStory]
    ) -> bool:
        with get_db() as session:
            for scraped_story in scraped_stories:
                story = Story.model_validate(scraped_story)
                
                statement = (
                    select(Story)
                    .where(Story.url == story.url)
                )
                existing_story = session.exec(statement).first()
                
                if existing_story:
                    existing_story.title = story.title
                    existing_story.content = story.content
                    existing_story.published_at = story.published_at
                    logger.debug(f"Updated: {story.title}")
                else:
                    session.add(story)
                    logger.debug(f"Saved: {story.title}")
                
                session.commit()
            return True
