import streamlit as st
import streamlit.components.v1 as components

# --- 페이지 설정 ---
# 페이지 레이아웃을 'wide'로 설정하여 아이프레임이 넓게 표시되도록 합니다.
st.set_page_config(
    page_title="이미지 표현 도구",
    layout="wide"
)

# --- 앱 제목 ---
st.title("이미지 표현(인공지능수학) 도구")
st.markdown("Google Apps Script로 제작된 웹 앱을 Streamlit 페이지에 연동한 예제입니다.")
st.markdown("---") # 구분선

# --- 아이프레임으로 삽입할 Google Apps Script URL ---
# 제공해주신 URL을 여기에 입력합니다.
apps_script_url = "https://script.google.com/macros/s/AKfycbzOjKP_IHrzKcP2Mu-eFaOtZowc2D5ephpld6zvIvsWAl9QqmHBO__zSRv5SPQIWbEU/exec"

# --- 아이프레임 생성 ---
# st.components.v1.iframe을 사용하여 웹 앱을 아이프레임으로 임베드합니다.
# height 값을 조절하여 아이프레임의 세로 길이를 맞출 수 있습니다.
components.iframe(apps_script_url, height=850, scrolling=True)

# --- 추가 설명 ---
st.info("위 콘텐츠는 Google Apps Script로 제작되었으며, 아이프레임(iframe)을 통해 현재 페이지에 표시되고 있습니다.")