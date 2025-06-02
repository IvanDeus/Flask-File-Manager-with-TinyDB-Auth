import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Flask server settings
HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 5000       # Default port
DEBUG = False      # Debug mode (set to False in production)

# Secret key (CHANGE THIS IN PRODUCTION!)
SECRET_KEY = 'your-secret-key-here'

# File upload settings
UPLOAD_FOLDER = BASE_DIR / 'static' / 'uploaded_files'
MAX_CONTENT_LENGTH = 1600 * 1024 * 1024  # 1600MB
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'ogg', 'wav', 'mp3', 'doc', 'docx', 'xls', 'xlsx'}

# Database settings
DB_FILE = BASE_DIR / 'users_db.json'

# Session settings
SESSION_COOKIE_NAME = 'file_manager_session'
PERMANENT_SESSION_LIFETIME = 3600  # 1 hour in seconds

# Logging settings
LOG_FILE = BASE_DIR / 'app.log'
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
