import logging

LOG_LEVEL = 'INFO'

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] [%(funcName)s()] - %(message)s", 
)

logger = logging.getLogger()