import logging

# Configure the logger for the 'X_Vector_Pro.logs.alerts' namespace
logger = logging.getLogger(__name__)

# Prevent duplicate log entries by adding a NullHandler if no handlers are configured
if not logger.hasHandlers():
    logger.addHandler(logging.NullHandler())

# Optionally, configure a StreamHandler for console output
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
