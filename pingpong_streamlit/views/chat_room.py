import time
import json
from datetime import datetime
import logging
import streamlit as st
import pytz

from utils.validators import sanitize_input, rate_limiter
from data.storage import load_messages, save_messages

def format_timestamp(timestamp_str):
    """ISO 형식의 타임스탬프를 보기 좋은 형식으로 변환"""
    timestamp = datetime.fromisoformat(timestamp_str)
    kr_tz = pytz.timezone('Asia/Seoul')
    kr_time = timestamp.astimezone(kr_tz)
    return kr_time.strftime("%Y-%m-%d %H:%M")

def chat_room():
    if not st.session_state['current_room'] or not st.session_state['current_user']:
        st.error("잘못된 접근입니다")
        st.session_state['page'] = 'main'
        st.rerun()
        return

    room = st.session_state['current_room']
    user = st.session_state['current_user']
    
    # 현재 유저가 채팅방 유저 목록에 없는 경우 유저 선택 화면으로 이동
    if user not in room['users']:
        st.error("채팅방 참여자가 아닙니다. 다시 선택해주세요.")
        st.session_state['current_user'] = None
        st.session_state['page'] = 'select_user'
        st.rerun()
        return

    # 사이드바 설정
    with st.sidebar:
        st.title(f"채팅방: {room['name']}")
        st.subheader("참여자 목록")
        for participant in room['users']:
            with st.container():
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.write("👤")
                with col2:
                    if participant == user:
                        st.write(f"**{participant} (나)**")
                    else:
                        st.write(participant)
        
        if st.button("메인으로 돌아가기", use_container_width=True):
            st.session_state['page'] = 'main'
            st.rerun()

    # 메인 채팅 영역
    st.header(f"{room['name']}")

    # 채팅 메시지 표시
    messages_container = st.container()
    
    # 메시지 입력
    message = st.chat_input("메시지를 입력하세요")
    
    if message:
        if not rate_limiter.can_proceed(user):
            st.warning("메시지 전송 속도가 너무 빠릅니다")
            return

        cleaned_message = sanitize_input(message)
        if not cleaned_message:
            st.error("올바른 메시지를 입력하세요")
            return

        try:
            messages = load_messages(room['id'])
            new_message = {
                'user': user,
                'message': cleaned_message,
                'timestamp': datetime.now(pytz.UTC).isoformat()
            }
            messages.append(new_message)
            save_messages(room['id'], messages)
            logging.info(f"Message sent in room {room['id']} by {user}")
        except Exception as e:
            logging.error(f"Error sending message: {str(e)}")
            st.error("메시지 전송 중 오류가 발생했습니다")
            return

    # 메시지 표시
    with messages_container:
        try:
            messages = load_messages(room['id'])
            for msg in messages:
                is_user = msg['user'] == user
                with st.chat_message(name=msg['user'], avatar="🧑‍💻" if is_user else "👤"):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(f"**{msg['user']}**")
                    with col2:
                        st.write(f"*{format_timestamp(msg['timestamp'])}*")
                    st.write(msg['message'])
        except Exception as e:
            logging.error(f"Error displaying messages: {str(e)}")
            st.error("채팅 기록을 불러오는 중 오류가 발생했습니다")

    # 자동 새로고침
    time.sleep(1)
    st.rerun()