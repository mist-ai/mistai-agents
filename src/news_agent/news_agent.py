from letta_client import Letta, CreateBlock
from utils import logger
from config import EMBEDDING_CONFIG, LLM_CONFIG
from news_agent.constants import NAME, PERSONA_PROMPT, HUMAN_PROMPT


class NewsAgent:
    def __init__(self, client: Letta):
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
            sys.path.append(os.environ["SYS_PATH"])
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
            sys.path.append(os.environ["SYS_PATH"])
            from news_agent.gnews_fetcher import gnews_fetcher

            return gnews_fetcher.fetch(keyword)

        
        rss_fetcher_tool = self.client.tools.create_from_function(
            func=call_rss_fetcher
        )
        gnews_fetcher_tool = self.client.tools.create_from_function(
            func=call_gnews_fetcher
        )

        new_agent = self.client.agents.create(
            name=NAME,
            memory_blocks=[
                CreateBlock(
                    value=HUMAN_PROMPT,
                    label="human",
                ),
                CreateBlock(
                    value=PERSONA_PROMPT,
                    label="persona",
                ),
            ],
            model="openai/gpt-4o-mini",
            embedding="openai/text-embedding-ada-002",
            tool_ids=[gnews_fetcher_tool.id, rss_fetcher_tool.id],
        )

        logger.info(f"{NAME} agent created with ID: {new_agent.id}")
