from pypfopt import black_litterman, risk_models
from pypfopt import BlackLittermanModel, plotting
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from pypfopt import EfficientFrontier, objective_functions
from pypfopt import DiscreteAllocation

class Portfolio:

    def bl_allocation():
        tickers = ["MSFT", "AMZN", "NAT", "BAC", "DPZ", "DIS", "KO", "MCD", "COST", "SBUX"]
        ohlc = yf.download(tickers, period="max")
        prices = ohlc["Adj Close"]
        prices.tail()

        market_prices = yf.download("SPY", period="max")["Adj Close"]
        market_prices.head()

        mcaps = {}
        for t in tickers:
            stock = yf.Ticker(t)
            mcaps[t] = stock.info["marketCap"]
        mcaps

        S = risk_models.CovarianceShrinkage(prices).ledoit_wolf()
        delta = black_litterman.market_implied_risk_aversion(market_prices)
        delta
        plotting.plot_covariance(S, plot_correlation=True)
        market_prior = black_litterman.market_implied_prior_returns(mcaps, delta, S)
        market_prior
        market_prior.plot.barh(figsize=(10,5))
        # You don't have to provide views on all the assets
        viewdict = {
            "AMZN": 0.10,
            "BAC": 0.30,
            "COST": 0.05,
            "DIS": 0.05,
            "DPZ": 0.20,
            "KO": -0.05,  # I think Coca-Cola will go down 5%
            "MCD": 0.15,
            "MSFT": 0.10,
            "NAT": 0.50,  # but low confidence, which will be reflected later
            "SBUX": 0.10
        }

        bl = BlackLittermanModel(S, pi=market_prior, absolute_views=viewdict)
        confidences = [
            0.6,
            0.4,
            0.2,
            0.5,
            0.7, # confident in dominos
            0.7, # confident KO will do poorly
            0.7, 
            0.5,
            0.1,
            0.4
        ]
        bl = BlackLittermanModel(S, pi=market_prior, absolute_views=viewdict, omega="idzorek", view_confidences=confidences)
        fig, ax = plt.subplots(figsize=(7,7))
        im = ax.imshow(bl.omega)

        # We want to show all ticks...
        ax.set_xticks(np.arange(len(bl.tickers)))
        ax.set_yticks(np.arange(len(bl.tickers)))

        ax.set_xticklabels(bl.tickers)
        ax.set_yticklabels(bl.tickers)
        plt.show()

        np.diag(bl.omega)

        intervals = [
            (0, 0.25),
            (0.1, 0.4),
            (-0.1, 0.15),
            (-0.05, 0.1),
            (0.15, 0.25),
            (-0.1, 0),
            (0.1, 0.2),
            (0.08, 0.12),
            (0.1, 0.9),
            (0, 0.3)
        ]

        variances = []
        for lb, ub in intervals:
            sigma = (ub - lb)/2
            variances.append(sigma ** 2)

        print(variances)
        omega = np.diag(variances)

        # We are using the shortcut to automatically compute market-implied prior
        bl = BlackLittermanModel(S, pi="market", market_caps=mcaps, risk_aversion=delta,
                                absolute_views=viewdict, omega=omega)
        
        # Posterior estimate of returns
        ret_bl = bl.bl_returns()
        ret_bl

        rets_df = pd.DataFrame([market_prior, ret_bl, pd.Series(viewdict)], 
             index=["Prior", "Posterior", "Views"]).T
        rets_df

        rets_df.plot.bar(figsize=(12,8))

        S_bl = bl.bl_cov()
        plotting.plot_covariance(S_bl)

        ef = EfficientFrontier(ret_bl, S_bl)
        ef.add_objective(objective_functions.L2_reg)
        ef.max_sharpe()
        weights = ef.clean_weights()
        weights

        pd.Series(weights).plot.pie(figsize=(10,10))

        da = DiscreteAllocation(weights, prices.iloc[-1], total_portfolio_value=20000)
        alloc, leftover = da.lp_portfolio()
        print(f"Leftover: ${leftover:.2f}")
        alloc


p = Portfolio()

p.bl_allocation()