from bs4 import BeautifulSoup

from app.model.story import Story
from app.model.index import Index, StoryPreview


class IndexParser:
    """Parse the urls in the index page"""
    def __init__(self, targets: dict[str, str]):
        self.targets = targets
    
    def parse_index(self, content: str):
        soup = BeautifulSoup(content, 'lxml')

        try:
            url_items = soup.select(self.targets['stories'])

            story_previews = []
            for item in url_items:
                preview = StoryPreview(title=item['title'], url = item['href'])
                story_previews.append(preview)
            
            return Index(data=story_previews)

        except Exception as exc:
            print(f"Parse failed: {str(exc)}")
            return None    


class StoryParser:
    """Parse the story page"""
    def __init__(self, targets: dict[str, str]):
        self.targets = targets

    def parse(self, content: str) -> Story | None:
        try:
            soup = BeautifulSoup(content, 'lxml')

            scraped_items = {}
            for key, selector in self.targets.items():
                if key == "content":
                    elements = soup.select(selector)
                    texts = [element.text.strip() if element else None for element in elements]
                    content = "".join(texts)
                    scraped_items[key] = content
                else:
                    element = soup.select_one(selector)
                    scraped_items[key] = element.text.strip() if element else None

            return Story(**scraped_items)

        except Exception as exc:
            print(f"Parse failed: {str(exc)}")
            return None
