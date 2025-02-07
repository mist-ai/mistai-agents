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
    "portfolio_value": 1000000,
    "tickers": ["MSFT", "AMZN", "NAT", "BAC", "DPZ", "DIS", "KO", "MCD", "COST", "SBUX"],
    "viewdict": {
        "AMZN": 0.10,
        "BAC": 0.30,
        "COST": 0.05,
        "DIS": 0.05,
        "DPZ": 0.20,
        "KO": -0.05,
        "MCD": 0.15,
        "MSFT": 0.10,
        "NAT": 0.50,
        "SBUX": 0.10
    },
    "confidences": [
        0.6,
        0.4,
        0.2,
        0.5,
        0.7,
        0.7,
        0.7,
        0.5,
        0.1,
        0.4
    ],
    "intervals": [
        [0, 0.25],
        [0.1, 0.4],
        [-0.1, 0.15],
        [-0.05, 0.1],
        [0.15, 0.25],
        [-0.1, 0],
        [0.1, 0.2],
        [0.08, 0.12],
        [0.1, 0.9],
        [0, 0.3]
    ]
}
"""
