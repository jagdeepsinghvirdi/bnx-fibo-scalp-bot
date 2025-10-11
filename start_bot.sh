#!/bin/bash

echo "=========================================="
echo "  Starting Fibo Scalp Bot"
echo "=========================================="
echo ""

cd /home/ec2-user/bnx_bot_fiboscalp

# Check balance first
echo "Checking balance..."
source venv/bin/activate
python check_balance.py

echo ""
echo "=========================================="
echo "Starting bot..."
echo "=========================================="
echo ""
echo "Press Ctrl+C to stop the bot"
echo ""

# Start the bot
python bot.py
