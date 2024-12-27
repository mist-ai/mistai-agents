from letta import LocalClient, RESTClient, ChatMemory
from config import EMBEDDING_CONFIG, LLM_CONFIG
from utils import logger
from constants import NAME, PERSONA_PROMPT, HUMAN_PROMPT


class IPSAgent:
    def __init__(self, client: LocalClient | RESTClient):
        self.name = NAME
        self.client = client

    def create(self):
        agentId = self.client.get_agent_id(self.name)

        if not agentId:

            new_agent = self.client.create_agent(
                name=self.name,
                embedding_config=EMBEDDING_CONFIG,
                llm_config=LLM_CONFIG,
                memory=ChatMemory(
                    human=HUMAN_PROMPT,
                    persona=PERSONA_PROMPT,
                ),
            )

        logger.info(f"Created {self.name} with ID: {new_agent.id}")
