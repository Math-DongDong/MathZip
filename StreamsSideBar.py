import streamlit as st

def Draw_sidebar():
    with st.sidebar:
        st.header("스트림스")
        st.page_link("StreamsExplanation.py", label="게임 방법")
        st.header("버전 설정")
        st.page_link("Streams.py", label="기본 버전")
        st.page_link("StreamsZ.py", label="정수 버전")
        st.page_link("StreamsQ.py", label="유리수 버전")
        st.page_link("StreamsR.py", label="실수 버전")
