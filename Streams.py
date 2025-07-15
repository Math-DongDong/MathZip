# Streams.py

import streamlit as st
import random

st.markdown("<h1 style='text-align: center; margin-bottom: 10px;'>🔢 스트림스 카드 뽑기</h1>", unsafe_allow_html=True)
# --- 구분선 ---
st.divider()

# --- 게임 초기화 함수 ---
def initialize_game():
    """스트림스 게임에 필요한 숫자 풀과 상태 변수들을 초기화합니다."""
    number_pool = []
    number_pool.extend(list(range(1, 11)))
    number_pool.extend(list(range(11, 21)))
    number_pool.extend(list(range(11, 21)))
    number_pool.extend(list(range(21, 31)))
    random.shuffle(number_pool)
    
    st.session_state.pool = number_pool
    st.session_state.draw_count = 0
    st.session_state.current_number = "❔"
    st.session_state.drawn_history = []

# --- 메인 앱 로직 ---
if 'pool' not in st.session_state:
    initialize_game()

# --- 상단 버튼 영역 ---
# *** 여기가 핵심 변경점 1: 화면을 3등분하여 버튼 배치 ***
# 화면을 3개의 동일한 너비의 컬럼으로 나눕니다.
# col_spacer는 버튼 사이의 공간을 만드는 역할을 합니다.
col1, col_spacer, col2 = st.columns(3)

# 왼쪽 첫 번째 컬럼: 초기화 버튼
with col1:
    if st.button("처음부터 다시하기", type="primary"):
        initialize_game()
        st.rerun()

# 오른쪽 세 번째 컬럼: 뽑기 버튼
with col2:
    is_disabled = (st.session_state.draw_count >= 20)
    if st.button("다음 숫자 뽑기", disabled=is_disabled):
        if st.session_state.pool:
            st.session_state.draw_count += 1
            new_number = st.session_state.pool.pop()
            st.session_state.current_number = new_number
            st.session_state.drawn_history.append(new_number)

# --- 결과 표시 영역 ---
if st.session_state.draw_count == 0:
    st.header("첫 번째 숫자를 뽑아주세요.")
elif st.session_state.draw_count >= 20:
    st.header("🏁 숫자를 모두 뽑았습니다! 🏁")
else:
    st.header(f"{st.session_state.draw_count}번째 숫자")

st.markdown(
    f"<p style='text-align: center; font-size: 150px; font-weight: bold;'>{st.session_state.current_number}</p>", 
    unsafe_allow_html=True
)

st.divider()

# *** 여기가 핵심 변경점 2: 게임 규칙 정보 제공 ***
# st.info를 사용하여 규칙을 눈에 띄게 표시합니다.
st.info("ℹ️ **숫자 타일 규칙:** 1 ~ 10 (각 1개), 11 ~ 20 (각 2개), 21 ~ 30 (각 1개)")

st.write("지금까지 뽑은 숫자들:")
formatted_history = "  ➡️  ".join(map(str, st.session_state.drawn_history))
st.info(formatted_history or "아직 뽑은 숫자가 없습니다.")