import json
from datetime import datetime
from pathlib import Path

from app.config import settings
from app.core.downloader import Downloader
from app.core.parser import StoryParser, IndexParser
from app.core.storage import Storage
from app.core.scraper import Scraper
from app.core.scheduler import scheduler


@scheduler.scheduled_job(
    'interval',
    minutes=1,
    next_run_time=datetime.now(),
)
def main() -> None:
    targets_path = Path(__file__).parent / "core" / "targets" / "story.json"
    story_targets = json.loads(targets_path.read_text())

    targets_path = Path(__file__).parent / "core" / "targets" / "index.json"
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
        index_url=settings.INDEX_URL,
        batch_size=30,
        batch_count=10,
    )


if __name__ == "__main__":
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
