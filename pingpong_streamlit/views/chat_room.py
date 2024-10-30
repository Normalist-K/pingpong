import time
import json
from datetime import datetime
import logging
import streamlit as st


from utils.validators import sanitize_input, rate_limiter
from data.storage import load_messages, save_messages

def chat_room():
    if not st.session_state['current_room'] or not st.session_state['current_user']:
        st.error("잘못된 접근입니다")
        st.session_state['page'] = 'main'
        st.rerun()
        return

    room = st.session_state['current_room']
    
    st.sidebar.title(f"채팅방: {room['name']}")
    st.sidebar.subheader("사용자 선택")
    user = st.sidebar.radio("사용자", room['users'], 
                           index=room['users'].index(st.session_state['current_user']))
    st.session_state['current_user'] = user

    st.subheader(f"{room['name']} 채팅방")
    message = st.text_input("메시지 입력", key="message_input")
    
    if st.button("전송"):
        if not message:
            st.warning("메시지를 입력하세요")
            return

        if not rate_limiter.can_proceed(user):
            st.warning("메시지 전송 속도가 너무 빠릅니다")
            return

        message = sanitize_input(message)
        if not message:
            st.error("올바른 메시지를 입력하세요")
            return

        try:
            messages = load_messages(room['id'])
            messages.append({
                'user': user,
                'message': message,
                'timestamp': datetime.now().isoformat()
            })
            save_messages(room['id'], messages)
            logging.info(f"Message sent in room {room['id']} by {user}")
            st.rerun()
        except FileNotFoundError:
            st.error("채팅방을 찾을 수 없습니다")
        except PermissionError:
            st.error("파일 접근 권한이 없습니다")
        except json.JSONDecodeError:
            st.error("메시지 데이터가 손상되었습니다")
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            st.error("알 수 없는 오류가 발생했습니다")

    st.subheader("채팅 기록")
    try:
        messages = load_messages(room['id'])
        for msg in messages:
            st.write(f"[{msg['timestamp']}] {msg['user']}: {msg['message']}")
    except Exception as e:
        logging.error(f"Error displaying messages: {str(e)}")
        st.error("채팅 기록을 불러오는 중 오류가 발생했습니다")

    if st.button("메인 화면으로 돌아가기"):
        st.session_state['page'] = 'main'
        st.rerun()

    time.sleep(1)
    st.rerun()