# Order Book Imbalance Strategy

## Overview

This project investigates whether short-term order book imbalance can predict future price movements in BTC/USDT.

The main hypothesis is that when bid-side volume significantly exceeds ask-side volume, short-term upward price pressure may occur, and vice versa.

## Data

Order book snapshots were collected from Binance using the BTC/USDT pair.

Each snapshot contains:

- Best bid price
- Best bid volume
- Best ask price
- Best ask volume
- Mid price

## Signal

The order book imbalance signal is calculated as:

```text
imbalance = (bid_volume - ask_volume) / (bid_volume + ask_volume)


## Baseline Results: Version 1

The first version tested a simple order book imbalance signal using top-of-book bid and ask volume.

### Results

- Total Return: -2.05%
- Win Rate: 18.86%
- Sharpe Ratio: -673.66
- Max Drawdown: -2.57%

### What Went Wrong

The baseline strategy was not profitable. The imbalance signal appeared too noisy and did not show a strong relationship with future returns.

Possible issues:

- Only the best bid and ask levels were used
- The prediction horizon may have been too short
- Transaction costs overwhelmed any weak signal
- The strategy traded whenever imbalance crossed a fixed threshold, without filtering for market conditions
- The signal was based on raw/smoothed volume imbalance only, with no volatility or spread filter

This result is useful because it shows that a naive imbalance strategy is not enough on its own.