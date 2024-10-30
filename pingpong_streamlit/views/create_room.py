import streamlit as st
import logging
import secrets
from datetime import datetime
from utils.validators import sanitize_input
from data.storage import load_rooms, save_rooms, save_messages

def create_chat_room():
    st.subheader("채팅방 설정")
    with st.form(key='create_room_form'):
        room_name = st.text_input("채팅방 이름")
        user_names = st.text_area("참여자 이름 (쉼표로 구분)", 
                                placeholder="예: Alice, Bob, Charlie")
        submit_button = st.form_submit_button(label="채팅방 생성")
    if st.button("메인으로 돌아가기"):
        st.session_state['page'] = 'main'
        st.rerun()
    
    if submit_button:
        room_name = sanitize_input(room_name, max_length=10)
        if not room_name:
            st.error("올바른 채팅방 이름을 입력하세요 (특수문자 불가, 최대 10자)")
            return

        users = [name.strip() for name in user_names.split(',') if sanitize_input(name, max_length=10)]
        if not users:
            st.error("올바른 사용자 이름을 입력하세요 (특수문자 불가, 최대 10자)")
            return

        try:
            room_id = secrets.token_hex(8)  # 더 안전한 방식의 ID 생성
            new_room = {
                'id': room_id,
                'name': room_name,
                'users': users,
                'created_at': datetime.now().isoformat()
            }
            
            rooms = load_rooms()
            rooms.append(new_room)
            save_rooms(rooms)
            save_messages(room_id, [])
            
            st.session_state['current_room'] = new_room
            st.session_state['page'] = 'select_user'
            logging.info(f"New room created: {room_id}")
            st.rerun()
        except Exception as e:
            logging.error(f"Error creating room: {str(e)}")
            st.error("채팅방 생성 중 오류가 발생했습니다")