from letta_client import Letta, CreateBlock
from utils import logger
from io_agent.constants import NAME, PERSONA_PROMPT, HUMAN_PROMPT


class IOAgent:
    def __init__(self, client: Letta):
        self.client = client

    def create(self):
        def call_db_service(sector: str, keyword: str) -> str:
            """
            Call the database service to generate a response to the user input.
            you can call_db_service in a case of below:
                - fetch more info for a give list of company names

            Args:
                sector (str): sector of the company
                keyword (str): company name

            Returns:
                response (str): IO agent response
            """
            import sys
            import os

            sys.path.append(os.environ["SYS_PATH"])
            from io_agent.database_service import db_service

            return db_service.get_company_info(keyword, sector=sector)

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
