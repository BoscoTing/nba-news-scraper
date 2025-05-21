import time
import random
from datetime import date
from app.core.logger import logger
from app.model.index import Index
from app.model.story import StoryBase, ScrapedStory


class Scraper:
    def __init__(
        self,
        downloader,
        index_parser,
        story_parser,
        storage,
    ):
        self.downloader = downloader
        self.index_parser = index_parser
        self.story_parser = story_parser
        self.storage = storage

    def _sleep_randomly(self) -> None:
        time.sleep(random.uniform(0.1, 0.5))
    
    def _turn_index_page(self, base_url: str, page: int = 1) -> str:
        if base_url.split("/")[-1].isdigit():
            base_url = "/".join(base_url.split("/")[:-1])
        return base_url + "/" + str(page)

    def scrape_index(self, url: str) -> Index:
        content = self.downloader.download(url)
        index = self.index_parser.parse(content)
        return index

    def scrape_story(self, url: str) -> ScrapedStory | None:
        """Scrape a single story url"""
        self._sleep_randomly()
        content = self.downloader.download(url)
        story = self.story_parser.parse(content)
        if story:
            scraped_story = ScrapedStory(
                url=url,
                **story.model_dump(),
            )
            return scraped_story
        return None
    
    def _stop_at_date(self, stories: list[StoryBase], specified_date: date) -> bool:
        return all(story.published_at.date() < specified_date for story in stories)

    def scrape_stories(
        self,
        index_url: str,
        batch_size: int,
        batch_count: int,
        specified_date: date | None = None,
    ) -> None:
        """Scrape multiple urls"""
        current_page = 1
        current_batch = 1
        stories = []
        story_urls = set()

        while current_batch <= batch_count:
            index = self.scrape_index(url=index_url)
            story_previews = index.data

            for story_preview in story_previews:
                story_urls.add(story_preview.url)

            while story_urls:
                story_url = story_urls.pop()
                story = self.scrape_story(url=story_url)

                if story:
                    logger.debug(f"Scraped: {story_url}, Title: {story.title}")
                    logger.debug(f"Batch: {current_batch}, Page: {current_page}, Story count: {len(stories)}")
                    stories.append(story)


                if len(stories) >= batch_size:
                    self.storage.save_stories_batch(stories)
                    stories = []
                    current_batch += 1

            if specified_date and self._stop_at_date(stories=stories, specified_date=specified_date):
                logger.info("All stories before the specified date have been scraped. Stopping.")
                break
    
            current_page += 1
            index_url = self._turn_index_page(base_url=index_url, page=current_page)
            story_urls = set()  
