import sys
import os
sys.path.append("/Users/thilakna/Documents/GitHub/mistai-agents/src")
from abc import ABC, abstractmethod
import json

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

class News:
    """
    Represents a news article.

    Attributes:
        title (str): The title of the news article.
        description (str): A brief description of the news article.
        url (str): The URL to the full news article.
        date (str): The publication date of the news article.
        content (str): The content of the news article.
    """
    def __init__(self, title: str, description: str, url: str, date: str, content: str = None):
        self.title = title
        self.description = description
        self.url = url
        self.date = date
        self.content = content

    def to_dict(self):
        """Convert the object to a dictionary."""
        return {
            "title": self.title,
            "description": self.description,
            "date": self.date,
            "content": self.content
        }
    