# Spot Trading with BTC/USDT Guide

## 🎯 Understanding Your Options

### If you have **BTC** (Bitcoin):
- ✅ You can **SELL BTC** to get USDT
- ❌ You cannot buy more BTC (need USDT for that)
- The bot would only execute SHORT signals (sell orders)

### If you have **USDT** (Tether):
- ✅ You can **BUY BTC** with USDT
- ❌ You cannot sell BTC (need BTC for that)
- The bot would only execute LONG signals (buy orders)

### If you have **BOTH BTC and USDT**:
- ✅ You can buy AND sell BTC
- ✅ Bot can execute full strategy (both directions)
- ✅ Most flexible setup

---

## 📊 BTC-USDT Trading Pair Explained

**Trading Pair:** BTC-USDT means:
- **Base Asset:** BTC (what you're buying/selling)
- **Quote Asset:** USDT (what you're paying with)

### Example Trades:

**Buy Signal (LONG):**
- You need: USDT
- Action: BUY BTC with USDT
- Result: Your USDT → BTC
- Profit: When BTC price goes UP

**Sell Signal (SHORT in spot):**
- You need: BTC
- Action: SELL BTC for USDT  
- Result: Your BTC → USDT
- Profit: When you bought BTC lower, sell higher

---

## 🔍 Check Your Wallet Types

BingX has multiple wallet types. Your funds might be in:

### 1. **Spot Wallet** (for spot trading)
```bash
python check_balance.py
```

### 2. **Futures Wallet** (for futures/perpetual trading)
Different from spot, uses leverage

### 3. **Funding Wallet** (main deposit wallet)
Needs to be transferred to Spot/Futures

### 4. **Other Wallets**
- Earn wallet
- Copy trading wallet
- etc.

---

## 💡 What To Do Based on Your Situation

### Scenario 1: You have BTC in Futures Wallet
**Need to:** Transfer BTC from Futures → Spot wallet

**On BingX:**
1. Go to Wallet → Transfer
2. From: Futures → To: Spot
3. Asset: BTC
4. Amount: Your amount
5. Confirm

### Scenario 2: You have BTC in Funding Wallet
**Need to:** Transfer BTC from Funding → Spot wallet

**On BingX:**
1. Go to Wallet → Transfer
2. From: Funding → To: Spot
3. Asset: BTC
4. Amount: Your amount
5. Confirm

### Scenario 3: You want to trade with BTC you own
**Option A: Sell BTC for USDT first** (Recommended)
```
1. Manually sell some BTC for USDT on BingX
2. Use USDT for bot trading (can buy and sell)
```

**Option B: Configure bot for BTC holdings**
```
- Bot can only SELL when it has BTC
- Limited strategy (only downtrend trades)
```

### Scenario 4: You want to buy BTC
**Need:** USDT in spot wallet
```
1. Deposit USDT to BingX
2. Transfer to Spot wallet
3. Bot can buy BTC with USDT
```

---

## ⚙️ Bot Configuration for Your Assets

### Current Setup (BTC-USDT with USDT):
```bash
SYMBOL=BTC-USDT
TRADING_TYPE=spot
```
**Requirements:** Need USDT to BUY BTC

### If you have BTC and want to sell:
The bot can work, but will only execute when:
- Strategy signals SELL
- You have enough BTC for the position size

### If you have both BTC and USDT:
Bot can execute full strategy in both directions

---

## 🚀 Recommended Setup

### Best Option: Have USDT Ready
Why USDT is better for bot trading:
1. ✅ Can buy on bullish signals
2. ✅ Easier position sizing
3. ✅ More trading opportunities
4. ✅ Clearer profit tracking
5. ✅ Bot can enter AND exit positions

### How much USDT?
- **Minimum:** $100 USDT (for testing)
- **Comfortable:** $500-1000 USDT
- **Optimal:** Depends on risk tolerance

With 10% risk per trade:
- $500 balance = $50 risk per trade
- $1000 balance = $100 risk per trade

---

## 📝 Step-by-Step: Convert BTC to USDT

If you have BTC and want to use USDT for trading:

### On BingX Website:
1. Go to **Trade → Spot**
2. Select **BTC/USDT** pair
3. Choose **Sell**
4. Enter amount of BTC to sell
5. Use **Market Order** for instant execution
6. Confirm sale
7. You now have USDT!

### Then Check Balance:
```bash
cd /home/ec2-user/bnx_bot_fiboscalp
source venv/bin/activate
python check_balance.py
```

---

## 🔧 Alternative: Trade Different Pairs

If you have other assets, you can trade those:

### Edit .env:
```bash
# Examples:
SYMBOL=ETH-USDT    # If you have ETH or USDT
SYMBOL=BNB-USDT    # If you have BNB or USDT
SYMBOL=SOL-USDT    # If you have SOL or USDT
```

---

## ⚠️ Important Notes

### Spot Trading Limitations:
- ❌ Cannot short sell (sell what you don't own)
- ❌ No leverage (1x only)
- ✅ No liquidation risk
- ✅ Own the actual asset

### For Full Strategy:
The Fibonacci retracement bot works best with:
- USDT available to enter positions
- Ability to buy AND sell
- Multiple timeframe analysis

### Reality Check:
If you only have BTC:
- Bot will wait for SELL signals only
- May have long waiting periods
- Limited trading opportunities
- Consider converting some BTC to USDT

---

## 📞 Quick Commands

### Check what you have:
```bash
python check_balance.py
```

### Check current market price:
```bash
python -c "
from core import DataFetcher
df = DataFetcher().get_klines('BTC-USDT', '1m', 1)
print(f'BTC Price: \$' + str(df['close'].iloc[0]) + ' USDT')
"
```

### Start bot (when ready):
```bash
python bot.py
```

---

## 🎯 Summary

**You said you have "BTCUSDT fund":**

If this means:
1. **"I want to trade the BTC-USDT pair"** → Need USDT in wallet to buy
2. **"I have BTC coins"** → Can sell BTC, but need USDT to buy more
3. **"I have funds for BTC/USDT trading"** → Transfer to Spot wallet first

**Best action now:**
1. Check where your funds are (Spot/Futures/Funding wallet)
2. Transfer to Spot wallet if needed
3. Consider having USDT for full bot functionality
4. Start with small amounts for testing

**Ready to check your actual balance?**
```bash
python check_balance.py
```
