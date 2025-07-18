import streamlit as st
import random
from StreamsSideBar import Draw_sidebar  
Draw_sidebar()

st.title("🔢 정수 타일 뽑기")
# --- 구분선 ---
st.divider()

# --- 게임 초기화 함수 ---
def initialize_game():
    """스트림스 게임에 필요한 숫자 풀과 상태 변수들을 초기화합니다."""
    number_pool = []
    
    # --- 여기가 핵심 변경점 1 ---
    # 규칙 1: -15부터 -5까지는 1개씩 추가
    # list(range(-15, -4))를 사용하여 각 숫자를 한 번씩만 리스트에 추가합니다.
    number_pool.extend(list(range(-15, -4)))
        
    # 규칙 2: -4부터 4까지는 2개씩 추가
    for num in range(-4, 5):
        number_pool.extend([num] * 2)
        
    # 규칙 3: 5부터 15까지는 1개씩 추가
    number_pool.extend(list(range(5, 16)))
    
    random.shuffle(number_pool)
    
    st.session_state.pool_Z = number_pool
    st.session_state.draw_count_Z = 0
    st.session_state.current_number_Z = "❔"
    st.session_state.drawn_history_Z = []

# --- 메인 앱 로직 ---
if 'pool_Z' not in st.session_state:
    initialize_game()

# --- 상단 버튼 영역 ---
col1, col_spacer, col2 = st.columns([1,2,1])

with col1:
    if st.button("  처음부터 다시하기  ", type="primary", use_container_width=True):
        initialize_game()
        st.rerun()

with col2:
    is_disabled = (st.session_state.draw_count_Z >= 19)
    if st.button("다음 정수 뽑기", disabled=is_disabled, use_container_width=True):
        if st.session_state.pool_Z:
            st.session_state.draw_count_Z += 1
            new_number = st.session_state.pool_Z.pop()
            st.session_state.current_number_Z = new_number
            st.session_state.drawn_history_Z.append(new_number)

# --- 결과 표시 영역 ---
if st.session_state.draw_count_Z == 0:
    st.header("첫 번째 정수를 뽑아주세요.")
elif st.session_state.draw_count_Z >= 20:
    st.header("🏁 20개의 정수를 모두 뽑았습니다! 🏁")
else:
    st.header(f"{st.session_state.draw_count_Z}번째 정수")

st.markdown(
    f"<p style='text-align: center; font-size: 150px; font-weight: bold;'>{st.session_state.current_number_Z}</p>", 
    unsafe_allow_html=True
)

st.divider()

# --- 규칙 및 기록 표시 영역 ---

# --- 여기가 핵심 변경점 2 ---
# 1. 정보 상자에 들어갈 규칙 텍스트를 정확한 내용으로 수정합니다.
rule_text = "ℹ️ **정수 타일 구성:** -15 ~ -5 (각 1개), -4 ~ 4 (각 2개), 5 ~ 15 (각 1개)"
history_title = "**※ 지금까지 뽑은 정수들:**"

# 2. 뽑은 기록 텍스트를 준비합니다. (이 부분은 수정 없음)
if st.session_state.drawn_history_Z:
    history_values = "  ➡️  ".join(map(str, st.session_state.drawn_history_Z))
else:
    history_values = "아직 뽑은 정수가 없습니다."

# 3. 모든 텍스트를 하나의 문자열로 결합합니다.
info_box_content = f"""{rule_text}
---
{history_title} {history_values}
"""

# 4. 완성된 문자열을 st.info() 위젯에 넣어줍니다.
st.info(info_box_content)