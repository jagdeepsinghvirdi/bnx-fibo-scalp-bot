# BingX API Setup Guide

## 🔑 How to Get BingX API Keys

### For Testnet (Recommended for Testing)

1. **Visit BingX Testnet:**
   - Go to: https://testnet.bingx.com/
   - Or: https://bingx-testnet.com/

2. **Create Testnet Account:**
   - Sign up with email
   - Complete verification

3. **Generate API Keys:**
   - Login to testnet account
   - Go to: Account → API Management
   - Click "Create API Key"
   - Save both:
     - API Key
     - Secret Key
   - Enable permissions:
     - ✅ Reading
     - ✅ Trading
     - ✅ Futures

4. **Get Testnet Funds:**
   - Use faucet to get test USDT
   - No real money needed

### For Mainnet (Live Trading)

1. **Visit BingX:**
   - Go to: https://bingx.com/

2. **Create Account:**
   - Sign up and complete KYC
   - Enable 2FA for security

3. **Generate API Keys:**
   - Login to account
   - Go to: User Center → API Management
   - Click "Create New Key"
   - Save both:
     - API Key
     - Secret Key
   - Enable permissions:
     - ✅ Reading
     - ✅ Trading
     - ✅ Enable Futures Trading

4. **IP Whitelist (Optional but Recommended):**
   - Add your server IP for extra security

---

## 📝 Add API Keys to Bot

### Method 1: Edit .env file directly

```bash
cd /home/ec2-user/bnx_bot_fiboscalp
nano .env
```

Replace these lines:
```bash
BINGX_API_KEY=your_api_key_here
BINGX_SECRET_KEY=your_secret_key_here
```

With your actual keys:
```bash
BINGX_API_KEY=your_actual_api_key_here
BINGX_SECRET_KEY=your_actual_secret_key_here
```

Save with: `Ctrl+X`, then `Y`, then `Enter`

### Method 2: Use environment variables (temporary)

```bash
export BINGX_API_KEY="YOUR_API_KEY"
export BINGX_SECRET_KEY="YOUR_SECRET_KEY"
```

---

## 🔔 Telegram Setup (Optional but Recommended)

### Get Telegram Bot Token

1. **Open Telegram**
2. **Find @BotFather**
3. **Create bot:**
   ```
   /newbot
   ```
4. **Follow prompts:**
   - Enter bot name
   - Enter username (must end with 'bot')
5. **Copy token** (looks like: `XXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXX`)

### Get Chat ID

1. **Start chat with @userinfobot**
2. **Send any message**
3. **Copy your Chat ID** (number like: `987654321`)

### Add to .env

```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

---

## ⚙️ Configuration Options

### Trading Mode

**Testnet (Safe for testing):**
```bash
TRADING_MODE=testnet
```

**Mainnet (Live trading):**
```bash
TRADING_MODE=mainnet
```

### Trading Parameters

```bash
SYMBOL=BTC-USDT              # Trading pair
RISK_PERCENT=10              # Risk per trade (default: 10%)
MAX_DAILY_TRADES=10          # Max trades per day
MAX_DAILY_LOSS_PERCENT=5     # Stop trading after this loss
```

### Strategy Parameters

```bash
EMA_FAST=50                  # Fast EMA period
EMA_SLOW=200                 # Slow EMA period
RSI_PERIOD=14                # RSI calculation period
SWING_LOOKBACK=20            # Bars to look back for swings
```

---

## ✅ Verify Configuration

Test that your API keys work:

```bash
cd /home/ec2-user/bnx_bot_fiboscalp
source venv/bin/activate
python -c "
from config import Settings
from core import BingXClient

client = BingXClient(
    Settings.BINGX_API_KEY,
    Settings.BINGX_SECRET_KEY,
    demo=(Settings.TRADING_MODE == 'testnet')
)

print('Testing API connection...')
balance = client.get_balance()
print('✓ API connection successful!')
print(f'Balance: {balance}')
"
```

If successful, you'll see your account balance!

---

## 🔒 Security Best Practices

### DO:
- ✅ Use testnet first
- ✅ Keep API keys secret
- ✅ Use read-only keys for testing
- ✅ Enable IP whitelist on mainnet
- ✅ Use 2FA on exchange account
- ✅ Store .env in secure location
- ✅ Never commit .env to git

### DON'T:
- ❌ Share API keys publicly
- ❌ Use mainnet without testing
- ❌ Give withdrawal permissions
- ❌ Use same keys on multiple bots
- ❌ Hardcode keys in source code

---

## 🚀 Ready to Run

Once API keys are configured:

```bash
cd /home/ec2-user/bnx_bot_fiboscalp
source venv/bin/activate

# Test with backtest first
python -m core.backtester

# Then run live bot
python bot.py
```

---

## 📞 Troubleshooting

### "Invalid API Key" Error
- Check for extra spaces in .env
- Verify key is copied correctly
- Check key permissions on BingX
- Ensure testnet keys for testnet mode

### "Signature Invalid" Error
- Check secret key is correct
- Verify no extra spaces or quotes
- Check system time is synchronized

### "Insufficient Balance" Error
- Verify you have funds in account
- For testnet, use faucet to get test funds
- Check you're using correct trading mode

---

## 📧 Need Help?

1. Check logs: `logs/bot_YYYYMMDD.log`
2. Verify .env configuration
3. Test API connection with verify script above
4. Check BingX API documentation
