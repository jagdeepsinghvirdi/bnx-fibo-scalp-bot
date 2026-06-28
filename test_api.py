#!/usr/bin/env python3
"""
Test BingX API Connection
Quick script to verify your API keys are working
"""

import sys
import json
from config import Settings
from core import BingXClient

def format_balance(balance):
    """Format balance data for better readability"""
    if isinstance(balance, dict):
        if 'balances' in balance and isinstance(balance['balances'], list):
            # Format list of balances
            for item in balance['balances']:
                print(f"  Asset: {item.get('disPlayName', item.get('asset', 'N/A'))}")
                print(f"    Free: {item.get('free', 'N/A')}")
                print(f"    Locked: {item.get('locked', 'N/A')}")
                print()
        else:
            # Format other dict structures
            for key, value in balance.items():
                if isinstance(value, (dict, list)):
                    print(f"  {key}:")
                    print(f"    {json.dumps(value, indent=6)}")
                else:
                    print(f"  {key}: {value}")
    else:
        print(f"  {balance}")

def test_connection():
    """Test API connection and display account info"""
    
    print("="*50)
    print("BingX API Connection Test")
    print("="*50)
    print()
    
    # Display configuration
    print("Configuration:")
    print(f"  Trading Mode: {Settings.TRADING_MODE}")
    print(f"  Symbol: {Settings.SYMBOL}")
    print(f"  API URL: {Settings.BINGX_API_URL}")
    print()
    
    # Check if API keys are set
    if not Settings.BINGX_API_KEY or Settings.BINGX_API_KEY == "your_api_key_here":
        print("❌ Error: API Key not configured")
        print("   Please run: ./add_api_keys.sh")
        return False
    
    if not Settings.BINGX_SECRET_KEY or Settings.BINGX_SECRET_KEY == "your_secret_key_here":
        print("❌ Error: Secret Key not configured")
        print("   Please run: ./add_api_keys.sh")
        return False
    
    print(f"API Key: {Settings.BINGX_API_KEY[:10]}...{Settings.BINGX_API_KEY[-10:]}")
    print()
    
    # Initialize client
    print("Initializing BingX client...")
    try:
        client = BingXClient(
            Settings.BINGX_API_KEY,
            Settings.BINGX_SECRET_KEY,
            demo=(Settings.TRADING_MODE == 'testnet')
        )
        print("✓ Client initialized")
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return False
    
    print()
    print("-"*50)
    print("Test 1: Get Account Balance")
    print("-"*50)
    
    try:
        balance = client.get_balance()
        if balance:
            print("✓ Balance retrieved successfully!")
            print()
            print("Account Balance:")
            format_balance(balance)
        else:
            print("⚠️  Empty response (might be normal for new testnet account)")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print()
    print("-"*50)
    print("Test 2: Get Market Data")
    print("-"*50)
    
    try:
        print(f"Fetching klines for {Settings.SYMBOL}...")
        klines = client.get_klines(Settings.SYMBOL, '1m', limit=5)
        
        if klines:
            print(f"✓ Retrieved {len(klines)} candles")
            print()
            print("Latest candle:")
            if isinstance(klines[-1], dict):
                print(f"  Time: {klines[-1].get('time', 'N/A')}")
                print(f"  Open: {klines[-1].get('open', 'N/A')}")
                print(f"  High: {klines[-1].get('high', 'N/A')}")
                print(f"  Low: {klines[-1].get('low', 'N/A')}")
                print(f"  Close: {klines[-1].get('close', 'N/A')}")
            else:
                print(f"  {klines[-1]}")
        else:
            print("⚠️  No kline data received")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print()
    print("="*50)
    print("✓ All Tests Passed!")
    print("="*50)
    print()
    print("Your API connection is working correctly.")
    print()
    print("Next steps:")
    print("  1. Review configuration in .env")
    print("  2. Run backtest: python -m core.backtester")
    print("  3. Start bot: python bot.py")
    print()
    
    return True

if __name__ == '__main__':
    try:
        success = test_connection()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
