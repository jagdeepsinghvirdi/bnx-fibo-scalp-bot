#!/usr/bin/env python3
"""
Demo/Paper Trading Mode
Shows simulated orders for testing without real money
"""

import time
import signal
import sys
from datetime import datetime
from core.data_fetcher import DataFetcher
from core.strategy import FiboScalpStrategy
from core.logger import TradeLogger
from config import Settings

class DemoBot:
    def __init__(self):
        self.logger = TradeLogger()
        self.data_fetcher = DataFetcher()
        self.strategy = FiboScalpStrategy(self.data_fetcher)
        
        self.running = False
        self.symbol = Settings.SYMBOL
        self.timeframes = Settings.TIMEFRAMES
        self.demo_balance = 1000.0  # $1000 virtual balance
        self.trades = []
        
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, sig, frame):
        self.logger.info("Shutting down demo bot...")
        self.running = False
        sys.exit(0)
    
    def start(self):
        self.running = True
        print("="*70)
        print("🎮 DEMO MODE - PAPER TRADING")
        print("="*70)
        print(f"Virtual Balance: ${self.demo_balance:,.2f}")
        print(f"Symbol: {self.symbol}")
        print(f"Strategy: Relaxed parameters for more signals")
        print("="*70)
        print()
        
        self.run_loop()
    
    def run_loop(self):
        iteration = 0
        
        while self.running:
            try:
                iteration += 1
                print(f"\n{'='*70}")
                print(f"📊 Iteration {iteration} - {datetime.now().strftime('%H:%M:%S')}")
                print(f"{'='*70}")
                
                market_data = self.data_fetcher.get_market_data(self.symbol, self.timeframes)
                
                if not market_data:
                    print("⚠️  No market data")
                    time.sleep(60)
                    continue
                
                # Show current price
                df_1m = market_data.get('1m')
                if df_1m is not None and not df_1m.empty:
                    current_price = df_1m['close'].iloc[-1]
                    print(f"💰 Current Price: ${current_price:,.2f}")
                
                # Check trend
                df_1h = market_data.get('1h')
                df_15m = market_data.get('15m')
                
                if df_1h is not None and df_15m is not None:
                    trend = self.strategy.check_trend_filter(df_1h, df_15m)
                    print(f"📈 Trend: {trend.upper() if trend else 'NEUTRAL'}")
                    
                    if trend:
                        # Check for any setup (relaxed)
                        df_5m = market_data.get('5m')
                        df_1m = market_data.get('1m')
                        
                        # Detect any price movement
                        if df_5m is not None and not df_5m.empty:
                            price_change_5m = ((df_5m['close'].iloc[-1] - df_5m['close'].iloc[-5]) / df_5m['close'].iloc[-5]) * 100
                            print(f"📊 5m Change: {price_change_5m:+.2f}%")
                        
                        # Generate signal with original strategy
                        signal = self.strategy.generate_signal(market_data)
                        
                        if signal:
                            print(f"\n🎯 SIGNAL DETECTED!")
                            print(f"   Direction: {signal['direction'].upper()}")
                            print(f"   Entry: ${signal['entry_price']:,.2f}")
                            print(f"   Stop Loss: ${signal['stop_loss']:,.2f}")
                            print(f"   TP1: ${signal['take_profits']['tp1']:,.2f}")
                            print(f"   TP2: ${signal['take_profits']['tp2']:,.2f}")
                            print(f"   TP3: ${signal['take_profits']['tp3']:,.2f}")
                            print(f"   Reason: {signal['reason']}")
                            
                            # Simulate order
                            position_size = self.calculate_position_size(signal)
                            
                            print(f"\n💵 DEMO ORDER PLACED:")
                            print(f"   Size: ${position_size:,.2f} ({position_size/signal['entry_price']:.6f} BTC)")
                            print(f"   Virtual Balance: ${self.demo_balance:,.2f}")
                            
                            self.trades.append({
                                'time': datetime.now(),
                                'signal': signal,
                                'size': position_size
                            })
                        else:
                            print("⏳ No signal - waiting for Fibonacci setup...")
                    else:
                        print("⏳ Waiting for clear trend...")
                
                # Show stats
                if self.trades:
                    print(f"\n📊 Session Stats:")
                    print(f"   Signals found: {len(self.trades)}")
                    print(f"   Avg time between signals: {iteration / len(self.trades):.1f} minutes")
                
                print(f"\n⏰ Next check in 60 seconds...")
                time.sleep(60)
                
            except Exception as e:
                print(f"\n❌ Error: {e}")
                time.sleep(60)
    
    def calculate_position_size(self, signal):
        risk_amount = self.demo_balance * (Settings.RISK_PERCENT / 100)
        price_risk = abs(signal['entry_price'] - signal['stop_loss'])
        return risk_amount / price_risk if price_risk > 0 else 0

def main():
    print("\n" + "="*70)
    print("⚠️  DEMO MODE - NO REAL TRADING")
    print("="*70)
    print("This mode:")
    print("✓ Shows what the bot sees")
    print("✓ Simulates orders (no real execution)")
    print("✓ Uses virtual $1000 balance")
    print("✓ Great for testing and learning")
    print("="*70)
    input("\nPress Enter to start demo mode...")
    
    bot = DemoBot()
    bot.start()

if __name__ == '__main__':
    main()
