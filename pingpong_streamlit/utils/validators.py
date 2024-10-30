import re
import logging
from datetime import datetime, timedelta

from config.settings import DATA_DIR



class RateLimiter:
    def __init__(self, seconds=1):
        self.last_request = {}
        self.time_limit = timedelta(seconds=seconds)

    def can_proceed(self, user):
        now = datetime.now()
        if user in self.last_request:
            if now - self.last_request[user] < self.time_limit:
                return False
        self.last_request[user] = now
        return True

rate_limiter = RateLimiter()

def sanitize_input(text, max_length=1000):
    """입력값 검증"""
    if not text or not isinstance(text, str):
        return None
    text = text.strip()
    if len(text) > max_length:
        return None
    if re.search(r'[<>{}[\]\\]', text):
        return None
    return text

def secure_file_path(room_id):
    """파일 경로 검증"""
    if not isinstance(room_id, str) or not room_id.isalnum():
        logging.error(f"Invalid room ID attempted: {room_id}")
        raise ValueError("Invalid room ID")
    return DATA_DIR / f"messages_{room_id}.json"