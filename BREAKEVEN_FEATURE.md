# Breakeven Order Feature

## 🎯 Automatic Risk Reduction

**NEW FEATURE:** When position size exceeds 0.1 contracts, the bot automatically places a breakeven order for half the position.

---

## 📊 How It Works

### **Trigger Condition:**
```
IF position_size > 0.1 contracts:
    Place limit order for 50% at entry price
```

### **What Happens:**

**Example Trade:**
```
Entry: $112,000
Position Size: 0.15 BTC
Stop Loss: $111,500

✅ Position > 0.1, so:
→ Half position (0.075 BTC) limit order at $112,000
→ Remaining half (0.075 BTC) follows normal TP strategy
```

---

## 💡 Benefits

### **1. Risk-Free Position Faster**
Once price returns to entry, you automatically secure 50% with zero loss.

### **2. Psychological Comfort**
Knowing half will close at breakeven reduces stress.

### **3. Better Risk Management**
- If trade goes against you: 50% closes at breakeven, 50% hits stop
- Reduces max loss by 25%

### **4. Still Allows Profit**
Remaining 50% still has full profit potential with 3 TPs.

---

## 📈 Order Structure Comparison

### **WITHOUT Breakeven Feature (Position ≤ 0.1):**
```
Entry: $112,000 (0.08 BTC)
Orders:
- Stop Loss: 0.08 BTC @ $111,500
- TP1: 30% @ $112,300
- TP2: 40% @ $112,600  
- TP3: 30% @ $113,200

Max Loss: $40 (0.08 × $500)
```

### **WITH Breakeven Feature (Position > 0.1):**
```
Entry: $112,000 (0.15 BTC)
Orders:
- Breakeven: 0.075 BTC @ $112,000 (LIMIT)
- Stop Loss: 0.15 BTC @ $111,500
- TP1: 30% of remaining @ $112,300
- TP2: 40% of remaining @ $112,600
- TP3: 30% of remaining @ $113,200

Scenarios:
1. Price returns to $112k: 
   → 0.075 BTC closes at breakeven ($0 loss)
   → Only 0.075 BTC at risk
   → Max loss reduced to $37.50

2. Price goes straight to TP:
   → Breakeven order doesn't fill
   → Full position takes profits normally
```

---

## 🔄 Trade Flow

### **Step 1: Entry Execution**
```python
position_size = 0.15 BTC  # Calculated from risk %
entry_price = $112,000

# Check position size
if position_size > 0.1:
    place_breakeven_order()
```

### **Step 2: Breakeven Order Placed**
```
LIMIT SELL Order:
Quantity: 0.075 BTC (50%)
Price: $112,000 (entry price)
Type: LIMIT - Good Till Cancelled

Status: PENDING
Waits for price to return to entry
```

### **Step 3A: Price Retraces to Entry**
```
Price touches $112,000
→ Breakeven order FILLS
→ 50% closed with $0 P&L
→ Remaining 50% still active
→ All TPs now apply to remaining half
```

### **Step 3B: Price Moves to Profit**
```
Price never returns to $112,000
→ Breakeven order stays PENDING
→ Full position moves to TPs
→ TP1 fills → Cancel breakeven order
→ Normal exit strategy continues
```

---

## 💰 Risk Reduction Examples

### **Example 1: Trade Goes Against You**

**Without Breakeven:**
```
Entry: $112,000 × 0.15 BTC
Price drops to $111,500
Stop Loss hits
Loss: $75
```

**With Breakeven:**
```
Entry: $112,000 × 0.15 BTC
Price retraces to $112,000 → 0.075 closes
Price then drops to $111,500
Stop Loss hits remaining 0.075 BTC
Loss: $37.50 (50% reduction!)
```

### **Example 2: Volatile Market**

**Without Breakeven:**
```
Entry: $112,000
Price: $112,500 (+$75 unrealized)
Price drops back to $111,800
Stop Loss: $111,500
You're sweating...
```

**With Breakeven:**
```
Entry: $112,000
Price: $112,500 (+$75 unrealized)
Price drops to $112,000
→ Half closes at breakeven
→ You're now risk-free on 50%
→ Much less stress
```

---

## ⚙️ Configuration

