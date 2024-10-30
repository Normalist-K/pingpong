import streamlit as st
import logging

def select_user_page():
    st.title("사용자 선택")
    
    if not st.session_state['current_room']:
        st.error("잘못된 접근입니다")
        st.session_state['page'] = 'main'
        st.rerun()
        return
        
    room = st.session_state['current_room']
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"### {room['name']} 채팅방")
        st.markdown("참여할 사용자를 선택해주세요.")
        
        user = st.radio("사용자 선택", room['users'])
        
        if st.button("채팅 시작", use_container_width=True):
            st.session_state['current_user'] = user
            st.session_state['page'] = 'chat_room'
            logging.info(f"User {user} selected for room: {room['id']}")
            st.rerun()
            
        if st.button("메인으로 돌아가기"):
            st.session_state['page'] = 'main'
            st.rerun()