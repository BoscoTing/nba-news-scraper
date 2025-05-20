from datetime import datetime
from unittest.mock import Mock, patch

import pytest
from pydantic import HttpUrl

from app.core.scraper import Scraper
from app.model.index import Index, StoryPreview
from app.model.story import StoryBase, ScrapedStory
from app.core.utils import load_mock_data


class TestScraper:
    @pytest.fixture
    def mock_downloader(self):
        return Mock()

    @pytest.fixture
    def mock_index_parser(self):
        return Mock()

    @pytest.fixture
    def mock_story_parser(self):
        return Mock()

    @pytest.fixture
    def mock_storage(self):
        return Mock()

    @pytest.fixture
    def scraper(self, mock_downloader, mock_index_parser, mock_story_parser, mock_storage):
        return Scraper(
            downloader=mock_downloader,
            index_parser=mock_index_parser,
            story_parser=mock_story_parser,
            storage=mock_storage
        )

    def test_turn_index_page(self, scraper):
        base_url = "https://example.com/nba/news/1"
        result = scraper._turn_index_page(base_url, page=2)
        assert result == "https://example.com/nba/news/2"

        # Test with URL that doesn't have a page number
        base_url = "https://example.com/nba/news"
        result = scraper._turn_index_page(base_url, page=2)
        assert result == "https://example.com/nba/news/2"

    def test_scrape_index(self, scraper):
        mock_content = load_mock_data('sample_index.html')
        mock_index = Index(data=[
            StoryPreview(title="Test Story", url="https://tw-nba.udn.com/nba/story/1")
        ])

        scraper.downloader.download.return_value = mock_content
        scraper.index_parser.parse.return_value = mock_index

        result = scraper.scrape_index("https://example.com/nba/news")

        assert result == mock_index
        scraper.downloader.download.assert_called_once_with("https://example.com/nba/news")
        scraper.index_parser.parse.assert_called_once_with(mock_content)

    def test_scrape_story(self, scraper):
        mock_content = load_mock_data('sample_story.html')
        mock_story = StoryBase(
            title="Test Story",
            published_at=datetime(2024, 3, 20),
            content="Test content"
        )

        scraper.downloader.download.return_value = mock_content
        scraper.story_parser.parse.return_value = mock_story

        result = scraper.scrape_story("https://example.com/nba/story/1")

        assert isinstance(result, ScrapedStory)
        assert result.url == HttpUrl("https://example.com/nba/story/1")
        assert result.title == "Test Story"
        assert result.published_at == datetime(2024, 3, 20)
        assert result.content == "Test content"

        scraper.downloader.download.assert_called_once()
        scraper.story_parser.parse.assert_called_once_with(mock_content)

    def test_scrape_story_parse_failure(self, scraper):
        mock_content = load_mock_data('sample_story.html')
        scraper.downloader.download.return_value = mock_content
        scraper.story_parser.parse.return_value = None

        result = scraper.scrape_story("https://example.com/nba/story/1")

        assert result is None
        scraper.downloader.download.assert_called_once()
        scraper.story_parser.parse.assert_called_once_with(mock_content)

    @patch.object(Scraper, 'scrape_index')
    @patch.object(Scraper, 'scrape_story')
    def test_scrape_stories(self, mock_scrape_story, mock_scrape_index, scraper):
        mock_index = Index(data=[
            StoryPreview(title="Story 1", url="https://tw-nba.udn.com/nba/story/1"),
            StoryPreview(title="Story 2", url="https://tw-nba.udn.com/nba/story/2")
        ])
        mock_scrape_index.return_value = mock_index

        mock_story = StoryBase(
            title="Test Story",
            content="Test content",
            published_at=datetime(2024, 3, 20),
        )
        mock_scrape_story.return_value = ScrapedStory(
            url=HttpUrl("https://example.com/nba/story/1"),
            **mock_story.model_dump()
        )

        scraper.storage.filter_existing_urls.return_value = ([], ["/nba/story/1", "/nba/story/2"])

        scraper.scrape_stories(
            index_url="https://example.com/nba/news",
            batch_size=1,
            batch_count=2
        )

        # Verify storage was called to save stories
        assert scraper.storage.save_stories_batch.call_count == 2
