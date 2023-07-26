import logging
import os
from datetime import datetime

# datetime.now() will return a datetime object with current date and time and .strftime() will
# convert the datetime object into a string with required format.

# log file name
LOG_FILE_NAME = f"{datetime.now().strftime('%d_%m_%Y__%H_%M_%S')}.log"

# log directory
LOG_FILE_DIR = os.path.join(os.getcwd(), "logs")

# create folder if not available 
os.makedirs(LOG_FILE_DIR, exist_ok=True)

# log file path
LOG_FILE_PATH = os.path.join(LOG_FILE_DIR, LOG_FILE_NAME)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(filename)s:[%(lineno)d] - %(levelname)s - %(message)s",
    level=logging.INFO,
    force = True
)