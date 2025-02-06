from letta import ChatMemory
from letta_client import Letta, CreateBlock
from config import EMBEDDING_CONFIG, LLM_CONFIG
from utils import logger
from ips_agent.constants import NAME, PERSONA_PROMPT, HUMAN_PROMPT


class IPSAgent:
    def __init__(self, client: Letta):
        self.name = NAME
        self.client = client

    def create(self):
        new_agent = self.client.agents.create(
            name=self.name,
            memory_blocks=[
                CreateBlock(
                    value="Name: Caren",
                    label="human",
                ),
            ],
            model="openai/gpt-4o-mini",
            embedding="openai/text-embedding-ada-002",
        )

        logger.info(f"Created {self.name} with ID: {new_agent.id}")
