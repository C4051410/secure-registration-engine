import logging
from logging.handlers import RotatingFileHandler
import sys
from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # --- Part D: Logging Setup ---
    formatter = logging.Formatter(app.config.get('LOG_FORMAT'), datefmt=app.config.get('LOG_DATEFMT'))

    # Rotate logs to file
    handler = RotatingFileHandler('registration.log', maxBytes=1_000_000, backupCount=3)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    # Also log to stdout for development/container visibility
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    app.logger.addHandler(stream_handler)

    # Set base logger level
    app.logger.setLevel(logging.INFO)
    # -----------------------------

    from .routes import main
    app.register_blueprint(main)

    return app