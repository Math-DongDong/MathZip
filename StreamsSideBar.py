import streamlit as st

def Draw_sidebar():
    with st.sidebar:
        st.header("스트림스 설명")
        st.page_link("StreamsExplanation.py", label="설명 영상 보기")
        st.header("스트림스 버전 설정")
        st.page_link("Streams.py", label="기본 버전")
        st.page_link("StreamsZ.py", label="정수 버전")
        st.page_link("StreamsQ.py", label="유리수 버전")
        st.page_link("StreamsR.py", label="실수 버전")
