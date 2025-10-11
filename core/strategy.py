import pandas as pd
from typing import Dict, Optional, Tuple
from config.settings import Settings
from core.data_fetcher import DataFetcher

class FiboScalpStrategy:
    def __init__(self, data_fetcher: DataFetcher):
        self.data_fetcher = data_fetcher
        self.settings = Settings
        
    def check_trend_filter(self, df_1h: pd.DataFrame, df_15m: pd.DataFrame) -> Optional[str]:
        """
        Check if market is SIDEWAYS/RANGING (not trending)
        Returns: 'bullish' for upward range, 'bearish' for downward range, None if strong trend
        """
        if df_1h.empty or df_15m.empty:
            return None
        
        # Calculate price position relative to EMAs
        price_1h = df_1h['close'].iloc[-1]
        ema200_1h = df_1h['ema_200'].iloc[-1]
        ema50_1h = df_1h['ema_50'].iloc[-1]
        
        price_15m = df_15m['close'].iloc[-1]
        ema200_15m = df_15m['ema_200'].iloc[-1]
        ema50_15m = df_15m['ema_50'].iloc[-1]
        
        # Calculate distance from EMAs (percentage)
        dist_1h_200 = abs(price_1h - ema200_1h) / ema200_1h * 100
        dist_15m_200 = abs(price_15m - ema200_15m) / ema200_15m * 100
        
        # Check if EMAs are flat (sideways market indicator)
        ema200_slope_1h = (ema200_1h - df_1h['ema_200'].iloc[-5]) / df_1h['ema_200'].iloc[-5] * 100
        ema50_slope_1h = (ema50_1h - df_1h['ema_50'].iloc[-5]) / df_1h['ema_50'].iloc[-5] * 100
        
        # SIDEWAYS DETECTION:
        # 1. Price close to EMAs (not far away)
        # 2. EMAs are relatively flat (not steep)
        # 3. Mixed signals between timeframes
        
        is_sideways = False
        
        # Method 1: Price near EMAs on both timeframes (ranging)
        if dist_1h_200 < 1.5 and dist_15m_200 < 1.5:
            is_sideways = True
        
        # Method 2: Flat EMAs indicate consolidation
        if abs(ema200_slope_1h) < 0.5 and abs(ema50_slope_1h) < 1.0:
            is_sideways = True
        
        # Method 3: Mixed signals (no clear trend agreement)
        trend_1h = 'up' if price_1h > ema200_1h else 'down'
        trend_15m = 'up' if price_15m > ema200_15m else 'down'
        if trend_1h != trend_15m:
            is_sideways = True
        
        if not is_sideways:
            # Strong trend detected - skip trading
            return None
        
        # In sideways market, determine range direction
        # Use shorter-term price action
        recent_high = df_15m['high'].tail(20).max()
        recent_low = df_15m['low'].tail(20).min()
        current_position = (price_15m - recent_low) / (recent_high - recent_low)
        
        # Trade both directions in ranging market
        if current_position > 0.5:
            return 'bullish'  # Upper half of range, look for shorts (or long bounces)
        else:
            return 'bearish'  # Lower half of range, look for longs
        
        # Default: allow trading in sideways
        return 'bullish'
    
    def detect_fibo_setup(self, df: pd.DataFrame, trend: str) -> Optional[Dict]:
        """
        Detect Fibo retracement setup on lower timeframes
        Returns setup dict with Fibo levels and entry conditions
        """
        is_impulse, impulse_dir = self.data_fetcher.detect_impulse(df)
        
        if not is_impulse:
            return None
        
        if trend == 'bullish' and impulse_dir != 'up':
            return None
        if trend == 'bearish' and impulse_dir != 'down':
            return None
        
        swing_high, swing_low, _, _ = self.data_fetcher.get_swing_high_low(
            df, self.settings.SWING_LOOKBACK
        )
        
        if swing_high is None or swing_low is None:
            return None
        
        direction = 'up' if trend == 'bullish' else 'down'
        fibo_levels = self.data_fetcher.build_fibo_levels(swing_low, swing_high, direction)
        
        current_price = df['close'].iloc[-1]
        
        in_entry_zone = self._is_in_entry_zone(current_price, fibo_levels, direction)
        
        if not in_entry_zone:
            return None
        
        return {
            'direction': direction,
            'fibo_levels': fibo_levels,
            'swing_high': swing_high,
            'swing_low': swing_low,
            'current_price': current_price,
            'entry_zone': (fibo_levels['0.382'], fibo_levels['0.618'])
        }
    
    def _is_in_entry_zone(self, price: float, fibo_levels: Dict, direction: str) -> bool:
        """Check if price is in Fibonacci entry zone (0.382-0.618)"""
        fibo_382 = fibo_levels['0.382']
        fibo_618 = fibo_levels['0.618']
        
        if direction == 'up':
            return fibo_618 <= price <= fibo_382
        else:
            return fibo_382 <= price <= fibo_618
    
    def confirm_entry(self, df: pd.DataFrame, setup: Dict) -> Tuple[bool, str]:
        """
        Confirm entry with RSI reversal or candle pattern
        Returns: (should_enter, reason)
        """
        if len(df) < 3:
            return False, "Not enough data"
        
        direction = setup['direction']
        current_rsi = df['rsi'].iloc[-1]
        
        if pd.isna(current_rsi):
            return False, "RSI not available"
        
        if direction == 'up':
            if current_rsi < self.settings.RSI_OVERSOLD:
                rsi_reversal = current_rsi > df['rsi'].iloc[-2]
                if rsi_reversal:
                    return True, "RSI reversal from oversold"
            
            if self._is_bullish_candle(df):
                return True, "Bullish candle pattern"
        
        else:  # bearish
            if current_rsi > self.settings.RSI_OVERBOUGHT:
                rsi_reversal = current_rsi < df['rsi'].iloc[-2]
                if rsi_reversal:
                    return True, "RSI reversal from overbought"
            
            if self._is_bearish_candle(df):
                return True, "Bearish candle pattern"
        
        return False, "No confirmation"
    
    def _is_bullish_candle(self, df: pd.DataFrame) -> bool:
        """Check for bullish candle pattern"""
        last = df.iloc[-1]
        prev = df.iloc[-2]
        
        body = last['close'] - last['open']
        prev_body = prev['close'] - prev['open']
        
        if body > 0 and prev_body < 0:
            return True
        
        if body > 0 and body > abs(prev_body) * 1.5:
            return True
        
        return False
    
    def _is_bearish_candle(self, df: pd.DataFrame) -> bool:
        """Check for bearish candle pattern"""
        last = df.iloc[-1]
        prev = df.iloc[-2]
        
        body = last['close'] - last['open']
        prev_body = prev['close'] - prev['open']
        
        if body < 0 and prev_body > 0:
            return True
        
        if body < 0 and abs(body) > prev_body * 1.5:
            return True
        
        return False
    
    def check_entry_trigger(self, df: pd.DataFrame, setup: Dict) -> bool:
        """
        Check for entry trigger (breakout above/below short-term high/low)
        """
        if len(df) < 5:
            return False
        
        direction = setup['direction']
        current_price = df['close'].iloc[-1]
        
        recent_highs = df['high'].tail(5).iloc[:-1]
        recent_lows = df['low'].tail(5).iloc[:-1]
        
        if direction == 'up':
            short_term_high = recent_highs.max()
            if current_price > short_term_high:
                return True
        else:
            short_term_low = recent_lows.min()
            if current_price < short_term_low:
                return True
        
        return False
    
    def calculate_stop_loss(self, setup: Dict) -> float:
        """Calculate stop-loss level just beyond 0.786 Fibo"""
        fibo_levels = setup['fibo_levels']
        direction = setup['direction']
        
        fibo_786 = fibo_levels['0.786']
        
        if direction == 'up':
            stop_loss = fibo_786 * 0.998
        else:
            stop_loss = fibo_786 * 1.002
        
        return stop_loss
    
    def calculate_take_profits(self, setup: Dict, entry_price: float) -> Dict[str, float]:
        """Calculate staged take-profit levels"""
        fibo_levels = setup['fibo_levels']
        direction = setup['direction']
        
        tp_levels = {
            'tp1': fibo_levels[str(self.settings.TP1_FIBO)],
            'tp2': fibo_levels[str(self.settings.TP2_FIBO)],
            'tp3': fibo_levels[str(self.settings.TP3_FIBO)]
        }
        
        return tp_levels
    
    def generate_signal(self, market_data: Dict[str, pd.DataFrame]) -> Optional[Dict]:
        """
        Main signal generation logic - SIDEWAYS/RANGING market focus
        Returns trade signal dict or None
        """
        df_1h = market_data.get('1h')
        df_15m = market_data.get('15m')
        df_5m = market_data.get('5m')
        df_1m = market_data.get('1m')
        
        if any(df is None or df.empty for df in [df_1h, df_15m, df_5m, df_1m]):
            return None
        
        # Check for sideways market (returns None if strong trend)
        market_condition = self.check_trend_filter(df_1h, df_15m)
        if market_condition is None:
            return None  # Skip if strong trending market
        
        setup_5m = self.detect_fibo_setup(df_5m, market_condition)
        setup_1m = self.detect_fibo_setup(df_1m, market_condition)
        
        setup = setup_5m or setup_1m
        if setup is None:
            return None
        
        df_signal = df_1m if setup_1m else df_5m
        
        should_enter, reason = self.confirm_entry(df_signal, setup)
        if not should_enter:
            return None
        
        entry_triggered = self.check_entry_trigger(df_signal, setup)
        if not entry_triggered:
            return None
        
        entry_price = setup['current_price']
        stop_loss = self.calculate_stop_loss(setup)
        take_profits = self.calculate_take_profits(setup, entry_price)
        
        signal = {
            'direction': setup['direction'],
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'take_profits': take_profits,
            'fibo_levels': setup['fibo_levels'],
            'reason': reason,
            'timeframe': '1m' if setup_1m else '5m'
        }
        
        return signal
