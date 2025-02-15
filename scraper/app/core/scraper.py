import time
import random

from app.core.downloader import Downloader
from app.core.parser import StoryParser, IndexParser
from app.core.storage import Storage
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
        time.sleep(random.uniform(0.5, 1.5))
    
    def _turn_index_page(self, base_url: str, page: int = 1) -> list[str]:
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
            for story_preview in story_previews:
                story_urls.add(story_preview.url)

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


if __name__ == "__main__":
    import json
    from pathlib import Path

    targets_path = Path(__file__).parent / "targets" / "story.json"
    story_targets = json.loads(targets_path.read_text())

    targets_path = Path(__file__).parent / "targets" / "index.json"
    index_targets = json.loads(targets_path.read_text())

    downloader = Downloader()
    index_parser = IndexParser(targets=index_targets)
    story_parser = StoryParser(targets=story_targets)
    storage = Storage()
    scraper = Scraper(
        downloader=downloader,
        index_parser=index_parser,
        story_parser=story_parser,
        storage=storage,
    )
    scraper.scrape_stories(
        index_url="https://tw-nba.udn.com/nba/cate/6754/0/newest",
        batch_count=3,
        batch_size=3,
    )
