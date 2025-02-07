from letta_client import Letta, CreateBlock
from orchestrator.constants import NAME, PERSONA_PROMPT, HUMAN_PROMPT
from utils import logger


class Orchestrator:
    def __init__(self, client: Letta):
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
            import os
            import sys

            sys.path.append(os.environ["SYS_PATH"])
            try:
                from letta_client import Letta, MessageCreate
                from ips_agent.constants import NAME

                client = Letta(base_url="http://localhost:8283")
                agent_id = list(
                    filter(lambda agent: agent.name == NAME, client.agents.list())
                )[0].id

                print(agent_id)

                response = client.agents.messages.create(
                    agent_id=agent_id,
                    messages=[
                        MessageCreate(
                            role="user",
                            content=prompt,
                        )
                    ],
                )
                return response.messages[len(response.messages) - 1].content
            except Exception as e:
                return e

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
            import os
            import sys

            sys.path.append(os.environ["SYS_PATH"])
            try:
                from letta_client import Letta, MessageCreate
                from analysis_agent.constants import NAME

                client = Letta(base_url="http://localhost:8283")
                agent_id = list(
                    filter(lambda agent: agent.name == NAME, client.agents.list())
                )[0].id

                print(agent_id)

                response = client.agents.messages.create(
                    agent_id=agent_id,
                    messages=[
                        MessageCreate(
                            role="user",
                            content=prompt,
                        )
                    ],
                )
                return response.messages[len(response.messages) - 1].content
            except Exception as e:
                return e

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
            import os
            import sys

            sys.path.append(os.environ["SYS_PATH"])
            try:
                from letta_client import Letta, MessageCreate
                from news_agent.constants import NAME

                client = Letta(base_url="http://localhost:8283")
                agent_id = list(
                    filter(lambda agent: agent.name == NAME, client.agents.list())
                )[0].id

                print(agent_id)

                response = client.agents.messages.create(
                    agent_id=agent_id,
                    messages=[
                        MessageCreate(
                            role="user",
                            content=prompt,
                        )
                    ],
                )
                return response.messages[len(response.messages) - 1].content
            except Exception as e:
                return e

        call_ips_tool = self.client.tools.create_from_function(func=call_ips)
        call_analysis_agent_tool = self.client.tools.create_from_function(
            func=call_analysis_agent
        )
        call_news_agent_tool = self.client.tools.create_from_function(
            func=call_news_agent
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
            tool_ids=[
                call_ips_tool.id,
                call_analysis_agent_tool.id,
                call_news_agent_tool.id,
            ],
        )

        logger.info(f"{NAME} agent created with ID: {new_agent.id}")
