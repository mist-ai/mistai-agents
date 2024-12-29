from letta import LocalClient, RESTClient, ChatMemory
from ips_agent.constants import NAME as IPS_NAME
from orchestrator.constants import NAME, PERSONA_PROMPT, HUMAN_PROMPT
from utils import logger
from config import EMBEDDING_CONFIG, LLM_CONFIG


class Orchestrator:
    def __init__(self, client: LocalClient | RESTClient):
        self.client = client

    async def call_ips(self, prompt: str) -> str:
        """
        Call the IPS agent to generate a response to the user input.

        Args:
            prompt (str): User input

        Returns:
            response (str): IPS agent response
        """

        # if self.client is None:
        #     logger.error("Client is not initialized")
        #     return "Error: Client is not initialized"
        response = await self.client.send_message(
            message=prompt, agent_name=IPS_NAME, role="user"
        )

        logger.info(f"IPS response: {response}")

        return response

    def create(self):

        call_ips_tool = self.client.create_tool(self.call_ips)

        self.client.create_agent(
            name=NAME,
            embedding_config=EMBEDDING_CONFIG,
            llm_config=LLM_CONFIG,
            memory=ChatMemory(human=HUMAN_PROMPT, persona=PERSONA_PROMPT),
            tool_ids=[call_ips_tool.id],
        )
