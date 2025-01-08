from abc import ABC, abstractmethod


class NewsFetcher(ABC):
    @abstractmethod
    def fetch(self, keyword: str) -> list:
        """
        Fetch news articles based on a keyword.
        Returns:
            List of news articles (each as a dictionary).
        """
        pass


class Analyzer(ABC):
    @abstractmethod
    def analyze(self, articles: list) -> list:
        """
        Analyze the given list of articles and enrich them with metadata.
        Args:
            articles: A list of articles (each as a dictionary).
        Returns:
            A list of enriched articles with additional metadata (e.g., sentiment).
        """
        pass
