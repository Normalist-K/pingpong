import streamlit as st
import logging
from config.settings import LOG_CONFIG
from views.login_page import login_page
from views.main_page import main_page
from views.chat_room import chat_room
from views.create_room import create_chat_room
from views.select_user import select_user_page

# 로깅 설정
logging.basicConfig(**LOG_CONFIG)

# 세션 상태 초기화
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False
if 'current_room' not in st.session_state:
    st.session_state['current_room'] = None
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None
if 'page' not in st.session_state:
    st.session_state['page'] = 'main'

def run_app():
    if not st.session_state["password_correct"]:
        login_page()
        return

    if st.session_state['page'] == 'main':
        main_page()
    elif st.session_state['page'] == 'create_room':
        create_chat_room()
    elif st.session_state['page'] == 'select_user':
        select_user_page()
    elif st.session_state['page'] == 'chat_room':
        chat_room()

if __name__ == "__main__":
    try:
        run_app()
    except Exception as e:
        logging.error(f"Application error: {str(e)}")
        st.error("애플리케이션 오류가 발생했습니다")