import streamlit as st
import logging
from data.storage import load_rooms, delete_room

def main_page():
    st.title("Pingpong")

    if st.button("채팅방 만들기"):
        st.session_state['page'] = 'create_room'
        st.rerun()

    st.subheader("채팅방 목록")
    rooms = load_rooms()
    for room in rooms:
        col1, col2 = st.columns([4, 1])
        with col1:
            if st.button(f"{room['name']} ({len(room['users'])}명)", key=f"room_{room['id']}"):
                st.session_state['current_room'] = room
                st.session_state['page'] = 'select_user'
                logging.info(f"Room selected: {room['id']}")
                st.rerun()
        with col2:
            if st.button("삭제", key=f"delete_{room['id']}", type="secondary"):
                if st.session_state.get('current_room', {}).get('id') == room['id']:
                    st.session_state['current_room'] = None
                delete_room(room['id'])
                st.success(f"채팅방 '{room['name']}'이(가) 삭제되었습니다")
                st.rerun()