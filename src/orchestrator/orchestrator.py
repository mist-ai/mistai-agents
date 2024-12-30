from letta import LocalClient, RESTClient, ChatMemory
from orchestrator.constants import NAME, PERSONA_PROMPT, HUMAN_PROMPT
from utils import logger
from config import EMBEDDING_CONFIG, LLM_CONFIG


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

            from letta import create_client
            from ips_agent.constants import NAME as IPS_NAME

            lClient = create_client()

            response = lClient.send_message(
                message=prompt, agent_name=IPS_NAME, role="user"
            )

            return response.messages[len(response.messages) - 2].tool_call.arguments

        call_ips_tool = self.client.create_tool(call_ips)

        self.client.create_agent(
            name=NAME,
            embedding_config=EMBEDDING_CONFIG,
            llm_config=LLM_CONFIG,
            memory=ChatMemory(human=HUMAN_PROMPT, persona=PERSONA_PROMPT),
            tool_ids=[call_ips_tool.id],
        )
