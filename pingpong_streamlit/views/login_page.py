import streamlit as st
import logging

def login_page():
    st.title("Pingpong Chat 로그인")
    
    # 중앙 정렬을 위한 컬럼 사용
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 환영합니다! 👋")
        st.markdown("채팅을 시작하려면 비밀번호를 입력하세요.")
        
        pwd = st.text_input("비밀번호", type="password")
        
        if st.button("로그인", use_container_width=True):
            if pwd == st.secrets["app"]["password"]:
                st.session_state["password_correct"] = True
                logging.info("Successful login attempt")
                st.rerun()
            else:
                if pwd:
                    logging.warning("Failed login attempt")
                st.error("잘못된 비밀번호입니다.")