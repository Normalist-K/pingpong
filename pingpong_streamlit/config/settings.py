import logging
import streamlit as st
from pathlib import Path
import os
import tempfile

# 로깅 설정
LOG_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'handlers': [logging.StreamHandler()]
}

# 데이터 저장 경로 설정
if os.getenv('STREAMLIT_CLOUD'):
    DATA_DIR = Path(tempfile.gettempdir()) / "secure_chat_data"
else:
    DATA_DIR = Path(st.secrets["app"]["data_dir"])
ROOMS_FILE = DATA_DIR / "rooms.json"