### **Threshold Setting:**
```python
# In risk_manager.py
BREAKEVEN_THRESHOLD = 0.1  # contracts

if position_size > BREAKEVEN_THRESHOLD:
    place_breakeven_order()
```

### **To Adjust Threshold:**
You can modify the threshold in the code or add to `.env`:
```bash
# Future enhancement
BREAKEVEN_THRESHOLD=0.1
```

---

## 🔔 Notifications

### **When Breakeven Order Placed:**
You'll receive Telegram notification:
```
🟢 ENTRY SIGNAL

Symbol: BTC-USDT
Direction: LONG
Entry Price: $112,000.00
Position Size: 0.1500

🎯 Breakeven Order Active
50% (0.0750) will close at entry price

Take Profits:
• TP1: $112,300
• TP2: $112,600
• TP3: $113,200
```

### **When Breakeven Order Fills:**
```
💚 Breakeven Hit

Symbol: BTC-USDT
Closed: 0.0750 BTC @ $112,000
P&L: $0.00
Remaining: 0.0750 BTC
```

---

## 📊 Statistics Impact

### **Expected Changes:**

**Win Rate:**
- May slightly decrease (more BE exits)
- But lower overall risk

**Average Win:**
- May decrease (some half-exits)
- But more consistent

**Average Loss:**
- Should decrease significantly
- Better risk/reward

**Profit Factor:**
- Should improve
- Reduced losses > reduced wins

**Max Drawdown:**
- Should decrease
- Better capital preservation

---

## 🎓 Strategy Considerations

### **When Breakeven Helps:**
1. ✅ Volatile/choppy markets
2. ✅ Unclear momentum
3. ✅ Want to reduce stress
4. ✅ Conservative trading
5. ✅ Larger position sizes

### **When It Might Not Help:**
1. ⚠️ Strong trending moves (misses full profit)
2. ⚠️ Very small positions (not triggered)
3. ⚠️ If price gaps past entry on return

### **Best Use Cases:**
- Position sizes 0.1 - 1.0 BTC
- Ranging/sideways markets
- When you want to "lock in" zero risk
- Scalping strategies
- Risk-averse trading

---

## 🔧 Technical Details

### **Order Type:**
```
Type: LIMIT order (not MARKET)
Price: Exact entry price
Quantity: 50% of position
Time In Force: GTC (Good Till Cancelled)
Side: Opposite of entry (SELL for longs, BUY for shorts)
```

### **Order Management:**
```python
# Placed immediately after entry
breakeven_order = place_limit_order(
    symbol='BTC-USDT',
    side='SELL',  # Opposite of entry
    quantity=position_size / 2,
    price=entry_price
)

# Tracks in position info
trade_info['breakeven_order_placed'] = True

# Should be cancelled if:
- First TP is hit (price moved in profit)
- Stop loss is hit
- Manual position close
```

---

## 📈 Example Scenarios

### **Scenario 1: Perfect Range Trade**
```
Entry: $112,000 (0.15 BTC long)
Market: Ranging $111,500 - $113,000

Timeline:
09:00 - Entry @ $112,000
      - Breakeven order placed: 0.075 @ $112,000
09:15 - Price rises to $112,500
09:30 - Price drops to $112,000
      - Breakeven order FILLS (0.075 BTC)
      - Remaining: 0.075 BTC
09:45 - Price drops to $111,500
      - Stop loss hits remaining 0.075
      
Result: Loss = $37.50 (instead of $75)
```

### **Scenario 2: Strong Move to Profit**
```
Entry: $112,000 (0.15 BTC long)
Market: Strong uptrend

Timeline:
09:00 - Entry @ $112,000
      - Breakeven order placed: 0.075 @ $112,000
09:05 - Price rises to $112,300
      - TP1 fills (30% of remaining)
      - Cancel breakeven order
09:10 - Price rises to $112,600
      - TP2 fills
09:20 - Price rises to $113,200
      - TP3 fills
      
Result: Full profit on entire position
```

---

## ✅ Summary

**Breakeven Feature = Automatic Risk Reduction**

- Activates when position > 0.1 contracts
- Closes 50% at entry price
- Reduces max loss by ~25%
- Still allows full profit potential
- Provides psychological comfort
- Better risk management
- Especially useful in ranging markets

**It's like having a safety net that automatically appears when you need it most!** 🎯
