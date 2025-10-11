#!/usr/bin/env python3
"""
Bot Status Dashboard
Shows current bot status, balance, and what it's waiting for
"""

import os
from datetime import datetime
from config import Settings
from core import DataFetcher, FiboScalpStrategy, BingXClient

def show_status():
    print("="*70)
    print(" 🤖 FIBO SCALP BOT STATUS DASHBOARD")
    print("="*70)
    print()
    
    # Check if bot is running
    import subprocess
    result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
    bot_running = 'python bot.py' in result.stdout
    
    print(f"Bot Status: {'🟢 RUNNING' if bot_running else '🔴 STOPPED'}")
    print(f"Mode: {Settings.TRADING_MODE.upper()}")
    print(f"Type: {Settings.TRADING_TYPE.upper()}")
    print(f"Symbol: {Settings.SYMBOL}")
    print()
    
    # Check balance
    print("-"*70)
    print("💰 ACCOUNT BALANCE")
    print("-"*70)
    
    client = BingXClient(
        Settings.BINGX_API_KEY,
        Settings.BINGX_SECRET_KEY,
        demo=(Settings.TRADING_MODE == 'testnet'),
        trading_type=Settings.TRADING_TYPE
    )
    
    balance = client.get_balance()
    if balance and 'balances' in balance:
        balances = balance['balances']
        if balances:
            for bal in balances:
                asset = bal.get('asset', 'Unknown')
                free = float(bal.get('free', 0))
                if free > 0:
                    print(f"  {asset}: {free:.8f}")
        else:
            print("  ⚠️  No funds in spot wallet")
    
    print()
    
    # Check market data
    print("-"*70)
    print("📊 CURRENT MARKET")
    print("-"*70)
    
    fetcher = DataFetcher()
    df = fetcher.get_klines(Settings.SYMBOL, '1m', 1)
    
    if not df.empty:
        price = df['close'].iloc[0]
        print(f"  Current Price: ${price:,.2f}")
    
    print()
    
    # Check strategy status
    print("-"*70)
    print("🎯 STRATEGY STATUS")
    print("-"*70)
    
    market_data = fetcher.get_market_data(Settings.SYMBOL, ['1h', '15m', '5m', '1m'])
    
    if market_data:
        strategy = FiboScalpStrategy(fetcher)
        
        # Check trend
        df_1h = market_data.get('1h')
        df_15m = market_data.get('15m')
        
        if df_1h is not None and df_15m is not None:
            trend = strategy.check_trend_filter(df_1h, df_15m)
            print(f"  Trend Direction: {trend.upper() if trend else 'NEUTRAL'}")
            
            if trend:
                # Check for setups
                setup_5m = strategy.detect_fibo_setup(market_data['5m'], trend)
                setup_1m = strategy.detect_fibo_setup(market_data['1m'], trend)
                
                print(f"  5m Fibo Setup: {'✓ Found' if setup_5m else '✗ Not found'}")
                print(f"  1m Fibo Setup: {'✓ Found' if setup_1m else '✗ Not found'}")
                
                if setup_5m or setup_1m:
                    setup = setup_5m or setup_1m
                    print()
                    print(f"  Setup Details:")
                    print(f"    Direction: {setup['direction']}")
                    print(f"    Entry Zone: ${setup['entry_zone'][0]:.2f} - ${setup['entry_zone'][1]:.2f}")
                    print(f"    Current Price: ${setup['current_price']:.2f}")
                else:
                    print()
                    print("  ⏳ Waiting for Fibonacci retracement setup...")
                    print("     - Need fast impulse move")
                    print("     - Then pullback to 0.382-0.618 zone")
                    print("     - Plus confirmation signal")
            else:
                print()
                print("  ⏳ Waiting for clear trend...")
                print("     - Need price above/below EMA200")
                print("     - On both 1H and 15m timeframes")
    
    print()
    
    # Check recent activity
    print("-"*70)
    print("📝 RECENT ACTIVITY")
    print("-"*70)
    
    log_file = f'logs/bot_{datetime.now().strftime("%Y%m%d")}.log'
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            lines = f.readlines()
            recent = lines[-10:] if len(lines) > 10 else lines
            
            if recent:
                print("  Last 10 log entries:")
                for line in recent:
                    if 'Iteration' in line or 'signal' in line.lower() or 'trade' in line.lower():
                        print(f"    {line.strip()}")
            else:
                print("  No recent activity")
    else:
        print("  No log file found")
    
    print()
    
    # Show what conditions are needed
    print("-"*70)
    print("⚙️  STRATEGY REQUIREMENTS")
    print("-"*70)
    print()
    print("  For a trade to execute, ALL must be true:")
    print("  1. ✓ Trend filter: Price above/below EMA200 on 1H and 15m")
    print("  2. ⏳ Impulse: Fast move on 5m or 1m (detected from swings)")
    print("  3. ⏳ Retracement: Price pulls back to 0.382-0.618 Fibo zone")
    print("  4. ⏳ Confirmation: RSI reversal OR bullish/bearish candle")
    print("  5. ⏳ Trigger: Breakout above/below short-term high/low")
    print("  6. ⚠️  Balance: Enough USDT for minimum order size")
    print()
    print("  ⚠️  IMPORTANT: Your balance is very small ($6.67 USDT)")
    print("     - BingX minimum order: ~$10-20 USDT")
    print("     - Even if signal appears, order may be rejected")
    print("     - Recommend: Add at least $50-100 USDT")
    print()
    
    print("="*70)
    print()
    print("To watch live: tail -f logs/bot_live.log")
    print("To stop bot:   pkill -f 'python bot.py'")
    print()

if __name__ == '__main__':
    show_status()
