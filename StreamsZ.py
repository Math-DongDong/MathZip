import streamlit as st
import random
# --- 여기가 핵심 변경점 1 ---
# 사이드바를 활성화하기 위해 주석을 해제합니다.
from StreamsSideBar import Draw_sidebar  
Draw_sidebar()

st.title("🔢 스트림스 카드 뽑기")
# --- 구분선 ---
st.divider()

# --- 게임 초기화 함수 ---
def initialize_game():
    """스트림스 게임에 필요한 숫자 풀과 상태 변수들을 초기화합니다."""
    # 숫자 풀을 만드는 로직은 그대로 유지합니다.
    # 게임은 139개의 타일 중에서 20개만 뽑는 방식으로 진행됩니다.
    number_pool = []
    
    # 규칙 1: -15부터 -5까지는 10개씩 추가
    for num in range(-15, -4):
        number_pool.extend([num] * 10)
        
    # 규칙 2: -4부터 4까지는 2개씩 추가
    for num in range(-4, 5):
        number_pool.extend([num] * 2)
        
    # 규칙 3: 5부터 15까지는 1개씩 추가
    number_pool.extend(list(range(5, 16)))
    
    random.shuffle(number_pool)
    
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
    # 최대 뽑기 횟수를 20으로 설정합니다.
    max_draws = 20
    is_disabled = (st.session_state.draw_count >= max_draws)
    
    if st.button("다음 수 뽑기", disabled=is_disabled, use_container_width=True):
        if st.session_state.pool:
            st.session_state.draw_count += 1
            new_number = st.session_state.pool.pop()
            st.session_state.current_number = new_number
            st.session_state.drawn_history.append(new_number)

# --- 결과 표시 영역 ---
if st.session_state.draw_count == 0:
    st.header("첫 번째 수를 뽑아주세요.")
# is_disabled 변수를 사용하여 20번 뽑았는지 확인합니다.
elif is_disabled:
    st.header("🏁 20개의 수를 모두 뽑았습니다! 🏁")
else:
    st.header(f"{st.session_state.draw_count}번째 수")

st.markdown(
    f"<p style='text-align: center; font-size: 150px; font-weight: bold;'>{st.session_state.current_number}</p>", 
    unsafe_allow_html=True
)

st.divider()

# --- 규칙 및 기록 표시 영역 ---
# 이 부분은 변경할 필요 없이 그대로 작동합니다.
rule_text = "ℹ️ **수 타일 구성:** -15 ~ -5 (각 10개), -4 ~ 4 (각 2개), 5 ~ 15 (각 1개)"
history_title = "**※ 지금까지 뽑은 수들:**"

if st.session_state.drawn_history:
    history_values = "  ➡️  ".join(map(str, st.session_state.drawn_history))
else:
    history_values = "아직 뽑은 수가 없습니다."

info_box_content = f"""{rule_text}
---
{history_title} {history_values}
"""

st.info(info_box_content)