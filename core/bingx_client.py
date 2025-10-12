"""
BingX API Client
Simple HTTP client for BingX API
"""

import hmac
import hashlib
import time
import requests
from typing import List, Dict, Optional
from urllib.parse import urlencode

class BingXClient:
    """Simple BingX API client using HTTP requests"""
    
    def __init__(self, api_key: str, secret_key: str, demo: bool = False, trading_type: str = 'spot'):
        """
        Initialize BingX client using official SDK
        
        Args:
            api_key: BingX API key
            secret_key: BingX secret key
            demo: Use demo/testnet mode
            trading_type: 'spot' or 'futures'
        """
        self.trading_type = trading_type.lower()
        
        # Use official bingX SDK for signature handling
        if demo:
            base_url = 'https://open-api-vst.bingx.com'
        else:
            base_url = 'https://open-api.bingx.com'
        
        self.client = API(
            api_key=api_key,
            api_secret=secret_key,
            base_url=base_url
        )
    
    def _request(self, method: str, endpoint: str, params: Dict = None) -> Dict:
        """Make HTTP request using official bingX SDK"""
        if params is None:
            params = {}
        
        try:
            if method == 'GET':
                result = self.client.get(endpoint, params=params)
            elif method == 'POST':
                result = self.client.post(endpoint, params=params)
            elif method == 'DELETE':
                result = self.client.delete(endpoint, params=params)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            print(f"DEBUG API response: {result}")
            return result
            
        except Exception as e:
            print(f"API request error: {e}")
            return {}
    
    def get_klines(self, symbol: str, interval: str, limit: int = 500) -> List[Dict]:
        """
        Get kline/candlestick data
        
        Args:
            symbol: Trading pair (e.g., 'BTC-USDT')
            interval: Time interval ('1m', '5m', '15m', '1h', etc.)
            limit: Number of candles to fetch
            
        Returns:
            List of kline data
        """
        try:
            # Format symbol correctly for API
            # Spot requires hyphen (BTC-USDT), futures requires no hyphen (BTCUSDT)
            if self.trading_type == 'spot':
                # Ensure hyphen format for spot
                if '-' not in symbol:
                    symbol = symbol[:3] + '-' + symbol[3:]  # Convert BTCUSDT to BTC-USDT
                formatted_symbol = symbol
            else:
                # Remove hyphen for futures
                formatted_symbol = symbol.replace('-', '')
            
            params = {
                'symbol': formatted_symbol,
                'interval': interval,
                'limit': limit
            }
            
            # Use different endpoint based on trading type
            if self.trading_type == 'spot':
                endpoint = '/openApi/spot/v1/market/kline'
            else:
                endpoint = '/openApi/swap/v2/quote/klines'
            
            response = self._request('GET', endpoint, params)
            
            if response and 'data' in response:
                data = response['data']
                if data is not None:
                    return data
            
            return []
            
        except Exception as e:
            print(f"Error fetching klines: {e}")
            return []
    
    def get_balance(self) -> Dict:
        """
        Get account balance
        
        Returns:
            Account balance info
        """
        try:
            # Use different endpoint based on trading type
            if self.trading_type == 'spot':
                endpoint = '/openApi/spot/v1/account/balance'
            else:
                endpoint = '/openApi/swap/v2/user/balance'
            
            response = self._request('GET', endpoint)
            if response and 'data' in response:
                return response['data']
            return {}
        except Exception as e:
            print(f"Error fetching balance: {e}")
            return {}
    
    def create_order(self, symbol: str, side: str, order_type: str, 
                     quantity: float, price: float = None, **kwargs) -> Optional[Dict]:
        """
        Create an order
        
        Args:
            symbol: Trading pair
            side: 'BUY' or 'SELL'  
            order_type: 'MARKET', 'LIMIT', etc.
            quantity: Order quantity
            price: Order price (for limit orders)
            
        Returns:
            Order response
        """
        try:
            # CRITICAL: Spot NEEDS hyphen (BTC-USDT), Futures needs NO hyphen (BTCUSDT)
            if self.trading_type == 'spot':
                # Ensure hyphen for spot
                formatted_symbol = symbol if '-' in symbol else f"{symbol[:3]}-{symbol[3:]}"
            else:
                # Remove hyphen for futures
                formatted_symbol = symbol.replace('-', '')
            
            params = {
                'symbol': formatted_symbol,
                'side': side,
                'type': order_type,
                'quantity': quantity
            }
            
            if price:
                params['price'] = price
            
            params.update(kwargs)
            
            # Use different endpoint based on trading type
            if self.trading_type == 'spot':
                endpoint = '/openApi/spot/v1/trade/order'
            else:
                endpoint = '/openApi/swap/v2/trade/order'
            
            response = self._request('POST', endpoint, params)
            
            if response and 'data' in response:
                return response['data']
            
            return response
            
        except Exception as e:
            print(f"Error creating order: {e}")
            return None
    
    def get_open_orders(self, symbol: str = None) -> List[Dict]:
        """Get open orders"""
        try:
            params = {}
            if symbol:
                params['symbol'] = symbol.replace('-', '')
            
            response = self._request('GET', '/openApi/swap/v2/trade/openOrders', params, signed=True)
            
            if response and 'data' in response:
                orders = response['data']
                if isinstance(orders, dict):
                    return orders.get('orders', [])
                elif isinstance(orders, list):
                    return orders
            
            return []
            
        except Exception as e:
            print(f"Error fetching open orders: {e}")
            return []
    
    def cancel_order(self, symbol: str, order_id: str) -> bool:
        """Cancel an order"""
        try:
            params = {
                'symbol': symbol.replace('-', ''),
                'orderId': order_id
            }
            response = self._request('DELETE', '/openApi/swap/v2/trade/order', params, signed=True)
            return response.get('code') == 0
        except Exception as e:
            print(f"Error canceling order: {e}")
            return False
    
    def get_positions(self, symbol: str = None) -> List[Dict]:
        """Get current positions"""
        try:
            params = {}
            if symbol:
                params['symbol'] = symbol.replace('-', '')
            
            response = self._request('GET', '/openApi/swap/v2/user/positions', params, signed=True)
            
            if response and 'data' in response:
                return response['data']
            
            return []
            
        except Exception as e:
            print(f"Error fetching positions: {e}")
            return []
