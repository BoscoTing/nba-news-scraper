import requests
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
from fake_useragent import UserAgent

from app.core.logger import logger


class Downloader:
    def __init__(self):
        self.user_agent = UserAgent()

    def _get_headers(self) -> dict[str, str]:
        return {
            'User-Agent': self.user_agent.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        }

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(requests.exceptions.RequestException),
        reraise=True,
    )
    def download(self, url: str) -> str | None:
        return requests.get(url, headers=self._get_headers()).text


if __name__ == "__main__":
    downloader = Downloader()
    text = downloader.download(url="https://tw-nba.udn.com/nba/story/7002/8549781")
    print(text)
