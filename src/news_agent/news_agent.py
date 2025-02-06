import os
import sys
from letta import LocalClient, RESTClient, ChatMemory
from utils import logger
from config import EMBEDDING_CONFIG, LLM_CONFIG
from news_agent.constants import NAME, PERSONA_PROMPT, HUMAN_PROMPT


class NewsAgent:
    def __init__(self, client: LocalClient | RESTClient):
        self.client = client

    def create(self):
        def call_rss_fetcher(keyword: str) -> str:
            """
            This tool fetch news through an RSS feed for a given keyword

            Args:
                keyword (str): keyword for a news

            Returns:
                response (str): rss fetcher news objects list
            """

            import sys
            import os
            sys.path(os.environ["SYS_PATH"])
            from news_agent.rss_fetcher import rss_fetcher

            return rss_fetcher.fetch(keyword)
        
        def call_gnews_fetcher(keyword: str) -> str:
            """
            This tool fetches news through GNews API
            Args:
                keyword (str): keyword for a news
            Returns:
                JSON response
            """
            import sys
            import os
            sys.path(os.environ["SYS_PATH"])
            from news_agent.gnews_fetcher import gnews_fetcher

            return gnews_fetcher.fetch(keyword)

        rss_fetcher_tool = self.client.create_tool(call_rss_fetcher)
        gnews_fetcher_tool = self.client.create_tool(call_gnews_fetcher)

        new_agent = self.client.create_agent(
            name=NAME,
            embedding_config=EMBEDDING_CONFIG,
            llm_config=LLM_CONFIG,
            memory=ChatMemory(human=HUMAN_PROMPT, persona=PERSONA_PROMPT),
            tool_ids=[rss_fetcher_tool.id],
        )

        logger.info(f"{NAME} agent created with ID: {new_agent.id}")
