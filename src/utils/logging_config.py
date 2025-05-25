import logging
import sys
from pathlib import Path

# Get the project root directory (where honeypot.log should be)
PROJECT_ROOT = Path(__file__).parents[2]

def setup_logging():
    """
    Configure logging for the entire application
    """
    log_file = PROJECT_ROOT / 'honeypot.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

def get_logger(name):
    """
    Get a logger instance with the given name
    """
    return logging.getLogger(name) 