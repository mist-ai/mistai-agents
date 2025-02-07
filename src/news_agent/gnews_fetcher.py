from news_agent.base import NewsFetcher


class GNewsFetcher(NewsFetcher):
    def __init__(self):
        ...

    def fetch(self, keyword: str) -> list:
        """
        Fetches news articles related to a given keyword.

        Args:
            keyword (str): The keyword to search for in news articles.

        Returns:
            List[News]: A list of `News` objects representing the fetched news articles.
        """
        import sys
        import os
        sys.path.append(os.environ["SYS_PATH"])
        from news_agent.base import News
        from googlenewsdecoder import new_decoderv1
        from newspaper import Article
        import time
        import random
        import requests
        from gnews import GNews


        gnews = GNews()
        news_articles = []
        results = gnews.get_news(keyword)

        for i in range(len(results)):
            url = results[i]["url"]
            redirected_url = new_decoderv1(url, 2)

            # Handle case where decoding fails
            if not redirected_url or "decoded_url" not in redirected_url:
                # logger.warning(f"Failed to decode URL: {url}")
                continue  # Skip this article

            decoded_url = redirected_url["decoded_url"]

            # Use requests to fetch the content first
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(decoded_url, headers=headers)

            if response.status_code != 200:
                # logger.warning(f"Failed to fetch article: {decoded_url} (Status: {response.status_code})")
                continue  # Skip this article

            # Use newspaper3k with custom headers
            article = Article(decoded_url, browser_user_agent=headers["User-Agent"])

            try:
                time.sleep(random.uniform(1, 2))
                article.download(input_html=response.text)  # Use pre-fetched HTML
                article.parse()
                results[i]["content"] = article.text

                news = News(
                    title=results[i].get("title", "No Title"),
                    description=results[i].get("description", "No Description"),
                    url=results[i].get("url", "No URL"),
                    date=results[i].get("published date", "No Date"),
                    content=article.text,
                )
                news_articles.append(news)
            except Exception as e:
                # logger.error(f"Error parsing article: {decoded_url} | {str(e)}")
                return e

        return news_articles

gnews_fetcher = GNewsFetcher()