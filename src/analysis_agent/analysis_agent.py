from letta_client import Letta, CreateBlock
from analysis_agent.constants import NAME, PERSONA_PROMPT, HUMAN_PROMPT
from utils import logger


class AnalysisAgent:
    def __init__(self, client: Letta):
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
                ## portfolio_value is the total value of the portfolio to allocate,
                ## tickers are the stocks we try to allocate for the portfolio, tickers array should be always non empty
                ## viewdict is the view for a particular stock movement a value between -1, 1 if no investor view provided in the prompt keep this empty
                ## confidence is how much confident we are regardign the viewdict movements, if view dict is empty keep this empty as well
                ## intervals, this is an empty array
                {
                    "portfolio_value": 1000000,
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
            import json

            sys.path.append(os.environ["SYS_PATH"])
            from analysis_agent.portfolio import PortfolioTools

            alloc, leftover = PortfolioTools().bl_allocation(config)
            return json.dumps({"allocation": alloc, "leftover": leftover}, indent=4)

        def technical_summary_of_stock(ticker: str) -> str:
            """
                this function fetches the techincal analysis summary of a particular stock using its ticker

                ## example
                # for input "SAMP.N0000"
                # output is type json string {...}

            Args:
                ticker (str): User input

            Returns:
                response (str): technical analysis summary of a stock/ticker
            """
            import sys
            import os
            import json

            sys.path.append(os.environ["SYS_PATH"])
            from analysis_agent.portfolio import PortfolioTools

            return json.dumps(
                PortfolioTools().technical_summary(ticker=ticker), indent=4
            )

        bl_allocation_tool = self.client.tools.create_from_function(
            func=allocate_portfolio_with_blacklittermen_model
        )

        technical_summary_tool = self.client.tools.create_from_function(
            func=technical_summary_of_stock
        )

        new_agent = self.client.agents.create(
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
            tool_ids=[bl_allocation_tool.id, technical_summary_tool.id],
        )

        logger.info(f"{NAME} agent created with ID: {new_agent.id}")
