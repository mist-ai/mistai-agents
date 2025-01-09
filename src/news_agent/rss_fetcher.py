import sys
sys.path.append("/Users/thilakna/Documents/GitHub/mistai-agents/src")
import miniflux
from news_agent.base import NewsFetcher, News
import os 
import json

class RSSFetcher(NewsFetcher):
    def __init__(self):
        self.client = miniflux.Client(os.environ['MINIFLUX_BASE_URL'], api_key=os.environ['MINIFLUX_API_KEY'])

    def fetch(self, keyword: str) -> list:
        """
        Fetches news articles related to a given keyword.

            Args:
                keyword (str): The keyword to search for in news articles.

            Returns:
               List[News]: A list of `News` objects representing the fetched news articles.

        """
        entries = self.client.get_entries(search=keyword)
     
        rss_entries = []
        for entry in entries['entries']:
            print(entry)
            title = entry['title']
            url = entry['url']
            date = entry['published_at']
            content = entry['content']
            description="No Description"

            news_article = News(title=title, url=url, date=date, content=content, description=description)
            news_article = news_article.to_dict()

            rss_entries.append(news_article)

        return rss_entries

rss_fetcher = RSSFetcher()
print(rss_fetcher.fetch('hnb'))