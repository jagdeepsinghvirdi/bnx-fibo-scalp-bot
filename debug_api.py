#!/usr/bin/env python3
"""
Debug script to test BingX API connection with detailed error messages
"""

import requests
import hmac
import hashlib
import time
from urllib.parse import urlencode
from config import Settings

def test_api_connection():
    """Test BingX API connection with detailed logging"""
    
    print("=" * 60)
    print("BingX API Connection Debug")
    print("=" * 60)
    print()
    
    # Display configuration
    print("Configuration:")
    print(f"  Mode: {Settings.TRADING_MODE}")
    print(f"  Base URL: {Settings.BINGX_API_URL}")
    print(f"  API Key: {Settings.BINGX_API_KEY[:20]}...")
    print()
    
    # Test 1: Check if credentials exist
    print("-" * 60)
    print("Test 1: Credentials Check")
    print("-" * 60)
    
    if not Settings.BINGX_API_KEY:
        print("❌ API Key is EMPTY")
        return False
    
    if not Settings.BINGX_SECRET_KEY:
        print("❌ Secret Key is EMPTY")
        return False
    
    print("✓ API Key loaded")
    print("✓ Secret Key loaded")
    print()
    
    # Test 2: Test public endpoint (no auth needed)
    print("-" * 60)
    print("Test 2: Public Endpoint (no auth required)")
    print("-" * 60)
    
    try:
        url = f"{Settings.BINGX_API_URL}/openApi/spot/v1/market/kline"
        params = {
            'symbol': 'BTC-USDT',
            'interval': '1m',
            'limit': 1
        }
        
        print(f"URL: {url}")
        print(f"Params: {params}")
        
        response = requests.get(url, params=params, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✓ Public endpoint works!")
            print(f"Response: {str(data)[:200]}...")
        else:
            print(f"❌ Status code {response.status_code}")
            print(f"Response: {response.text}")
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
    
    # Test 3: Test authenticated endpoint
    print("-" * 60)
    print("Test 3: Authenticated Endpoint (requires valid keys)")
    print("-" * 60)
    
    try:
        endpoint = '/openApi/spot/v1/account/balance'
        timestamp = int(time.time() * 1000)
        
        params = {
            'timestamp': timestamp
        }
        
        # Generate signature
        query_string = urlencode(sorted(params.items()))
        signature = hmac.new(
            Settings.BINGX_SECRET_KEY.encode(),
            query_string.encode(),
            hashlib.sha256
        ).hexdigest()
        
        params['signature'] = signature
        
        headers = {
            'X-BX-APIKEY': Settings.BINGX_API_KEY,
            'Content-Type': 'application/json'
        }
        
        url = f"{Settings.BINGX_API_URL}{endpoint}"
        
        print(f"URL: {url}")
        print(f"Params: {params}")
        print(f"Headers: {{'X-BX-APIKEY': '{Settings.BINGX_API_KEY[:20]}...'}}")
        print()
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print()
        
        data = response.json()
        print(f"Response Body:")
        print(data)
        print()
        
        if response.status_code == 200 and 'data' in data:
            print("✅ Authentication SUCCESSFUL!")
            if 'balances' in data['data']:
                balances = data['data']['balances']
                print(f"\nYou have {len(balances)} assets:")
                for bal in balances:
                    if float(bal.get('free', 0)) > 0 or float(bal.get('locked', 0)) > 0:
                        asset = bal.get('asset')
                        free = float(bal.get('free', 0))
                        locked = float(bal.get('locked', 0))
                        print(f"  {asset}: {free} (free) + {locked} (locked)")
        else:
            print(f"❌ Authentication FAILED")
            if 'code' in data:
                print(f"Error Code: {data.get('code')}")
            if 'msg' in data:
                print(f"Error Message: {data.get('msg')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 60)

if __name__ == '__main__':
    test_api_connection()
