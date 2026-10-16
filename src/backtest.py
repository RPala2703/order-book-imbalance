#3rd

import pandas as pd
from pathlib import Path

PROCESSED_PATH = Path("data/processed_data.csv")
BACKTEST_PATH = Path("data/backtest_results.csv")


def run_backtest(
    threshold=0.35,
    transaction_cost=0.0002,
    min_volatility_quantile=0.6,
    max_spread_quantile=0.8
):
    df = pd.read_csv(PROCESSED_PATH)

    df["position"] = 0

    volatility_cutoff = df["volatility"].quantile(min_volatility_quantile)
    spread_cutoff = df["spread_pct"].quantile(max_spread_quantile)

    trade_filter = (
        (df["volatility"] > volatility_cutoff) &
        (df["spread_pct"] < spread_cutoff)
    )

    long_condition = (
        (df["imbalance_smooth"] > threshold) &
        trade_filter
    )

    short_condition = (
        (df["imbalance_smooth"] < -threshold) &
        trade_filter
    )

    df.loc[long_condition, "position"] = 1
    df.loc[short_condition, "position"] = -1

    df["strategy_return"] = df["position"] * df["future_return"]

    df["trade"] = df["position"].diff().abs().fillna(0)

    df["strategy_return_after_costs"] = (
        df["strategy_return"] - df["trade"] * transaction_cost
    )

    df["cum_return"] = (
        1 + df["strategy_return_after_costs"]
    ).cumprod()

    df.to_csv(BACKTEST_PATH, index=False)

    print(f"Saved backtest results to {BACKTEST_PATH}")
    print(f"Trades taken: {(df['position'] != 0).sum()} out of {len(df)} rows")


if __name__ == "__main__":
    run_backtest()