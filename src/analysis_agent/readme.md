# PyPortfolio Usage

## Prerequisites

We need a expected return estimate and a risk model to do the optimization

# Expected Returns Estimators

### 1. Mean Historical Returns

### 2. Black Litterman Allocation

- [Find cookbook for BL Model usage (click here)](https://github.com/robertmartin8/PyPortfolioOpt/blob/master/cookbook/4-Black-Litterman-Allocation.ipynb)

- This combines a prior estimate o f returns (for example, the market-implied returns) with views on certain assets, to produce a posterior estimate of expected returns. The advantages of this are:

    - You can provide views on only a subset of assets and BL will meaningfully propagate it, taking into account the covariance with other assets.
    - You can provide confidence in your views.
    - Using Black-Litterman posterior returns results in much more stable portfolios than using mean-historical return.

## Concepts of BL Model

### Views

* In the Black-Litterman model, users can either provide absolute or relative views. Absolute views are statements like: “AAPL will return 10%” or “XOM will drop 40%”. Relative views, on the other hand, are statements like “GOOG will outperform FB by 3%”.

These views must be specified in the vector 𝑄
and mapped to the asset universe via the picking matrix 𝑃
. A brief example of this is shown below, though a comprehensive guide is given by Idzorek. Let’s say that our universe is defined by the ordered list: SBUX, GOOG, FB, AAPL, BAC, JPM, T, GE, MSFT, XOM. We want to represent four views on these 10 assets, two absolute and two relative:

1. SBUX will drop 20% (absolute)
2. MSFT will rise by 5% (absolute)
3. GOOG outperforms FB by 10%
4. BAC and JPM will outperform T and GE by 15%

The corresponding views vector is formed by taking the numbers above and putting them into a column:

```python
Q = np.array([-0.20, 0.05, 0.10, 0.15]).reshape(-1, 1)
```

The picking matrix is more interesting. Remember that its role is to link the views (which mention 8 assets) to the universe of 10 assets. Arguably, this is the most important part of the model because it is what allows us to propagate our expectations (and confidences in expectations) into the model:

```python
P = np.array(
    [
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, -1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0.5, 0.5, -0.5, -0.5, 0, 0],
    ]
)
```

Explanation of above

- Each view has a corresponding row in the picking matrix (the order matters)
- Absolute views have a single 1 in the column corresponding to the ticker’s order in the universe.
- Relative views have a positive number in the nominally outperforming asset columns and a negative number in the nominally underperforming asset columns. The numbers in each row should sum up to 0.


# Risk Models Estimators
The way of quantifing the risk of the asset

> [!TIP]
> Subject of risk models is far more important than expected returns
research by Kritzman et al. (2010) [1] suggests that minimum variance portfolios, formed by optimising without providing expected returns, actually perform much better out of sample.

#### Covariance Matrix
- Most commonly used to represent a risk model
- Contains co-dependence and volatilites of assets
- reducing dependencies can reduce risk

### Statistical Estimators for Covariance Matrix

#### 1. Simple Covariance

- _recent (post-2000) research indicates that there are much more robust statistical estimators of the covariance matrix_

Suffers from misspecification error and a lack of robustness. This is particularly problematic in mean-variance optimization, because the optimizer may give extra credence to the erroneous values.

> [!NOTE]
> This should not be your default choice! Please use a shrinkage estimator instead.

#### 2. Semi Covariance

- The covariance given that the returns are less than the benchmark.

#### 3. Exponential Covariance

- the covariance given that the returns are less than the benchmark.

> [!TIP]
> For most use cases, I would just go with Ledoit Wolf shrinkage, as recommended by Quantopian in their lecture series on quantitative finance.

#### 4. ledoit_wolf_constant_variance

- The target is the diagonal matrix with the mean of asset variances on the diagonals and zeroes elsewhere. This is the shrinkage offered by `sklearn.LedoitWolf`

#### 5. ledoit_wolf_single_factor

- Based on Sharpe’s single-index model which effectively uses a stock’s beta to the market as a risk model. See Ledoit and Wolf 2001

#### 6. ledoit_wolf_constant_correlation

- Which all pairwise correlations are set to the average correlation (sample variances are unchanged). See Ledoit and Wolf 2003

#### 7. oracle_approximating

- Oracle approximating shrinkage (OAS), invented by Chen et al. (2010) [5], which has a lower mean-squared error than Ledoit-Wolf shrinkage when samples are Gaussian or near-Gaussian.


# Optimizations

### 1. Mean Variance Optimization

- can support short positions
- can create market neutral portfolios
- can set L2 regularization if needed to avoid more zero weights 
- can get discrete allocations 

```python
# w contains cleaned weights from optimzation
latest_prices = get_latest_prices(df)
da = DiscreteAllocation(w, latest_prices, total_portfolio_value=20000)
```

### Objective functions that can use

- Portfolio variance (i.e square of volatility)
- Portfolio return
- Sharpe ratio
- L2 regularisation (minimising this reduces nonzero weights)

> [!NOTE]
> In practice, 𝛾
 must be tuned to achieve the level of regularisation that you want. However, if the universe of assets is small (less than 20 assets), then gamma=1 is a good starting point. For larger universes, or if you want more non-negligible weights in the final portfolio, increase gamma.

- Quadratic utility
- Transaction cost model (a simple one)
- Ex-ante (squared) tracking error
- Ex-post (squared) tracking error

### 2. Efficient SemiVariance Optimization

- Instead of penalising volatility, mean-semivariance optimization seeks to only penalise downside volatility, since upside volatility may be desirable.

- EfficientSemivariance has a slightly different API to EfficientFrontier. Instead of passing in a covariance matrix, you should past in a dataframe of historical/simulated returns (this can be constructed from your price dataframe using the helper method

> [!WARNING]
> Finding portfolios on the mean-semivariance frontier is computationally harder than standard mean-variance optimization: our implementation uses 2T + N optimization variables, meaning that for 50 assets and 3 years of data, there are about 1500 variables. While EfficientSemivariance allows for additional constraints/objectives in principle, you are much more likely to run into solver errors. I suggest that you keep EfficientSemivariance problems small and minimally constrained.

### 3. Efficient CVaR

### 4. Efficient CDaR

### There are other optimizors as well

# How to improve performance

- Try the Hierarchical Risk Parity model (see Other Optimizers) – which seems to robustly outperform mean-variance optimization out of sample.
- Use the Black-Litterman model to construct a more stable model of expected returns. Alternatively, just drop the expected returns altogether! There is a large body of research that suggests that minimum variance portfolios (ef.min_volatility()) consistently outperform maximum Sharpe ratio portfolios out-of-sample (even when measured by Sharpe ratio), because of the difficulty of forecasting expected returns.
- Try different risk models: shrinkage models are known to have better numerical properties compared with the sample covariance matrix.
- Add some new objective terms or constraints. Tune the L2 regularisation parameter to see how diversification affects the performance.

> [!CAUTION]
> Supplying expected returns can do more harm than good. If predicting stock returns were as easy as calculating the mean historical return, we’d all be rich! For most use-cases, I would suggest that you focus your efforts on choosing an appropriate risk model (see Risk Models).
As of v0.5.0, you can use Black-Litterman Allocation to significantly improve the quality of your estimate of the expected returns.