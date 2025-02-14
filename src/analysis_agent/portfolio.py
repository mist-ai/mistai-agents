# import sys
# import os

# sys.path.append(os.environ["SYS_PATH"])
import json
import numpy as np
import pandas as pd
import yfinance as yf
from pypfopt import black_litterman, risk_models
from pypfopt import BlackLittermanModel
from pypfopt import EfficientFrontier, objective_functions
from pypfopt import DiscreteAllocation
from analysis_agent.base import BLConfig, json_string
from analysis_agent.agent_utils import get_prices, get_market_caps
from tradingview_ta import TA_Handler, Interval


class PortfolioTools:
    def __init__(self):
        ...

    def bl_allocation(self, config: str):
        self.bl_config = BLConfig.from_json(config)
        if len(self.bl_config.tickers) == 0:
            return json.dumps({})

        # ohlc = yf.download(self.bl_config.tickers, period="max")
        # prices = ohlc["Close"]
        prices = get_prices(self.bl_config.tickers)
        prices.tail()

        # market_prices = yf.download("SPY", period="max")["Close"]
        # market_prices.head()
        market_prices = get_prices(["ASI"])

        # mcaps = {}
        # for t in self.bl_config.tickers:
        #     stock = yf.Ticker(t)
        #     mcaps[t] = stock.info["marketCap"]
        # mcaps

        mcaps = get_market_caps(self.bl_config.tickers, currency="LKR")

        S = risk_models.CovarianceShrinkage(prices).ledoit_wolf()
        delta = black_litterman.market_implied_risk_aversion(market_prices)
        delta
        # plotting.plot_covariance(S, plot_correlation=True)
        market_prior = black_litterman.market_implied_prior_returns(mcaps, delta, S)
        market_prior
        # market_prior.plot.barh(figsize=(10, 5))

        bl = BlackLittermanModel(
            S, pi=market_prior, absolute_views=self.bl_config.viewdict
        )
        bl = BlackLittermanModel(
            S,
            pi=market_prior,
            absolute_views=self.bl_config.viewdict,
            omega="idzorek",
            view_confidences=self.bl_config.confidences,
        )
        # fig, ax = plt.subplots(figsize=(7, 7))
        # ax.imshow(bl.omega)

        # We want to show all ticks...
        # ax.set_xticks(np.arange(len(bl.tickers)))
        # ax.set_yticks(np.arange(len(bl.tickers)))

        # ax.set_xticklabels(bl.tickers)
        # ax.set_yticklabels(bl.tickers)
        # plt.show()

        np.diag(bl.omega)

        variances = []
        for lb, ub in self.bl_config.intervals:
            sigma = (ub - lb) / 2
            variances.append(sigma**2)

        print(variances)
        omega = np.diag(variances)

        # We are using the shortcut to automatically compute market-implied prior
        bl = BlackLittermanModel(
            S,
            pi="market",
            market_caps=mcaps,
            risk_aversion=delta,
            absolute_views=self.bl_config.viewdict,
            omega=omega,
        )

        # Posterior estimate of returns
        ret_bl = bl.bl_returns()
        ret_bl

        rets_df = pd.DataFrame(
            [market_prior, ret_bl, pd.Series(self.bl_config.viewdict)],
            index=["Prior", "Posterior", "Views"],
        ).T
        rets_df

        # rets_df.plot.bar(figsize=(12, 8))
        # plt.show()

        S_bl = bl.bl_cov()
        # plotting.plot_covariance(S_bl)

        ef = EfficientFrontier(ret_bl, S_bl)
        ef.add_objective(objective_functions.L2_reg)
        ef.max_sharpe()
        weights = ef.clean_weights()
        weights

        # pd.Series(weights).plot.pie(figsize=(10, 10))

        da = DiscreteAllocation(
            weights,
            prices.iloc[-1],
            total_portfolio_value=self.bl_config.portfolio_value,
        )
        alloc, leftover = da.lp_portfolio()
        return alloc, leftover

    def technical_summary(self, ticker: str) -> dict:
        handler = TA_Handler(
            symbol=ticker,
            screener="srilanka",
            exchange="CSELK",
            interval=Interval.INTERVAL_1_DAY,
        )
        return dict(
            summary=handler.get_analysis().summary,
            indicators=handler.get_analysis().indicators,
            oscillators=handler.get_analysis().oscillators,
            moving_averages=handler.get_analysis().moving_averages,
        )


# p = PortfolioTools()
# print(p.technical_summary())
# print(p.bl_allocation(json_string))
