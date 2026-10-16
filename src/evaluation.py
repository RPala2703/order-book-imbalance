#4th

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

BACKTEST_PATH = Path("data/backtest_results.csv")

RESULTS_DIR = Path("results")
METRICS_PATH = RESULTS_DIR / "metrics.txt"
EQUITY_CURVE_PATH = RESULTS_DIR / "equity_curve.png"
IMBALANCE_PLOT_PATH = RESULTS_DIR / "imbalance_vs_return.png"


def evaluate():
    df = pd.read_csv(BACKTEST_PATH)

    returns = df["strategy_return_after_costs"]

    total_return = df["cum_return"].iloc[-1] - 1
    win_rate = (returns > 0).mean()

    sharpe = (
        returns.mean() / returns.std()
    ) * np.sqrt(252 * 24 * 60 * 60)

    drawdown = (df["cum_return"] / df["cum_return"].cummax() - 1).min()

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    with open(METRICS_PATH, "w") as f:
        f.write(f"Total Return: {total_return:.4f}\n")
        f.write(f"Win Rate: {win_rate:.4f}\n")
        f.write(f"Sharpe Ratio: {sharpe:.4f}\n")
        f.write(f"Max Drawdown: {drawdown:.4f}\n")

    plt.figure()
    df["cum_return"].plot(title="Strategy Equity Curve")
    plt.xlabel("Observation")
    plt.ylabel("Cumulative Return")
    plt.savefig(EQUITY_CURVE_PATH)
    plt.close()

    plt.figure()
    plt.scatter(df["imbalance_smooth"], df["future_return"])
    plt.xlabel("Smoothed Order Book Imbalance")
    plt.ylabel("Future Return")
    plt.title("Imbalance vs Future Return")
    plt.savefig(IMBALANCE_PLOT_PATH)
    plt.close()

    print(f"Saved results to {RESULTS_DIR}")


if __name__ == "__main__":
    evaluate()