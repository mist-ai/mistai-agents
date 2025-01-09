from letta import LocalClient, RESTClient, ChatMemory
from config import EMBEDDING_CONFIG, LLM_CONFIG
from utils import logger
from ips_agent.constants import NAME, PERSONA_PROMPT, HUMAN_PROMPT


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

        else:
            logger.info(f" {self.name} already exists.")

    def delete(self):
        agentId = self.client.get_agent_id(self.name)

        if agentId:
            self.client.delete_agent(agentId)
            logger.info(f"Deleted {self.name} with ID: {agentId}")
        else:
            logger.info(f"Agent {self.name} not found")
