# ⚠️ MAINNET MODE - REAL MONEY TRADING

## 🔴 CRITICAL WARNING

You are now running in **MAINNET SPOT TRADING MODE**. This means:

- ✅ **REAL MONEY** will be used for trades
- ✅ **REAL PROFITS** and **REAL LOSSES** will occur
- ✅ All trades execute on the live BingX exchange
- ✅ Cannot be undone or reversed

---

## 🛡️ Safety Checklist

Before running the bot, verify:

### ✅ Account Setup
- [ ] BingX account is fully verified (KYC completed)
- [ ] 2FA (Two-Factor Authentication) is enabled
- [ ] API key has **only** these permissions:
  - ✅ Reading
  - ✅ Spot Trading
  - ❌ NO Withdrawal permissions
- [ ] IP whitelist is configured (optional but recommended)

### ✅ Bot Configuration
- [ ] Started with **small test trades** first
- [ ] Risk percentage is reasonable (currently: 10%)
- [ ] Daily loss limit is set (currently: 5%)
- [ ] Max daily trades is reasonable (currently: 10)
- [ ] Tested strategy logic thoroughly

### ✅ Monitoring
- [ ] Have Telegram notifications enabled
- [ ] Can monitor logs in real-time
- [ ] Understand how to stop the bot quickly
- [ ] Have alerts set for unusual activity

---

## 💰 Current Configuration

**Trading Mode:** Mainnet (LIVE)  
**Trading Type:** Spot  
**Symbol:** BTC-USDT  
**Risk per Trade:** 10%  
**Max Daily Trades:** 10  
**Max Daily Loss:** 5%  

---

## 🚨 Emergency Stop

### Method 1: Stop the bot
```bash
# If running in terminal
Ctrl+C

# If running in background
pkill -f "python bot.py"
```

### Method 2: Disable API key
1. Login to BingX
2. Go to API Management
3. Disable or delete the API key
4. Bot will stop immediately

---

## 📊 Monitor Your Bot

### View Live Logs
```bash
cd /home/ec2-user/bnx_bot_fiboscalp
tail -f logs/bot_$(date +%Y%m%d).log
```

### Check Trade History
```bash
cat logs/trades_$(date +%Y%m%d).csv
```

### Test Connection First
```bash
source venv/bin/activate
python test_api.py
```

---

## 💡 Best Practices

### Start Small
1. ✅ Test with minimum trade sizes first
2. ✅ Monitor for 24-48 hours
3. ✅ Gradually increase position sizes
4. ✅ Review performance regularly

### Risk Management
- Never risk more than you can afford to lose
- Keep majority of funds in cold storage
- Use only 20-30% of capital for automated trading
- Set conservative risk parameters
- Review daily P&L limits

### Strategy Validation
- Backtest thoroughly before going live
- Paper trade for at least 1 week
- Understand market conditions
- Know when to turn bot off (high volatility, news events)

---

## 🎯 Recommended Starting Settings

For your first live run, consider these safer settings:

```bash
# Edit .env file
RISK_PERCENT=2              # Lower risk (was 10%)
MAX_DAILY_TRADES=5          # Fewer trades (was 10)
MAX_DAILY_LOSS_PERCENT=2    # Tighter loss limit (was 5%)
```

Then gradually increase as you gain confidence.

---

## 📈 Performance Monitoring

Check these regularly:
- **Win Rate:** Should be > 40%
- **Profit Factor:** Should be > 1.5
- **Max Drawdown:** Should be < 20%
- **Daily P&L:** Track trends

---

## ⚙️ Spot Trading Differences

Spot trading is different from futures:

✅ **Pros:**
- No liquidation risk
- Can hold positions indefinitely
- Simpler to understand
- Lower risk than leverage

❌ **Limitations:**
- Can only go LONG (buy low, sell high)
- Cannot short sell (unless using margin)
- Requires buying full asset amount
- Lower profit potential vs futures

---

## 🔄 Switch Back to Testnet

To switch back to safe testnet mode:

```bash
cd /home/ec2-user/bnx_bot_fiboscalp
nano .env

# Change these lines:
TRADING_MODE=testnet
```

Then restart the bot.

---

## 📞 Support & Help

- Check logs: `logs/bot_YYYYMMDD.log`
- Review trades: `logs/trades_YYYYMMDD.csv`
- Test API: `python test_api.py`
- Read docs: `README.md`, `API_SETUP.md`

---

## ⚡ Quick Commands

```bash
# Check if bot is running
ps aux | grep "python bot.py"

# Stop bot
pkill -f "python bot.py"

# Start bot
cd /home/ec2-user/bnx_bot_fiboscalp
source venv/bin/activate
python bot.py

# View logs
tail -f logs/bot_*.log

# Check balance
python -c "from core import BingXClient; from config import Settings; \
c = BingXClient(Settings.BINGX_API_KEY, Settings.BINGX_SECRET_KEY, False, 'spot'); \
print(c.get_balance())"
```

---

## ✅ Final Check

Before running, answer YES to all:

- [ ] I understand this uses real money
- [ ] I have tested thoroughly
- [ ] I can afford potential losses
- [ ] I know how to stop the bot
- [ ] I will monitor actively
- [ ] API key has NO withdrawal permissions
- [ ] I'm starting with small positions

---

**🚀 Ready to proceed? Start the bot:**

```bash
cd /home/ec2-user/bnx_bot_fiboscalp
source venv/bin/activate
python bot.py
```

**Monitor carefully and good luck! 📊💰**
