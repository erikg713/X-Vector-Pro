import os

# General settings
PROJECT_NAME = "X-Vector Pro"
VERSION = "1.0.0"
AUTHOR = "Your Name"

# File paths (modify based on your project structure)
LOGS_DIR = os.path.join(os.getcwd(), 'logs')
DATA_DIR = os.path.join(os.getcwd(), 'data')
REPORTS_DIR = os.path.join(os.getcwd(), 'reports')

# Logging settings
LOG_FILE = os.path.join(LOGS_DIR, 'xvector_log.txt')
LOG_LEVEL = "INFO"  # Possible values: DEBUG, INFO, WARNING, ERROR, CRITICAL

# Network settings
API_URL = "https://api.xvector.com"
TIMEOUT = 30  # Timeout in seconds for network requests

# Authentication settings (Example)
API_KEY = "your-api-key-here"  # Can be set to None or environment variable
DEBUG_MODE = False  # If set to True, the application will run in debug mode

# Database settings
DB_URI = os.getenv("DB_URI", "mongodb://localhost:27017/xvector_db")  # MongoDB URI
DB_NAME = "xvector_db"

# Security settings
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "default_encryption_key")
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

# Email settings (if you're sending email notifications or reports)
EMAIL_HOST = "smtp.yourmail.com"
EMAIL_PORT = 587
EMAIL_USER = "youremail@yourmail.com"
EMAIL_PASSWORD = "yourpassword"

# Other settings (example for AI/ML model)
MODEL_PATH = os.path.join(DATA_DIR, 'models', 'xvector_model_final.pth')
CHECKPOINT_PATH = os.path.join(DATA_DIR, 'checkpoints')

# Customize any additional settings you may need
