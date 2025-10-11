import pandas as pd
from typing import Dict, Optional
from datetime import datetime, timedelta
from core.bingx_client import BingXClient
from config.settings import Settings

class RiskManager:
    def __init__(self, api_key: str = None, secret_key: str = None):
        self.api_key = api_key or Settings.BINGX_API_KEY
        self.secret_key = secret_key or Settings.BINGX_SECRET_KEY
        demo = Settings.TRADING_MODE == 'testnet'
        trading_type = Settings.TRADING_TYPE
        self.client = BingXClient(self.api_key, self.secret_key, demo=demo, trading_type=trading_type)
        
        self.daily_trades = 0
        self.daily_pnl = 0.0
        self.last_reset_date = datetime.now().date()
        
        self.active_positions = {}
        self.trailing_stops = {}
    
    def reset_daily_counters(self):
        """Reset daily trade counters"""
        today = datetime.now().date()
        if today > self.last_reset_date:
            self.daily_trades = 0
            self.daily_pnl = 0.0
            self.last_reset_date = today
    
    def can_trade(self) -> tuple[bool, str]:
        """Check if trading is allowed based on daily limits"""
        self.reset_daily_counters()
        
        if self.daily_trades >= Settings.MAX_DAILY_TRADES:
            return False, f"Max daily trades reached ({Settings.MAX_DAILY_TRADES})"
        
        if self.daily_pnl < 0:
            loss_pct = abs(self.daily_pnl / self.get_account_balance() * 100)
            if loss_pct >= Settings.MAX_DAILY_LOSS_PERCENT:
                return False, f"Max daily loss reached ({Settings.MAX_DAILY_LOSS_PERCENT}%)"
        
        return True, "Trading allowed"
    
    def get_account_balance(self) -> float:
        """Get account balance"""
        try:
            account = self.client.get_balance()
            if isinstance(account, dict):
                balance = account.get('balance', {})
                if isinstance(balance, dict):
                    return float(balance.get('balance', 0))
                elif isinstance(balance, list) and len(balance) > 0:
                    return float(balance[0].get('balance', 0))
            return 0.0
        except Exception as e:
            print(f"Error getting balance: {e}")
            return 0.0
    
    def calculate_position_size(self, entry_price: float, stop_loss: float, balance: float = None) -> float:
        """
        Calculate position size based on risk percentage
        Risk = balance * risk_pct / 100
        Position size = Risk / (entry_price - stop_loss)
        """
        if balance is None:
            balance = self.get_account_balance()
        
        if balance == 0:
            return 0.0
        
        risk_amount = balance * (Settings.RISK_PERCENT / 100)
        
        price_risk = abs(entry_price - stop_loss)
        if price_risk == 0:
            return 0.0
        
        position_size = risk_amount / price_risk
        
        return position_size
    
    def place_market_order(self, symbol: str, side: str, quantity: float) -> Optional[Dict]:
        """Place market order"""
        try:
            order = self.client.create_order(
                symbol=symbol,
                side=side.upper(),
                type='MARKET',
                quantity=quantity
            )
            return order
        except Exception as e:
            print(f"Error placing market order: {e}")
            return None
    
    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float) -> Optional[Dict]:
        """Place limit order"""
        try:
            order = self.client.create_order(
                symbol=symbol,
                side=side.upper(),
                type='LIMIT',
                quantity=quantity,
                price=price,
                timeInForce='GTC'
            )
            return order
        except Exception as e:
            print(f"Error placing limit order: {e}")
            return None
    
    def place_stop_loss(self, symbol: str, side: str, quantity: float, stop_price: float) -> Optional[Dict]:
        """Place stop-loss order"""
        try:
            stop_side = 'SELL' if side == 'BUY' else 'BUY'
            order = self.client.create_order(
                symbol=symbol,
                side=stop_side,
                type='STOP_MARKET',
                quantity=quantity,
                stopPrice=stop_price
            )
            return order
        except Exception as e:
            print(f"Error placing stop-loss: {e}")
            return None
    
    def place_take_profit(self, symbol: str, side: str, quantity: float, tp_price: float) -> Optional[Dict]:
        """Place take-profit order"""
        try:
            tp_side = 'SELL' if side == 'BUY' else 'BUY'
            order = self.client.create_order(
                symbol=symbol,
                side=tp_side,
                type='TAKE_PROFIT_MARKET',
                quantity=quantity,
                stopPrice=tp_price
            )
            return order
        except Exception as e:
            print(f"Error placing take-profit: {e}")
            return None
    
    def execute_trade(self, signal: Dict, symbol: str) -> Optional[Dict]:
        """Execute full trade with entry, stop-loss, and take-profits"""
        can_trade, reason = self.can_trade()
        if not can_trade:
            print(f"Cannot trade: {reason}")
            return None
        
        balance = self.get_account_balance()
        entry_price = signal['entry_price']
        stop_loss = signal['stop_loss']
        direction = signal['direction']
        
        position_size = self.calculate_position_size(entry_price, stop_loss, balance)
        
        if position_size == 0:
            print("Position size is 0")
            return None
        
        side = 'BUY' if direction == 'up' else 'SELL'
        
        entry_order = self.place_market_order(symbol, side, position_size)
        if not entry_order:
            return None
        
        self.place_stop_loss(symbol, side, position_size, stop_loss)
        
        take_profits = signal['take_profits']
        
        # NEW: If position > 0.1 contracts, place breakeven order for half
        breakeven_order_placed = False
        if position_size > 0.1:
            half_position = position_size / 2
            # Place limit order at entry price (breakeven) for half position
            breakeven_order = self.place_limit_order(
                symbol, 
                'SELL' if side == 'BUY' else 'BUY',  # Opposite side to close
                half_position, 
                entry_price
            )
            if breakeven_order:
                print(f"✅ Breakeven order placed: {half_position:.6f} contracts at ${entry_price:.2f}")
                breakeven_order_placed = True
            
            # Adjust TP quantities to work with remaining half
            if breakeven_order_placed:
                # TPs apply to remaining half after breakeven
                tp1_qty = half_position * (Settings.TP1_PERCENT / 100)
                tp2_qty = half_position * (Settings.TP2_PERCENT / 100)
                tp3_qty = half_position * (Settings.TP3_PERCENT / 100)
            else:
                # Use full position if breakeven order failed
                tp1_qty = position_size * (Settings.TP1_PERCENT / 100)
                tp2_qty = position_size * (Settings.TP2_PERCENT / 100)
                tp3_qty = position_size * (Settings.TP3_PERCENT / 100)
        else:
            # Normal TP allocation for positions <= 0.1
            tp1_qty = position_size * (Settings.TP1_PERCENT / 100)
            tp2_qty = position_size * (Settings.TP2_PERCENT / 100)
            tp3_qty = position_size * (Settings.TP3_PERCENT / 100)
        
        self.place_take_profit(symbol, side, tp1_qty, take_profits['tp1'])
        self.place_take_profit(symbol, side, tp2_qty, take_profits['tp2'])
        self.place_take_profit(symbol, side, tp3_qty, take_profits['tp3'])
        
        self.daily_trades += 1
        
        trade_info = {
            'timestamp': datetime.now(),
            'symbol': symbol,
            'direction': direction,
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'position_size': position_size,
            'breakeven_order_placed': breakeven_order_placed,
            'take_profits': take_profits,
            'entry_order': entry_order,
            'signal': signal
        }
        
        self.active_positions[symbol] = trade_info
        
        return trade_info
    
    def partial_exit(self, symbol: str, exit_price: float, percentage: float) -> bool:
        """Execute partial exit"""
        if symbol not in self.active_positions:
            return False
        
        position = self.active_positions[symbol]
        remaining_qty = position['position_size']
        exit_qty = remaining_qty * (percentage / 100)
        
        side = 'SELL' if position['direction'] == 'up' else 'BUY'
        order = self.place_market_order(symbol, side, exit_qty)
        
        if order:
            position['position_size'] -= exit_qty
            
            pnl = self._calculate_pnl(position['entry_price'], exit_price, exit_qty, position['direction'])
            self.daily_pnl += pnl
            
            return True
        
        return False
    
    def _calculate_pnl(self, entry_price: float, exit_price: float, quantity: float, direction: str) -> float:
        """Calculate PnL for a trade"""
        if direction == 'up':
            return (exit_price - entry_price) * quantity
        else:
            return (entry_price - exit_price) * quantity
    
    def update_trailing_stop(self, symbol: str, current_price: float):
        """Update trailing stop after first target is hit"""
        if symbol not in self.active_positions:
            return
        
        position = self.active_positions[symbol]
        direction = position['direction']
        entry_price = position['entry_price']
        
        if symbol not in self.trailing_stops:
            if direction == 'up' and current_price >= position['take_profits']['tp1']:
                self.trailing_stops[symbol] = entry_price
            elif direction == 'down' and current_price <= position['take_profits']['tp1']:
                self.trailing_stops[symbol] = entry_price
        else:
            if direction == 'up':
                new_stop = current_price * 0.995
                if new_stop > self.trailing_stops[symbol]:
                    self.trailing_stops[symbol] = new_stop
            else:
                new_stop = current_price * 1.005
                if new_stop < self.trailing_stops[symbol]:
                    self.trailing_stops[symbol] = new_stop
    
    def close_position(self, symbol: str, reason: str = "Manual close") -> bool:
        """Close entire position"""
        if symbol not in self.active_positions:
            return False
        
        position = self.active_positions[symbol]
        side = 'SELL' if position['direction'] == 'up' else 'BUY'
        
        order = self.place_market_order(symbol, side, position['position_size'])
        
        if order:
            del self.active_positions[symbol]
            if symbol in self.trailing_stops:
                del self.trailing_stops[symbol]
            
            print(f"Position closed: {symbol} - {reason}")
            return True
        
        return False
