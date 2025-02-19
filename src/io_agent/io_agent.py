from letta_client import Letta, CreateBlock
from utils import logger
from io_agent.constants import NAME, PERSONA_PROMPT, HUMAN_PROMPT


class IOAgent:
    def __init__(self, client: Letta):
        self.client = client

    def create(self):
        def call_db_service(prompt: str) -> str:
            """
            Call the database service to generate a response based on user input.

            This function can be used to interact with the database service to:
            - Fetch more information for a given list of company names.
            - Retrieve company data based on a provided sector and keyword.

            Args:
                prompt (str): What user is looking for in the database as a user prompt

            Returns:
                response (str): A response containing company data or relevant information.
        
            """
            import sys
            import os

            sys.path.append(os.environ["SYS_PATH"])
            from io_agent.database_service import db_service

            return db_service.get_entities_from_graph(prompt)

        db_service_tool = self.client.tools.create_from_function(func=call_db_service)

        io_agent = self.client.agents.create(
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
            tool_ids=[db_service_tool.id],
        )

        logger.info(f"{NAME} agent created with ID: {io_agent.id}")
