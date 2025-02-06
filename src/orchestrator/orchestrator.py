from letta import LocalClient, RESTClient, ChatMemory
from orchestrator.constants import NAME, PERSONA_PROMPT, HUMAN_PROMPT
from utils import logger
from config import EMBEDDING_CONFIG, LLM_CONFIG
import sys
import os


class Orchestrator:
    def __init__(self, client: LocalClient | RESTClient):
        self.client = client

    def create(self):
        def call_ips(prompt: str) -> str:
            """
            Call the IPS agent to generate a response to the user input.

            Args:
                prompt (str): User input

            Returns:
                response (str): IPS agent response
            """
            import sys
            import os

            sys.path(os.environ["SYS_PATH"])
            from letta import create_client
            from ips_agent.constants import NAME as IPS_NAME
            from letta.schemas.llm_config import LLMConfig
            from letta.schemas.embedding_config import EmbeddingConfig

            lClient = create_client()

            lClient.set_default_llm_config(LLMConfig.default_config("gpt-4o-mini"))
            lClient.set_default_embedding_config(
                EmbeddingConfig.default_config(provider="openai")
            )

            response = lClient.send_message(
                message=prompt, agent_name=IPS_NAME, role="user"
            )

            return response.messages[len(response.messages) - 2].tool_call.arguments

        def call_analysis_agent(prompt: str) -> str:
            """
            Call the Analysis agent to generate a response to the user input.
            you can call analysis_agent in a case of below:
                - create a porfolio for given stocks, but you have to pass tickers of the stock inorder to get a response

            Args:
                prompt (str): prompt that should be passed for the analysis agent

            Returns:
                response (str): analysis agent response
            """
            import sys
            import os

            sys.path(os.environ["SYS_PATH"])
            from letta import create_client
            from analysis_agent.constants import NAME as IPS_NAME
            from letta.schemas.llm_config import LLMConfig
            from letta.schemas.embedding_config import EmbeddingConfig

            lClient = create_client()

            lClient.set_default_llm_config(LLMConfig.default_config("gpt-4o-mini"))
            lClient.set_default_embedding_config(
                EmbeddingConfig.default_config(provider="openai")
            )

            response = lClient.send_message(
                message=prompt, agent_name=IPS_NAME, role="user"
            )

            return response.messages[len(response.messages) - 2].tool_call.arguments

        def call_news_agent(prompt: str) -> str:
            """
            Call the News agent to fetch news for a keyword.
            you can call news_agent in a case of below:
                - fetch news form rss feed for a specific keyword

            Args:
                prompt (str): prompt that should be passed for the news agent

            Returns:
                response (str): news agent response
            """
            import sys
            import os

            sys.path(os.environ["SYS_PATH"])
            from letta import create_client
            from news_agent.constants import NAME as IPS_NAME

            from letta.schemas.llm_config import LLMConfig
            from letta.schemas.embedding_config import EmbeddingConfig

            lClient = create_client()

            lClient.set_default_llm_config(LLMConfig.default_config("gpt-4o-mini"))
            lClient.set_default_embedding_config(
                EmbeddingConfig.default_config(provider="openai")
            )

            response = lClient.send_message(
                message=prompt, agent_name=IPS_NAME, role="user"
            )

            return response.messages[len(response.messages) - 2].tool_call.arguments
        call_ips_tool = self.client.tools.upsert_from_function(func=call_ips)
        call_analysis_agent_tool = self.client.tools.upsert_from_function(
            func=call_analysis_agent
        )
        call_news_agent_tool = self.client.tools.upsert_from_function(
            func=call_news_agent
        )

        new_agent = self.client.create_agent(
            name=NAME,
            memory=ChatMemory(human=HUMAN_PROMPT, persona=PERSONA_PROMPT),
            tool_ids=[
                call_ips_tool.id,
                call_analysis_agent_tool.id,
                call_news_agent_tool.id
            ],
        )

        logger.info(f"{NAME} agent created with ID: {new_agent.id}")
