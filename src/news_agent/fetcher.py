from .base import NewsFetcher
from gnews import GNews
from googlenewsdecoder import new_decoderv1
from newspaper import Article
import time
import random

class GNewsFetcher(NewsFetcher):
    def __init__(self):
        self.gnews = GNews()

    def fetch(self, keyword: str) -> list:
        """
        Fetches news articles related to a given keyword.

        Args:
            keyword (str): The keyword to search for in news articles.

        Returns:
            List[Dict[str, str]]: 
                A list of dictionaries where each dictionary represents a news article with the following keys:
                    - "title" (str): The title of the news article.
                    - "description" (str): A brief description of the news article.
                    - "url" (str): The URL to the full news article.
                    - "date" (str): The publication date of the news article.
                    - "content" (str): The content of the news article

        """
        results = self.gnews.get_news(keyword)
        print(results)
        for i in range(len(results)):

            url = (results[i]['url'])
            redirected_url = new_decoderv1(url,2)
            article = Article(redirected_url["decoded_url"])

            time.sleep(random.uniform(1, 2)) 

            article.download()
            article.parse()
            results[i]['content'] = article.text
            

        # return results
    


a = GNewsFetcher()
a.fetch('sri lanka')
