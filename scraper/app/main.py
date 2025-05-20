from datetime import datetime, date
import argparse

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
def main(specified_date: date | None = None) -> None:
    BATCH_SIZE = 30
    BATCH_COUNT = 10

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
        batch_size=BATCH_SIZE,
        batch_count=BATCH_COUNT,
        specified_date=specified_date,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the scraper with optional date parameter')
    parser.add_argument('--no-date', action='store_true', help='Run without specifying a date')
    args = parser.parse_args()
    
    try:
        if args.no_date:
            main()
        else:
            main(specified_date=date.today())
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
