#2nd

import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw_orderbook.csv")
PROCESSED_PATH = Path("data/processed_data.csv")


def create_features(horizon=30, depth=5, smooth_window=20):
    df = pd.read_csv(RAW_PATH)

    bid_volume_cols = [f"bid_vol_{i}" for i in range(1, depth + 1)]
    ask_volume_cols = [f"ask_vol_{i}" for i in range(1, depth + 1)]

    df["total_bid_volume"] = df[bid_volume_cols].sum(axis=1)
    df["total_ask_volume"] = df[ask_volume_cols].sum(axis=1)

    df["depth_imbalance"] = (
        df["total_bid_volume"] - df["total_ask_volume"]
    ) / (
        df["total_bid_volume"] + df["total_ask_volume"]
    )

    df["imbalance_smooth"] = df["depth_imbalance"].rolling(smooth_window).mean()

    df["future_return"] = (
        df["mid_price"].shift(-horizon) / df["mid_price"] - 1
    )

    df["volatility"] = df["mid_price"].pct_change().rolling(smooth_window).std()

    df["spread_pct"] = df["spread"] / df["mid_price"]

    df = df.dropna()

    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)

    print(f"Saved processed data to {PROCESSED_PATH}")


if __name__ == "__main__":
    create_features(horizon=30, depth=5, smooth_window=20)