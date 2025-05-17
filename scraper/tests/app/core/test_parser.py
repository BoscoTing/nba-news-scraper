from pathlib import Path

import pytest

from app.core.parser import IndexParser
from app.model.index import Index, StoryPreview
from app.core.utils import load_targets


def load_mock_data(filename: str) -> str:
    """Load mock HTML data from the tests/data directory."""
    base_path = Path(__file__).parent.parent.parent / 'data'
    file_path = base_path / filename
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

class TestIndexParser:
    @pytest.fixture
    def parser(self):
        index_targets = load_targets("index.json")
        return IndexParser(targets=index_targets)

    def test_parse_successful(self, parser):
        mock_index_html = load_mock_data('sample_index.html')
        
        result = parser.parse(mock_index_html)
        
        # Basic assertions
        assert result is not None
        assert isinstance(result, Index)
        assert len(result.data) > 0
        
        # Check the structure of the first story preview
        first_story = result.data[0]
        assert isinstance(first_story, StoryPreview)
        assert first_story.title is not None
        assert first_story.url is not None
        assert str(first_story.url).startswith('https://tw-nba.udn.com/nba/story/')

    def test_parse_empty_content(self, parser):
        result = parser.parse("")
        assert isinstance(result, Index)
        assert len(result.data) == 0

    def test_parse_invalid_html(self, parser):
        result = parser.parse("<invalid>html</invalid>")
        assert isinstance(result, Index)
        assert len(result.data) == 0
