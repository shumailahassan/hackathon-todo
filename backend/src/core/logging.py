import logging
from datetime import datetime
from typing import Optional
import json


class Logger:
    def __init__(self, name: str = "auth_system"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # Create handler if not already set up
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def info(self, message: str, user_id: Optional[str] = None, extra: Optional[dict] = None):
        log_data = {
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "extra": extra or {}
        }
        self.logger.info(json.dumps(log_data))

    def error(self, message: str, user_id: Optional[str] = None, exception: Optional[Exception] = None, extra: Optional[dict] = None):
        log_data = {
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "exception": str(exception) if exception else None,
            "extra": extra or {}
        }
        self.logger.error(json.dumps(log_data))

    def warning(self, message: str, user_id: Optional[str] = None, extra: Optional[dict] = None):
        log_data = {
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "extra": extra or {}
        }
        self.logger.warning(json.dumps(log_data))

    def debug(self, message: str, user_id: Optional[str] = None, extra: Optional[dict] = None):
        log_data = {
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "extra": extra or {}
        }
        self.logger.debug(json.dumps(log_data))


# Global logger instance
auth_logger = Logger()