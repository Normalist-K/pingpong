import streamlit as st
import logging

def check_password():
    """사용자 인증"""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        pwd = st.text_input("비밀번호를 입력하세요:", type="password")
        if pwd == st.secrets["app"]["password"]:
            st.session_state["password_correct"] = True
            logging.info("Successful login attempt")
        else:
            if pwd:
                logging.warning("Failed login attempt")
            st.error("잘못된 비밀번호입니다.")
            return False
    return True