import json
from typing import List, Dict, Tuple


class BLConfig:
    def __init__(
        self,
        portfolio_value: float,
        tickers: List[str],
        viewdict: Dict[str, float],
        confidences: List[float],
        intervals: List[Tuple[float, float]],
    ):
        self.portfolio_value = portfolio_value
        self.tickers = tickers
        self.viewdict = viewdict
        self.confidences = confidences
        self.intervals = intervals

    @classmethod
    def from_json(cls, json_string: str):
        """Deserialize JSON string to a PortfolioModel object."""
        data = json.loads(json_string)

        # Convert intervals to tuples
        intervals = [tuple(interval) for interval in data["intervals"]]

        return cls(
            portfolio_value=data["portfolio_value"],
            tickers=data["tickers"],
            viewdict=data["viewdict"],
            confidences=data["confidences"],
            intervals=intervals,
        )

    def __repr__(self):
        return (
            f"PortfolioModel("
            f"portfolio_value={self.portfolio_value}"
            f"tickers={self.tickers}, "
            f"viewdict={self.viewdict}, "
            f"confidences={self.confidences}, "
            f"intervals={self.intervals})"
        )


# example json
json_string = """
{
    "portfolio_value": 250,
    "tickers": ["SAMP.N0000", "AEL.N0000"],
    "viewdict": {
    },
    "confidences": [],
    "intervals": []
}
"""
