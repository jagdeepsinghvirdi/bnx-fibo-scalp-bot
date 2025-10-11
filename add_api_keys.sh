#!/bin/bash

echo "=========================================="
echo "  BingX Fibo Scalp Bot - API Key Setup"
echo "=========================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env from template..."
    cp .env.template .env
fi

echo "Please enter your BingX API credentials:"
echo ""

# Get API Key
read -p "BingX API Key: " api_key
if [ -z "$api_key" ]; then
    echo "Error: API Key cannot be empty"
    exit 1
fi

# Get Secret Key
read -p "BingX Secret Key: " secret_key
if [ -z "$secret_key" ]; then
    echo "Error: Secret Key cannot be empty"
    exit 1
fi

# Trading Mode
echo ""
echo "Select Trading Mode:"
echo "1) Testnet (Safe for testing - recommended)"
echo "2) Mainnet (Live trading with real money)"
read -p "Enter choice (1 or 2): " mode_choice

if [ "$mode_choice" == "1" ]; then
    trading_mode="testnet"
    echo "✓ Using Testnet mode"
elif [ "$mode_choice" == "2" ]; then
    trading_mode="mainnet"
    echo "⚠️  WARNING: Using Mainnet mode - REAL MONEY!"
    read -p "Are you sure? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        echo "Cancelled."
        exit 1
    fi
else
    echo "Invalid choice. Using testnet by default."
    trading_mode="testnet"
fi

# Optional: Telegram
echo ""
read -p "Add Telegram notifications? (y/n): " add_telegram

telegram_token=""
telegram_chat=""

if [ "$add_telegram" == "y" ] || [ "$add_telegram" == "Y" ]; then
    read -p "Telegram Bot Token: " telegram_token
    read -p "Telegram Chat ID: " telegram_chat
fi

# Update .env file
echo ""
echo "Updating .env file..."

# Backup existing .env
cp .env .env.backup

# Update API credentials
sed -i "s/^BINGX_API_KEY=.*/BINGX_API_KEY=$api_key/" .env
sed -i "s/^BINGX_SECRET_KEY=.*/BINGX_SECRET_KEY=$secret_key/" .env
sed -i "s/^TRADING_MODE=.*/TRADING_MODE=$trading_mode/" .env

if [ ! -z "$telegram_token" ]; then
    sed -i "s/^TELEGRAM_BOT_TOKEN=.*/TELEGRAM_BOT_TOKEN=$telegram_token/" .env
    sed -i "s/^TELEGRAM_CHAT_ID=.*/TELEGRAM_CHAT_ID=$telegram_chat/" .env
fi

echo "✓ Configuration saved!"
echo ""

# Test API connection
echo "=========================================="
echo "Testing API Connection..."
echo "=========================================="
echo ""

if [ -d "venv" ]; then
    source venv/bin/activate
    
    python3 << EOF
from config import Settings
from core import BingXClient
import sys

try:
    print(f"Trading Mode: {Settings.TRADING_MODE}")
    print(f"API URL: {Settings.BINGX_API_URL}")
    print("")
    
    client = BingXClient(
        Settings.BINGX_API_KEY,
        Settings.BINGX_SECRET_KEY,
        demo=(Settings.TRADING_MODE == 'testnet')
    )
    
    print("Testing connection...")
    balance = client.get_balance()
    
    if balance:
        print("")
        print("✓ API Connection Successful!")
        print("")
        print("Account Balance:")
        print(balance)
    else:
        print("")
        print("⚠️  API connection returned empty response")
        print("This might be normal for new testnet accounts")
        
except Exception as e:
    print(f"")
    print(f"❌ Error: {e}")
    print("")
    print("Please check:")
    print("- API keys are correct")
    print("- API has trading permissions enabled")
    print("- Using correct mode (testnet/mainnet)")
    sys.exit(1)
EOF

    if [ $? -eq 0 ]; then
        echo ""
        echo "=========================================="
        echo "✓ Setup Complete!"
        echo "=========================================="
        echo ""
        echo "Next steps:"
        echo "1. Review your .env configuration"
        echo "2. Test with backtest: python -m core.backtester"
        echo "3. Run live bot: python bot.py"
        echo ""
        echo "For more info, see API_SETUP.md"
    fi
else
    echo "⚠️  Virtual environment not found"
    echo "Run ./setup.sh first to install dependencies"
fi

echo ""
