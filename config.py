import datetime


class Config:
SECRET_KEY = 'devkey123'
DEBUG = True
TESTING = True
# CSRF is enabled via Flask-WTF using SECRET_KEY
# Logging configuration values (optional) - can be extended
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_DATEFMT = '%Y-%m-%dT%H:%M:%SZ