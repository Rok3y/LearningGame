# logging_config.py
import logging
import datetime
import os
import config as cfg

def setup_logger():
    # Create a logger object
    logger = logging.getLogger("StocksLogger")
    logger.setLevel(logging.INFO)  # Set the logging level

    # Formatter
    #LOG_FORMAT = "[%(threadName)s %(module)-30s %(asctime)s %(levelname)s] %(message)s"
    formatter = logging.Formatter(cfg.LOG_STR_FORMAT, datefmt='%H:%M:%S')

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)  # Set the same format for console use

    # File handler
    if not os.path.exists('logs'):
        os.makedirs('logs')
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    file_handler = logging.FileHandler(f'logs/{cfg.DB_NAME}_{date_str}_application.log')
    file_handler.setFormatter(formatter)  # Set the same format for file use

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# Ensure that the logger is configured when module is loaded
logger = setup_logger()