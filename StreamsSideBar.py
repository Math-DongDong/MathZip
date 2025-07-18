import streamlit as st
with open("스트림스_게임판.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()

def Draw_sidebar():
    with st.sidebar:
        st.header("스트림스")
        st.page_link("StreamsExplanation.py", label="게임 방법")
        st.download_button(
            label="게임판 다운로드",
            data=PDFbyte,                       # 중요: 파일에서 읽어온 바이트 데이터를 그대로 전달
            file_name="스트림스_게임판.pdf",     # 중요: 사용자가 다운로드할 때 제안될 파일 이름
            mime="application/octet-stream"     # 중요: 모든 종류의 파일에 사용 가능한 범용적인 타입
                                                # 또는 "application/pdf"를 사용해도 됩니다.
        )        
        st.header("버전 설정")
        st.page_link("Streams.py", label="기본 버전")
        st.page_link("StreamsZ.py", label="정수 버전")
        st.page_link("StreamsQ.py", label="유리수 버전")
        st.page_link("StreamsR.py", label="실수 버전")
