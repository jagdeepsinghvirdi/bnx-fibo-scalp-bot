import pandas as pd
import numpy as np
from typing import Tuple, Dict, List
from core.bingx_client import BingXClient
from config.settings import Settings

class DataFetcher:
    def __init__(self, api_key: str = None, secret_key: str = None):
        self.api_key = api_key or Settings.BINGX_API_KEY
        self.secret_key = secret_key or Settings.BINGX_SECRET_KEY
        demo = Settings.TRADING_MODE == 'testnet'
        trading_type = Settings.TRADING_TYPE
        self.client = BingXClient(self.api_key, self.secret_key, demo=demo, trading_type=trading_type)
        
    def get_klines(self, symbol: str, interval: str, limit: int = 500) -> pd.DataFrame:
        """Fetch OHLCV candles from BingX"""
        try:
            klines = self.client.get_klines(symbol=symbol, interval=interval, limit=limit)
            
            if not klines:
                return pd.DataFrame()
            
            data = []
            for candle in klines:
                if isinstance(candle, dict):
                    # Dict format (futures)
                    data.append([
                        candle.get('time', 0),
                        float(candle.get('open', 0)),
                        float(candle.get('high', 0)),
                        float(candle.get('low', 0)),
                        float(candle.get('close', 0)),
                        float(candle.get('volume', 0))
                    ])
                elif isinstance(candle, list) and len(candle) >= 6:
                    # Array format (spot): [timestamp, open, high, low, close, volume, close_time, quote_volume]
                    data.append([
                        candle[0],  # timestamp
                        float(candle[1]),  # open
                        float(candle[2]),  # high
                        float(candle[3]),  # low
                        float(candle[4]),  # close
                        float(candle[5])   # volume
                    ])
            
            if not data:
                return pd.DataFrame()
            
            df = pd.DataFrame(data, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume'
            ])
            
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
            df.set_index('timestamp', inplace=True)
            
            return df
        except Exception as e:
            print(f"Error fetching klines: {e}")
            return pd.DataFrame()
    
    def get_swing_high_low(self, df: pd.DataFrame, lookback: int = 20) -> Tuple[float, float, int, int]:
        """
        Detect local swing high and low zones
        Returns: (swing_high, swing_low, high_index, low_index)
        """
        if len(df) < lookback:
            return None, None, None, None
        
        highs = df['high'].tail(lookback)
        lows = df['low'].tail(lookback)
        
        swing_high = highs.max()
        swing_low = lows.min()
        
        high_idx = highs.idxmax()
        low_idx = lows.idxmin()
        
        return swing_high, swing_low, high_idx, low_idx
    
    def build_fibo_levels(self, low: float, high: float, direction: str = 'up') -> Dict[str, float]:
        """
        Compute Fibonacci retracement levels
        direction: 'up' for uptrend (low to high), 'down' for downtrend (high to low)
        """
        diff = high - low
        
        if direction == 'up':
            levels = {
                '0.0': high,
                '0.236': high - 0.236 * diff,
                '0.382': high - 0.382 * diff,
                '0.5': high - 0.5 * diff,
                '0.618': high - 0.618 * diff,
                '0.786': high - 0.786 * diff,
                '1.0': low,
                '1.272': high + 0.272 * diff,  # Extension
                '1.618': high + 0.618 * diff   # Extension
            }
        else:  # down
            levels = {
                '0.0': low,
                '0.236': low + 0.236 * diff,
                '0.382': low + 0.382 * diff,
                '0.5': low + 0.5 * diff,
                '0.618': low + 0.618 * diff,
                '0.786': low + 0.786 * diff,
                '1.0': high,
                '1.272': low - 0.272 * diff,  # Extension
                '1.618': low - 0.618 * diff   # Extension
            }
        
        return levels
    
    def ema(self, df: pd.DataFrame, period: int, column: str = 'close') -> pd.Series:
        """Calculate Exponential Moving Average"""
        return df[column].ewm(span=period, adjust=False).mean()
    
    def rsi(self, df: pd.DataFrame, period: int = 14, column: str = 'close') -> pd.Series:
        """Calculate Relative Strength Index"""
        delta = df[column].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def get_market_data(self, symbol: str, timeframes: List[str]) -> Dict[str, pd.DataFrame]:
        """Fetch data for multiple timeframes"""
        market_data = {}
        
        for tf in timeframes:
            df = self.get_klines(symbol, tf)
            if not df.empty:
                df['ema_50'] = self.ema(df, Settings.EMA_FAST)
                df['ema_200'] = self.ema(df, Settings.EMA_SLOW)
                df['rsi'] = self.rsi(df, Settings.RSI_PERIOD)
                market_data[tf] = df
        
        return market_data
    
    def detect_impulse(self, df: pd.DataFrame, min_candles: int = 3, min_pct: float = 0.25) -> Tuple[bool, str]:
        """
        Detect fast impulse move (RELAXED: 0.25% instead of 0.5%)
        Returns: (is_impulse, direction)
        """
        if len(df) < min_candles:
            return False, None
        
        recent = df.tail(min_candles)
        price_change = ((recent['close'].iloc[-1] - recent['close'].iloc[0]) / recent['close'].iloc[0]) * 100
        
        if price_change > min_pct:
            return True, 'up'
        elif price_change < -min_pct:
            return True, 'down'
        
        return False, None
