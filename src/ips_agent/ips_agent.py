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
    # define a function with a docstring
        def roll_dice() -> str:
            """
            Simulate the roll of a 20-sided die (d20).

            This function generates a random integer between 1 and 20, inclusive,
            which represents the outcome of a single roll of a d20.

            Returns:
                str: The result of the die roll.
            """
            import random

            dice_role_outcome = random.randint(1, 20)
            output_string = f"You rolled a {dice_role_outcome}"
            return output_string


        # create the tool
        tool = self.client.tools.create_from_function(
            func=roll_dice
        )
        print(f"Created tool {tool.name}")

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
            tool_ids=[tool.id]
        )

        logger.info(f"Created {self.name} with ID: {new_agent.id}")
