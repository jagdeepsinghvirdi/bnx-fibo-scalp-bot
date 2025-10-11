## 🟩 Prompt 1 – Setup & Architecture

> Build a complete setup plan for the “Scalp Fibo Bot” for BingX.  
> Include required Python libraries, folder structure, environment variables, and Docker configuration.  
> Use `bingx` for BingX API integration, `pandas` and `numpy` for analytics,  
> and a Telegram bot for notifications.  
> Support both **testnet** and **mainnet** modes, with modular folders for:
> - `/core` → strategy, data, risk modules  
> - `/config` → env & credentials  
> - `/logs` → trade CSV files  
> - `/docker` → Dockerfile + compose  
> Also include `.env` template and logging setup.

---

## 🟩 Prompt 2 – Data Fetcher & Fibo Calculations

> Write a Python module to fetch live and historical data for the Scalp Fibo Bot.  
> Use `bingx` to get OHLCV candles for 1m, 3m, 5m, 15m, and 1H timeframes.  
> Implement helper functions:
> - `get_swing_high_low(df, lookback)` – detect local swing zones  
> - `build_fibo_levels(low, high)` – compute 0.236–0.886 levels  
> - `ema(df, period)` – for EMA(50, 200) trend filters  
> - `rsi(df, period)` – optional overbought/oversold filter  
> Return all data as pandas DataFrames ready for signal generation.

---

## 🟩 Prompt 3 – Strategy Logic (Scalp-Fibo Core)

> Implement the **Scalp Fibo Logic** strategy in Python.  
> Core rules:
> 1️⃣ Use 1H → 15m trend filter (price above/below EMA200).  
> 2️⃣ On 5m and 1m charts, detect fast impulses and draw local Fibo retracement.  
> 3️⃣ Wait for price to correct into 0.382–0.618 zone in the direction of the main trend.  
> 4️⃣ Confirm entry with RSI reversal or bullish/bearish candle pattern.  
> 5️⃣ Entry trigger = breakout above/below short-term high/low.  
> 6️⃣ Stop-loss = just beyond 0.786 level.  
> 7️⃣ Position size = 10 % of deposit risk.  
> 8️⃣ Take-profit = staged: 0.236 / 0.0 / 1.272 Fibo extensions.  
> Include placeholders for order execution, Telegram alerts, and CSV logging.

---

## 🟩 Prompt 5 – Risk Control & Order Management

> Add full risk and order management to the Scalp Fibo Bot.  
> Implement:
> - Position sizing with max 10 % deposit risk.  
> - Market/limit orders with automatic stop-loss and take-profit placement.  
> - Partial exits at each Fibo target (0.236 / 0.0 / 1.272).  
> - Trailing stop once 1st target is reached.  
> - Daily trade count and loss limits to prevent overtrading.  
> - CSV logging of every action (timestamp, pair, entry, stop, qty, pnl).  
> - Telegram notifications for entry, exit, stop, and errors.

---

## 🟩 Prompt 6 – Automation & Backtesting

> Build automation and backtesting for the Scalp Fibo Bot.  
> 1️⃣ Continuous loop fetching 1m–5m candles and executing logic every tick.  
> 2️⃣ WebSocket integration for live updates and fast signal triggers.  
> 3️⃣ Backtest mode to simulate Fibo-based entries/exits using historical data (pandas or backtrader).  
> 4️⃣ Generate charts visualizing Fibo levels, entry points, and TP/SL.  
> 5️⃣ Log performance stats (win rate, drawdown, profit factor).  
> 6️⃣ Make code modular, Docker-ready, and able to switch between live and backtest mode via config.
