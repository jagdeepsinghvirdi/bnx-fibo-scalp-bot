import logging
import csv
import os
from datetime import datetime
from typing import Dict
from config.settings import Settings

class TradeLogger:
    def __init__(self, log_dir: str = 'logs'):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
        self.setup_logger()
        self.csv_file = os.path.join(log_dir, f'trades_{datetime.now().strftime("%Y%m%d")}.csv')
        self._init_csv()
    
    def setup_logger(self):
        """Setup logging configuration"""
        log_level = getattr(logging, Settings.LOG_LEVEL)
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler()
            ]
        )
        
        if Settings.LOG_TO_FILE:
            file_handler = logging.FileHandler(
                os.path.join(self.log_dir, f'bot_{datetime.now().strftime("%Y%m%d")}.log')
            )
            file_handler.setFormatter(
                logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            )
            logging.getLogger().addHandler(file_handler)
        
        self.logger = logging.getLogger('FiboScalpBot')
    
    def _init_csv(self):
        """Initialize CSV file with headers"""
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp', 'symbol', 'direction', 'action', 
                    'entry_price', 'exit_price', 'quantity', 
                    'stop_loss', 'pnl', 'reason'
                ])
    
    def log_trade(self, trade_data: Dict):
        """Log trade to CSV"""
        with open(self.csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                trade_data.get('timestamp', datetime.now()),
                trade_data.get('symbol', ''),
                trade_data.get('direction', ''),
                trade_data.get('action', ''),
                trade_data.get('entry_price', 0),
                trade_data.get('exit_price', 0),
                trade_data.get('quantity', 0),
                trade_data.get('stop_loss', 0),
                trade_data.get('pnl', 0),
                trade_data.get('reason', '')
            ])
    
    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)
