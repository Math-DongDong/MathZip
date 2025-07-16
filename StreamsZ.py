import streamlit as st
import random
from StreamsSideBar import Draw_sidebar  # 사이드바 임포트 부분은 그대로 둡니다.
Draw_sidebar()

st.title("🔢 스트림스 카드 뽑기")
# --- 구분선 ---
st.divider()

# --- 게임 초기화 함수 ---
def initialize_game():
    """스트림스 게임에 필요한 숫자 풀과 상태 변수들을 초기화합니다."""
    number_pool = []
    
    # --- 여기가 핵심 변경점 1 ---
    # 새로운 규칙에 따라 숫자 풀을 생성합니다.
    
    # 규칙 1: -15부터 -5까지는 10개씩 추가
    # range(-15, -4)는 -15, -14, ..., -5까지의 숫자를 생성합니다.
    for num in range(-15, -4):
        number_pool.extend([num] * 10)
        
    # 규칙 2: -4부터 4까지는 2개씩 추가
    # range(-4, 5)는 -4, -3, ..., 4까지의 숫자를 생성합니다.
    for num in range(-4, 5):
        number_pool.extend([num] * 2)
        
    # 규칙 3: 5부터 15까지는 1개씩 추가
    # range(5, 16)은 5, 6, ..., 15까지의 숫자를 생성합니다.
    number_pool.extend(list(range(5, 16)))
    
    # 생성된 숫자 풀을 무작위로 섞습니다.
    random.shuffle(number_pool)
    
    # 게임 상태를 초기화합니다.
    st.session_state.pool = number_pool
    st.session_state.draw_count = 0
    st.session_state.current_number = "❔"
    st.session_state.drawn_history = []

# --- 메인 앱 로직 ---
if 'pool' not in st.session_state:
    initialize_game()

# --- 상단 버튼 영역 ---
col1, col_spacer, col2 = st.columns([1,2,1])

with col1:
    if st.button("  처음부터 다시하기  ", type="primary", use_container_width=True):
        initialize_game()
        st.rerun()

with col2:
    # --- 여기가 핵심 변경점 2 ---
    # 전체 타일 개수를 계산하여 최대 뽑기 횟수를 업데이트합니다.
    # 계산: (-15~-5: 11개*10) + (-4~4: 9개*2) + (5~15: 11개*1) = 110 + 18 + 11 = 139개
    total_tiles = 139
    is_disabled = (st.session_state.draw_count >= total_tiles)
    
    if st.button("다음 수 뽑기", disabled=is_disabled, use_container_width=True):
        if st.session_state.pool:
            st.session_state.draw_count += 1
            new_number = st.session_state.pool.pop()
            st.session_state.current_number = new_number
            st.session_state.drawn_history.append(new_number)

# --- 결과 표시 영역 ---
if st.session_state.draw_count == 0:
    st.header("첫 번째 수를 뽑아주세요.")
# is_disabled 변수를 여기서도 활용할 수 있습니다.
elif is_disabled:
    st.header("🏁 수를 모두 뽑았습니다! 🏁")
else:
    st.header(f"{st.session_state.draw_count}번째 수")

st.markdown(
    f"<p style='text-align: center; font-size: 150px; font-weight: bold;'>{st.session_state.current_number}</p>", 
    unsafe_allow_html=True
)

st.divider()

# --- 규칙 및 기록 표시 영역 ---

# --- 여기가 핵심 변경점 3 ---
# 1. 정보 상자에 들어갈 규칙 텍스트를 새로운 내용으로 변경합니다.
rule_text = "ℹ️ **수 타일 구성:** -15 ~ -5 (각 10개), -4 ~ 4 (각 2개), 5 ~ 15 (각 1개)"
history_title = "**※ 지금까지 뽑은 수들:**"

# 2. 뽑은 기록이 있을 때와 없을 때를 구분하여 텍스트를 준비합니다.
if st.session_state.drawn_history:
    # map(str, ...)을 사용하여 리스트의 모든 숫자들을 문자열로 변환합니다.
    history_values = "  ➡️  ".join(map(str, st.session_state.drawn_history))
else:
    history_values = "아직 뽑은 수가 없습니다."

# 3. 모든 텍스트를 하나의 문자열로 결합합니다.
info_box_content = f"""{rule_text}
---
{history_title} {history_values}
"""

# 4. 완성된 문자열을 st.info() 위젯에 넣어줍니다.
st.info(info_box_content)