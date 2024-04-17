# --------------------  Imports  --------------------

import os
import sys
import logging
from .globals import BACKEND_ROOT_PATH

# --------------------  Config  --------------------
"""
Methods available: debug, info, warning, error, critical
ex: logging.debug('This is a debug message')
"""
log_file_name = "backend_log.log"
log_file_path = os.path.join(BACKEND_ROOT_PATH, log_file_name)
logging.basicConfig(
    filename=log_file_path,
    filemode="a",
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.DEBUG,
)

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(sys.stdout))

# --------------------  END  --------------------