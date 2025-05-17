import time
import random

from app.core.logger import logger
from app.model.index import Index, StoryPreview
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
    
    def _turn_index_page(self, base_url: str, page: int = 1) -> list[str]:
        if base_url.split("/")[-1].isdigit():
            base_url = "/".join(base_url.split("/")[:-1])
        return base_url + "/" + str(page)

    def _process_url_batch(self, story_previews: list[StoryPreview]) -> tuple[set[str], bool]:
        """
        Process a batch of URLs, checking which ones exist in the database.
        Returns a tuple of (new_urls_set, should_stop)
        """
        urls_to_check = [str(preview.url) for preview in story_previews]
        existing_urls, new_urls = self.storage.filter_existing_urls(urls_to_check)
        
        should_stop = len(existing_urls) == len(urls_to_check)
        
        if should_stop:
            logger.info("All URLs in this batch already exist in database. Stopping.")
        else:
            logger.info(f"Found {len(new_urls)} new URLs to process")
        
        return set(new_urls), should_stop

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

    def scrape_stories(
        self,
        index_url: str,
        batch_size: int,
        batch_count: int
    ) -> list[StoryBase]:
        """Scrape multiple urls"""
        current_page = 1
        current_batch = 1
        stories = []
        story_urls = set()

        while current_batch <= batch_count:
            index = self.scrape_index(url=index_url)
            story_previews = index.data
            
            new_urls, should_stop = self._process_url_batch(story_previews)
            
            if should_stop:
                break
                
            story_urls.update(new_urls)

            while story_urls:
                story_url = story_urls.pop()
                story = self.scrape_story(url=story_url)
                logger.debug(f"Scraped: {story_url}, Title: {story.title}")
                logger.debug(f"Batch: {current_batch}, Page: {current_page}, Story count: {len(stories)}")

                if story:
                    stories.append(story)
                if len(stories) >= batch_size:
                    self.storage.save_stories_batch(stories)
                    stories = []
                    current_batch += 1
    
            current_page += 1
            index_url = self._turn_index_page(base_url=index_url, page=current_page)
