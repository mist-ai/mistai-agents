from letta import ChatMemory
from letta_client import Letta, CreateBlock
from config import EMBEDDING_CONFIG, LLM_CONFIG
from utils import logger
from widget_agent.constants import NAME, PERSONA_PROMPT, HUMAN_PROMPT


class WidgetAgent:
    def __init__(self, client: Letta):
        self.name = NAME
        self.client = client

    def create(self):
        def call_ips_agent(prompt: str) -> str:
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
        
        call_ips_tool = self.client.tools.create_from_function(func=call_ips_agent)

        new_agent = self.client.agents.create(
            name=self.name,
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
            ]
        )

        logger.info(f"Created {self.name} with ID: {new_agent.id}")
