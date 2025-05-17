from datetime import datetime

from app.config import settings
from app.core.downloader import Downloader
from app.core.parser import StoryParser, IndexParser
from app.core.storage import Storage
from app.core.scraper import Scraper
from app.core.scheduler import scheduler
from app.core.utils import load_targets

@scheduler.scheduled_job(
    'interval',
    minutes=1,
    next_run_time=datetime.now(),
)
def main() -> None:
    story_targets = load_targets("story.json")
    index_targets = load_targets("index.json")

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
        index_url=settings.INDEX_URL,
        batch_size=30,
        batch_count=10,
    )


if __name__ == "__main__":
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
