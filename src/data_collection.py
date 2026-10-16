#1st

from binance.client import Client
import pandas as pd
import time
from pathlib import Path
from requests.exceptions import ConnectionError, ReadTimeout
from urllib3.exceptions import ProtocolError

client = Client()

DATA_PATH = Path("data/raw_orderbook.csv")


def collect_orderbook(symbol="BTCUSDT", snapshots=1000, interval=1, depth=5):
    data = []

    while len(data) < snapshots:
        try:
            ob = client.get_order_book(symbol=symbol, limit=depth)

            row = {"timestamp": time.time()}

            for i in range(depth):
                row[f"bid_price_{i+1}"] = float(ob["bids"][i][0])
                row[f"bid_vol_{i+1}"] = float(ob["bids"][i][1])
                row[f"ask_price_{i+1}"] = float(ob["asks"][i][0])
                row[f"ask_vol_{i+1}"] = float(ob["asks"][i][1])

            best_bid = row["bid_price_1"]
            best_ask = row["ask_price_1"]

            row["mid_price"] = (best_bid + best_ask) / 2
            row["spread"] = best_ask - best_bid

            data.append(row)

            print(f"Collected {len(data)}/{snapshots}")
            time.sleep(interval)

        except (ConnectionError, ProtocolError, ReadTimeout, ConnectionResetError):
            print("Connection issue. Waiting 5 seconds and retrying...")
            time.sleep(5)

        except Exception as e:
            print(f"Unexpected error: {e}")
            print("Waiting 5 seconds and retrying...")
            time.sleep(5)

    df = pd.DataFrame(data)

    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_PATH, index=False)

    print(f"Saved {len(df)} rows to {DATA_PATH}")


if __name__ == "__main__":
    collect_orderbook(symbol="BTCUSDT", snapshots=2000, interval=1, depth=5)