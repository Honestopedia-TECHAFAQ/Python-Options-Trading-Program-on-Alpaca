# Alpaca Trading Bot

This is a Python-based trading bot that integrates with Alpaca's API to trade based on technical indicators. It uses the RSI (Relative Strength Index) and Bollinger Bands to decide whether to buy call or put options.

## Features:
- Real-time stock analysis using RSI and Bollinger Bands.
- Trades based on buy or sell signals.
- Logs each trade to a CSV file for future reference.
- Runs every hour to analyze stocks and execute trades.

## Requirements:
- Python 3.x
- Alpaca Trade API credentials (API_KEY, API_SECRET).
- Libraries: `alpaca-trade-api`, `pandas`, `ta`, `time`.

## Setup:

1. Install the required dependencies:
   ```bash
   pip install alpaca-trade-api pandas ta
