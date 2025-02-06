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

            lClient = create_client()

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
            sys.path(os.environ["SYS_PATH"])
            from letta import create_client
            from analysis_agent.constants import NAME as IPS_NAME

            lClient = create_client()

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
            sys.path(os.environ["SYS_PATH"])
            from letta import create_client
            from news_agent.constants import NAME as IPS_NAME

            lClient = create_client()

            response = lClient.send_message(
                message=prompt, agent_name=IPS_NAME, role="user"
            )

            return response.messages[len(response.messages) - 2].tool_call.arguments

        call_ips_tool = self.client.create_tool(call_ips, name="call_ips")
        call_analysis_agent_tool = self.client.create_tool(
            call_analysis_agent, name="call_analysis_agent_tool"
        )
        call_news_agent_tool = self.client.create_tool(
            call_news_agent, name="call_news_agent"
        )

        new_agent = self.client.create_agent(
            name=NAME,
            embedding_config=EMBEDDING_CONFIG,
            llm_config=LLM_CONFIG,
            memory=ChatMemory(human=HUMAN_PROMPT, persona=PERSONA_PROMPT),
            tool_ids=[
                call_ips_tool.id,
                call_analysis_agent_tool.id,
                call_news_agent_tool.id,
            ],
        )

        logger.info(f"{NAME} agent created with ID: {new_agent.id}")
