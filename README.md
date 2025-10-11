# Fibo Scalp Bot for BingX

A sophisticated cryptocurrency scalping bot that uses Fibonacci retracement levels and multi-timeframe analysis for trading on BingX.

## Features

- **Multi-Timeframe Analysis**: Uses 1H, 15m, 5m, and 1m charts for trend confirmation
- **Fibonacci Retracement**: Automatically detects swing points and calculates Fibo levels
- **Risk Management**: 10% risk per trade with automatic stop-loss and take-profit levels
- **Staged Exits**: Partial profit-taking at multiple Fibonacci extension levels
- **Trailing Stop**: Moves stop to breakeven after first target is hit
- **Daily Limits**: Configurable max trades and loss limits per day
- **Telegram Notifications**: Real-time alerts for entries, exits, and errors
- **CSV Logging**: Detailed trade history for analysis
- **Backtesting**: Test strategies on historical data before going live
- **Docker Support**: Easy deployment with Docker and Docker Compose

## Strategy Overview

1. **Trend Filter**: Price above/below EMA200 on 1H and 15m timeframes
2. **Impulse Detection**: Fast price moves on 5m and 1m charts
3. **Fibonacci Retracement**: Wait for pullback into 0.382-0.618 zone
4. **Entry Confirmation**: RSI reversal or bullish/bearish candle pattern
5. **Entry Trigger**: Breakout above/below short-term high/low
6. **Stop Loss**: Just beyond 0.786 Fibonacci level
7. **Take Profit**: Staged exits at 0.236 / 0.0 / 1.272 extensions

## Installation

### Prerequisites

- Python 3.11+
- BingX account with API keys
- (Optional) Telegram bot token for notifications

### Setup

1. Navigate to project directory:
```bash
cd /home/ec2-user/bnx_bot_fiboscalp
```

2. Run automated setup:
```bash
./setup.sh
```
This installs all dependencies and creates your `.env` file.

3. Add your BingX API credentials:

**Interactive setup (recommended):**
```bash
./add_api_keys.sh
```

**Or manually edit .env:**
```bash
nano .env
```

Required credentials:
```bash
BINGX_API_KEY=your_actual_api_key
BINGX_SECRET_KEY=your_actual_secret_key
TRADING_MODE=testnet  # Use testnet for testing first!
```

**📖 Don't have API keys?** Check [API_SETUP.md](API_SETUP.md) for step-by-step instructions.

4. Test your API connection:
```bash
source venv/bin/activate
python test_api.py
```

## Usage

### Live Trading

Start the bot in live mode:
```bash
python bot.py
```

### Backtesting

Run backtests on historical data:
```bash
python -m core.backtester
```

### Docker Deployment

Build and run with Docker Compose:
```bash
cd docker
docker-compose up -d
```

View logs:
```bash
docker-compose logs -f
```

Stop the bot:
```bash
docker-compose down
```

## Configuration

All settings can be configured in `.env`:

- **Trading Parameters**: Symbol, risk percentage, daily limits
- **Strategy Parameters**: EMA periods, RSI levels, Fibonacci zones
- **Timeframes**: Which timeframes to use for analysis
- **API Endpoints**: Testnet vs Mainnet URLs

## Project Structure

```
bnx_bot_fiboscalp/
├── bot.py                      # Main bot entry point
├── core/
│   ├── __init__.py
│   ├── data_fetcher.py         # Market data and indicators
│   ├── strategy.py             # Fibo scalp strategy logic
│   ├── risk_manager.py         # Position sizing and order management
│   ├── logger.py               # Logging to CSV and console
│   ├── telegram_notifier.py    # Telegram notifications
│   └── backtester.py           # Backtesting engine
├── config/
│   ├── __init__.py
│   └── settings.py             # Configuration management
├── logs/                       # Trade logs and charts
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── requirements.txt
├── .env.template
└── README.md
```

## Risk Warning

**IMPORTANT**: Trading cryptocurrencies involves substantial risk of loss. This bot is provided for educational purposes only. Always:

- Start with testnet mode to verify functionality
- Use small position sizes when testing live
- Never risk more than you can afford to lose
- Monitor the bot regularly
- Understand the strategy before deploying

## Support

For issues, questions, or contributions, please open an issue in the repository.

## License

MIT License - See LICENSE file for details
