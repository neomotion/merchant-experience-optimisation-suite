import os
import logging


app_env = os.getenv("APP_ENV")


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("testing_run.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)