# Added example handler to log to console 
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Modified to use logger object  
def log_data(data):
    try:
        logger.info(data) 
    except Exception as e:
        logger.error(f"Error logging data: {str(e)}")