#!/bin/bash

echo "==================================="
echo "Fibo Scalp Bot Setup Script"
echo "==================================="

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.template .env
    echo "Please edit .env file with your API keys and settings"
else
    echo ".env file already exists"
fi

# Create logs directory
mkdir -p logs

echo ""
echo "==================================="
echo "Setup Complete!"
echo "==================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your BingX API keys"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Run backtest: python -m core.backtester"
echo "4. Run live bot: python bot.py"
echo ""
echo "For Docker deployment:"
echo "  cd docker && docker-compose up -d"
echo ""
