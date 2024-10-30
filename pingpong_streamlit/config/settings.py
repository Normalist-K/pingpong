import logging

# 로깅 설정
LOG_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'handlers': [logging.StreamHandler()]
}