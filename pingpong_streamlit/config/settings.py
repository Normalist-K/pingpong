import streamlit as st
from pathlib import Path

# 로깅 설정
LOG_CONFIG = {
    'filename': st.secrets["app"]["log_file"],
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s'
}

# 데이터 저장 경로 설정
DATA_DIR = Path(st.secrets["app"]["data_dir"])
ROOMS_FILE = DATA_DIR / "rooms.json"