# Quick Start Guide

## Setup in 5 Minutes

### 1. Run Setup Script
```bash
cd /home/ec2-user/bnx_bot_fiboscalp
./setup.sh
```

### 2. Add Your API Keys

**Option A: Interactive Setup (Recommended)**
```bash
./add_api_keys.sh
```
This will guide you through adding your BingX API keys step-by-step.

**Option B: Manual Edit**
```bash
nano .env
```

**Minimum required settings:**
```
BINGX_API_KEY=your_actual_api_key_here
BINGX_SECRET_KEY=your_actual_secret_key_here
TRADING_MODE=testnet
SYMBOL=BTC-USDT
```

**📖 Need API keys?** See [API_SETUP.md](API_SETUP.md) for detailed instructions.

### 2b. Test API Connection
```bash
source venv/bin/activate
python test_api.py
```
This verifies your API keys are working correctly.

### 3. Test with Backtest (Optional but Recommended)
```bash
source venv/bin/activate
python -m core.backtester
```

### 4. Run Live Bot
```bash
source venv/bin/activate
python bot.py
```

## Using Docker

### Build and Run
```bash
cd docker
docker-compose up -d
```

### View Logs
```bash
docker-compose logs -f
```

### Stop Bot
```bash
docker-compose down
```

## Important Notes

- **Always start with testnet mode** to verify everything works
- Check logs in the `logs/` directory
- Monitor Telegram for real-time notifications
- The bot runs continuously, checking for signals every 60 seconds

## Strategy Summary

- **Timeframes**: 1H (trend) → 15m (confirmation) → 5m/1m (entry)
- **Entry**: Fibonacci retracement 0.382-0.618 zone
- **Stop Loss**: Beyond 0.786 level
- **Take Profit**: 3 levels at 0.236 / 0.0 / 1.272 extensions
- **Risk**: 10% per trade (configurable)

## Getting BingX API Keys

1. Login to BingX account
2. Go to API Management
3. Create new API key with trading permissions
4. Save API Key and Secret Key
5. For testnet, use testnet.bingx.com

## Troubleshooting

**"Module not found" errors:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**"BingX API error":**
- Check API keys are correct
- Verify trading permissions enabled
- Ensure sufficient balance

**Bot not generating signals:**
- Market conditions may not match strategy criteria
- Check logs for detailed information
- Verify timeframe data is being fetched

## Support

Check logs for detailed error messages:
- Console output
- `logs/bot_YYYYMMDD.log`
- `logs/trades_YYYYMMDD.csv`
