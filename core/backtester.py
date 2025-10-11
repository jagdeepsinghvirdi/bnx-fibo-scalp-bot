import pandas as pd
import numpy as np
from typing import Dict, List
from datetime import datetime
import matplotlib.pyplot as plt
from core.data_fetcher import DataFetcher
from core.strategy import FiboScalpStrategy
from config.settings import Settings

class Backtester:
    def __init__(self, initial_balance: float = 10000):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.data_fetcher = DataFetcher()
        self.strategy = FiboScalpStrategy(self.data_fetcher)
        
        self.trades = []
        self.equity_curve = []
        self.positions = []
    
    def load_historical_data(self, symbol: str, timeframes: List[str], start_date: str, end_date: str) -> Dict:
        """Load historical data for backtesting"""
        print(f"Loading historical data for {symbol}...")
        
        market_data = {}
        for tf in timeframes:
            df = self.data_fetcher.get_klines(symbol, tf, limit=1000)
            if not df.empty:
                market_data[tf] = df
        
        return market_data
    
    def calculate_position_size(self, entry_price: float, stop_loss: float) -> float:
        """Calculate position size for backtest"""
        risk_amount = self.balance * (Settings.RISK_PERCENT / 100)
        price_risk = abs(entry_price - stop_loss)
        
        if price_risk == 0:
            return 0
        
        return risk_amount / price_risk
    
    def execute_backtest_trade(self, signal: Dict, timestamp: datetime):
        """Execute a single trade in backtest"""
        entry_price = signal['entry_price']
        stop_loss = signal['stop_loss']
        direction = signal['direction']
        take_profits = signal['take_profits']
        
        position_size = self.calculate_position_size(entry_price, stop_loss)
        
        if position_size == 0:
            return
        
        trade = {
            'entry_time': timestamp,
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'direction': direction,
            'position_size': position_size,
            'take_profits': take_profits,
            'status': 'open',
            'exit_time': None,
            'exit_price': None,
            'pnl': 0
        }
        
        self.positions.append(trade)
    
    def update_positions(self, current_data: Dict, timestamp: datetime):
        """Update open positions with current market data"""
        if not self.positions:
            return
        
        df_1m = current_data.get('1m')
        if df_1m is None or df_1m.empty:
            return
        
        current_price = df_1m['close'].iloc[-1]
        
        for trade in self.positions:
            if trade['status'] != 'open':
                continue
            
            direction = trade['direction']
            
            if direction == 'up':
                if current_price <= trade['stop_loss']:
                    self.close_trade(trade, trade['stop_loss'], timestamp, 'Stop Loss')
                elif current_price >= trade['take_profits']['tp3']:
                    self.close_trade(trade, trade['take_profits']['tp3'], timestamp, 'TP3')
                elif current_price >= trade['take_profits']['tp2']:
                    self.close_trade(trade, trade['take_profits']['tp2'], timestamp, 'TP2')
                elif current_price >= trade['take_profits']['tp1']:
                    self.close_trade(trade, trade['take_profits']['tp1'], timestamp, 'TP1')
            
            else:  # down
                if current_price >= trade['stop_loss']:
                    self.close_trade(trade, trade['stop_loss'], timestamp, 'Stop Loss')
                elif current_price <= trade['take_profits']['tp3']:
                    self.close_trade(trade, trade['take_profits']['tp3'], timestamp, 'TP3')
                elif current_price <= trade['take_profits']['tp2']:
                    self.close_trade(trade, trade['take_profits']['tp2'], timestamp, 'TP2')
                elif current_price <= trade['take_profits']['tp1']:
                    self.close_trade(trade, trade['take_profits']['tp1'], timestamp, 'TP1')
    
    def close_trade(self, trade: Dict, exit_price: float, timestamp: datetime, reason: str):
        """Close a trade and update balance"""
        trade['exit_price'] = exit_price
        trade['exit_time'] = timestamp
        trade['status'] = 'closed'
        trade['reason'] = reason
        
        if trade['direction'] == 'up':
            trade['pnl'] = (exit_price - trade['entry_price']) * trade['position_size']
        else:
            trade['pnl'] = (trade['entry_price'] - exit_price) * trade['position_size']
        
        self.balance += trade['pnl']
        self.trades.append(trade)
        self.equity_curve.append({
            'timestamp': timestamp,
            'balance': self.balance,
            'pnl': trade['pnl']
        })
    
    def run(self, symbol: str, timeframes: List[str], start_date: str = None, end_date: str = None):
        """Run backtest"""
        print("Starting backtest...")
        
        market_data = self.load_historical_data(symbol, timeframes, start_date, end_date)
        
        if not market_data:
            print("No data available for backtesting")
            return
        
        df_1m = market_data.get('1m')
        if df_1m is None or df_1m.empty:
            print("No 1m data available")
            return
        
        for i in range(len(df_1m)):
            timestamp = df_1m.index[i]
            
            current_data = {}
            for tf, df in market_data.items():
                current_data[tf] = df.loc[:timestamp]
            
            signal = self.strategy.generate_signal(current_data)
            
            if signal and len(self.positions) < 1:
                self.execute_backtest_trade(signal, timestamp)
            
            self.update_positions(current_data, timestamp)
        
        self.generate_report()
    
    def generate_report(self):
        """Generate backtest performance report"""
        print("\n" + "="*50)
        print("BACKTEST RESULTS")
        print("="*50)
        
        total_trades = len(self.trades)
        winning_trades = len([t for t in self.trades if t['pnl'] > 0])
        losing_trades = len([t for t in self.trades if t['pnl'] < 0])
        
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        total_profit = sum([t['pnl'] for t in self.trades if t['pnl'] > 0])
        total_loss = sum([t['pnl'] for t in self.trades if t['pnl'] < 0])
        
        net_profit = self.balance - self.initial_balance
        roi = (net_profit / self.initial_balance * 100) if self.initial_balance > 0 else 0
        
        profit_factor = abs(total_profit / total_loss) if total_loss != 0 else 0
        
        print(f"Initial Balance: ${self.initial_balance:.2f}")
        print(f"Final Balance: ${self.balance:.2f}")
        print(f"Net Profit: ${net_profit:.2f}")
        print(f"ROI: {roi:.2f}%")
        print(f"\nTotal Trades: {total_trades}")
        print(f"Winning Trades: {winning_trades}")
        print(f"Losing Trades: {losing_trades}")
        print(f"Win Rate: {win_rate:.2f}%")
        print(f"Profit Factor: {profit_factor:.2f}")
        
        if self.trades:
            avg_win = total_profit / winning_trades if winning_trades > 0 else 0
            avg_loss = total_loss / losing_trades if losing_trades > 0 else 0
            print(f"\nAverage Win: ${avg_win:.2f}")
            print(f"Average Loss: ${avg_loss:.2f}")
            
            max_win = max([t['pnl'] for t in self.trades])
            max_loss = min([t['pnl'] for t in self.trades])
            print(f"Max Win: ${max_win:.2f}")
            print(f"Max Loss: ${max_loss:.2f}")
        
        self.plot_equity_curve()
    
    def plot_equity_curve(self):
        """Plot equity curve"""
        if not self.equity_curve:
            return
        
        df = pd.DataFrame(self.equity_curve)
        
        plt.figure(figsize=(12, 6))
        plt.plot(df['timestamp'], df['balance'])
        plt.title('Equity Curve')
        plt.xlabel('Time')
        plt.ylabel('Balance ($)')
        plt.grid(True)
        plt.tight_layout()
        
        filename = f'logs/equity_curve_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
        plt.savefig(filename)
        print(f"\nEquity curve saved to {filename}")
        plt.close()

def main():
    """Run backtest"""
    backtester = Backtester(initial_balance=10000)
    backtester.run(
        symbol=Settings.SYMBOL,
        timeframes=Settings.TIMEFRAMES
    )

if __name__ == '__main__':
    main()
