#!/usr/bin/env python3
"""
Quick balance checker for mainnet spot account
"""

from config import Settings
from core import BingXClient

def check_balance():
    print("="*50)
    print("BingX Spot Balance Check")
    print("="*50)
    print()
    
    print(f"Mode: {Settings.TRADING_MODE}")
    print(f"Type: {Settings.TRADING_TYPE}")
    print()
    
    client = BingXClient(
        Settings.BINGX_API_KEY,
        Settings.BINGX_SECRET_KEY,
        demo=(Settings.TRADING_MODE == 'testnet'),
        trading_type=Settings.TRADING_TYPE
    )
    
    print("Fetching account balance...")
    balance = client.get_balance()
    
    if balance and 'balances' in balance:
        balances = balance['balances']
        
        if not balances:
            print()
            print("⚠️  No funds in spot wallet")
            print()
            print("To trade, you need to:")
            print("1. Deposit USDT to your BingX account")
            print("2. Transfer funds to Spot wallet")
            print("3. Verify balance shows here")
            print()
        else:
            print()
            print("Spot Wallet Balances:")
            print("-" * 50)
            
            for bal in balances:
                asset = bal.get('asset', 'Unknown')
                free = float(bal.get('free', 0))
                locked = float(bal.get('locked', 0))
                total = free + locked
                
                if total > 0:
                    print(f"{asset:8} - Free: {free:15.8f}  Locked: {locked:15.8f}  Total: {total:15.8f}")
            
            print()
            
            # Check USDT balance specifically
            usdt_balance = next((b for b in balances if b.get('asset') == 'USDT'), None)
            if usdt_balance:
                usdt_free = float(usdt_balance.get('free', 0))
                if usdt_free > 0:
                    print(f"✅ Ready to trade! USDT available: ${usdt_free:,.2f}")
                else:
                    print("⚠️  No USDT available for trading")
            else:
                print("⚠️  No USDT in account")
                
    else:
        print("⚠️  Could not fetch balance")
        print(f"Response: {balance}")
    
    print()
    print("="*50)

if __name__ == '__main__':
    check_balance()
