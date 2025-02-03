import sys

from letta import LocalClient, RESTClient, ChatMemory
from analysis_agent.constants import NAME, PERSONA_PROMPT, HUMAN_PROMPT
from utils import logger
from config import EMBEDDING_CONFIG, LLM_CONFIG


class AnalysisAgent:
    def __init__(self, client: LocalClient | RESTClient):
        self.client = client

    def create(self):
        def allocate_portfolio_with_blacklittermen_model(config: str) -> str:
            """
                this function allocate the a portfolio of stocks using black littermen model
                input will be a json string which will contain all the portfolio requirements
                and this will output the allocation of each stock and the left over balance after the allocation

                Customer is given a portfolio details in a form of a json following structure
                extract below information from the prompt, generate a json as below specific to the usecase

                # JSON INPUT EXAMPLE
                ## tickers are the stocks we try to allocate for the portfolio, tickers array should be always non empty
                ## viewdict is the view for a particular stock movement a value between -1, 1 if no investor view provided in the prompt keep this empty
                ## confidence is how much confident we are regardign the viewdict movements, if view dict is empty keep this empty as well
                ## intervals, this is an empty array
                {
                    "tickers": ["MSFT", "AMZN", "NAT", "BAC", "DPZ", "DIS", "KO", "MCD", "COST", "SBUX"],
                    "viewdict": {
                        "AMZN": 0.10,
                        "BAC": 0.30
                    },
                    "confidences": [
                        0.6,
                        0.4
                    ],
                    "intervals": [
                        [0, 0.25],
                        [0.1, 0.4]
                    ]
                }

            Args:
                config (str): User input

            Returns:
                response (str): allocated portfolio details
            """
            import sys
            import os
            sys.path.append(os.environ["SYS_PATH"])
            from analysis_agent.portfolio import PortfolioTools

            return PortfolioTools(config).bl_allocation()

        bl_allocation_tool = self.client.create_tool(
            allocate_portfolio_with_blacklittermen_model
        )

        new_agent = self.client.create_agent(
            name=NAME,
            embedding_config=EMBEDDING_CONFIG,
            llm_config=LLM_CONFIG,
            memory=ChatMemory(human=HUMAN_PROMPT, persona=PERSONA_PROMPT),
            tool_ids=[bl_allocation_tool.id],
        )

        logger.info(f"{NAME} agent created with ID: {new_agent.id}")
