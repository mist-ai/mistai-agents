from .base import NewsFetcher, News
from gnews import GNews
from googlenewsdecoder import new_decoderv1
from newspaper import Article
import time
import random
from utils import logger

class GNewsFetcher(NewsFetcher):
    def __init__(self):
        self.gnews = GNews()

    def fetch(self, keyword: str) -> list:
        """
        Fetches news articles related to a given keyword.

        Args:
            keyword (str): The keyword to search for in news articles.

        Returns:
            List[News]: A list of `News` objects representing the fetched news articles.
        """
        news_articles = []
        results = self.gnews.get_news(keyword)
        for i in range(len(results)):
            url = (results[i]['url'])
            redirected_url = new_decoderv1(url,2)
            article = Article(redirected_url["decoded_url"])
            time.sleep(random.uniform(1, 2)) 
            article.download()
            article.parse()
            results[i]['content'] = article.text

            news = News(
                title=results[i].get("title", "No Title"),
                description=results[i].get("description", "No Description"),
                url=results[i].get("url", "No URL"),
                date=results[i].get("published date", "No Date"),
                content=article.text
                )
            news_articles.append(news)
        return news_articles
    
gnews_fetcher = GNewsFetcher()
