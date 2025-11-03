import datetime

class Config:
    SECRET_KEY = 'devkey123'
    DEBUG = True
    TESTING = True
    # Logging configuration values
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    LOG_DATEFMT = '%Y-%m-%dT%H:%M:%SZ'