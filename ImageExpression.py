import streamlit as st
import streamlit.components.v1 as components

# --- 앱 제목 ---
st.title("이미지 자료의 표현 방법")
st.warning('흑백 이미지와 컬러 이미지 표현간 전환이 자유롭지 않으면 새로고침하세요.', icon="⚠️")

# --- 아이프레임으로 삽입할 Google Apps Script URL ---
# 제공해주신 URL을 여기에 입력합니다.
apps_script_url = "https://script.google.com/macros/s/AKfycbyhYt7Z0bisZUdjPX0-iH4fXCmlvIgv2APAiYg_otxwX4oMSeIlMTPs7DDgOXeM099Odg/exec"

# --- 아이프레임 생성 ---
# st.components.v1.iframe을 사용하여 웹 앱을 아이프레임으로 임베드합니다.
# height 값을 조절하여 아이프레임의 세로 길이를 맞출 수 있습니다.
components.iframe(apps_script_url, height=700, scrolling=True)