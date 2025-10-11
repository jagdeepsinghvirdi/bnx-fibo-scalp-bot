#!/usr/bin/env python3
"""
Place a small test order to verify the bot CAN execute
"""

from config import Settings
from core import BingXClient

print("="*70)
print("🧪 TEST ORDER PLACEMENT")
print("="*70)
print()
print("⚠️  WARNING: This will place a REAL order on mainnet!")
print()
print(f"Current balance: $6.67 USDT")
print(f"BingX minimum order: ~$10 USDT")
print()
print("Result: Order will likely be REJECTED due to minimum size")
print()

confirm = input("Continue anyway to test? (yes/no): ")

if confirm.lower() != 'yes':
    print("Cancelled.")
    exit(0)

print()
print("Attempting to place smallest possible BTC order...")
print()

client = BingXClient(
    Settings.BINGX_API_KEY,
    Settings.BINGX_SECRET_KEY,
    demo=False,
    trading_type='spot'
)

# Get current price
klines = client.get_klines('BTC-USDT', '1m', 1)
if klines:
    current_price = float(klines[0][4])
    print(f"Current BTC price: ${current_price:,.2f}")
    
    # Try to buy the smallest amount
    usdt_amount = 6.00  # Try $6
    btc_quantity = usdt_amount / current_price
    
    print(f"Attempting to buy: {btc_quantity:.8f} BTC (~${usdt_amount})")
    print()
    
    result = client.create_order(
        symbol='BTC-USDT',
        side='BUY',
        order_type='MARKET',
        quantity=btc_quantity
    )
    
    print("Result:")
    print(result)
    
    if result and 'orderId' in result:
        print()
        print("✅ ORDER PLACED SUCCESSFULLY!")
        print(f"Order ID: {result['orderId']}")
    else:
        print()
        print("❌ ORDER REJECTED")
        print("Reason: Likely below minimum order size")
        print()
        print("To fix:")
        print("1. Add more USDT to your spot wallet (minimum $50-100)")
        print("2. Bot will automatically execute when signals appear")
else:
    print("Could not get current price")
