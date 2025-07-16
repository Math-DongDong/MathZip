# StreamsQ.py

import streamlit as st
import random
from StreamsSideBar import Draw_sidebar

# 사이드바를 활성화합니다.
Draw_sidebar()

# --- 여기가 핵심 변경점입니다: 올바른 CSS 선택자로 수정 ---
# 유리수 latex를 키우기 위한 CSS문법 추가
st.markdown("""
<style>
.stMarkdown .katex-display .katex {
    font-size: 5em;  /* 이 값을 5, 6, 8 등으로 조절하여 원하시는 크기를 찾으세요. */
}
</style>
""", unsafe_allow_html=True)

st.title("유리수 스트림스 카드 뽑기")
st.divider()

# --- '유리수 버전'만의 고유한 게임 초기화 함수 ---
def initialize_game_Q():
    """'유리수 버전'을 위한 게임 상태를 초기화합니다."""
    number_pool = []

    # 규칙 1: ±10/2 ~ ±1/2 (각 1장씩, 총 20장)
    for i in range(1, 11):
        number_pool.append(f"\\frac{{{i}}}{{2}}")
        number_pool.append(f"-\\frac{{{i}}}{{2}}")

    # 규칙 2: 분모가 3인 분수들 (총 8장)
    number_pool.append( "\\frac{7}{3}"); number_pool.append("-\\frac{7}{3}")
    number_pool.append( "\\frac{5}{3}"); number_pool.append("-\\frac{5}{3}")
    number_pool.append( "\\frac{4}{3}"); number_pool.append("-\\frac{4}{3}")
    number_pool.append( "\\frac{1}{3}"); number_pool.append("-\\frac{1}{3}")

    # 규칙 3: ±5 ~ ±1 (각 1장씩, 총 10장)
    for i in range(1, 6):
        number_pool.append(str(i))
        number_pool.append(str(-i))

    # 규칙 4: 0 (2장)
    number_pool.extend(["0", "0"])

    random.shuffle(number_pool)
    
    st.session_state.pool_Q = number_pool
    st.session_state.draw_count_Q = 0
    st.session_state.current_number_Q = "❔"
    st.session_state.drawn_history_Q = []

# --- 메인 앱 로직 ---
if 'pool_Q' not in st.session_state:
    initialize_game_Q()

# --- 상단 버튼 영역 ---
col1, col_spacer, col2 = st.columns([1,2,1])

with col1:
    if st.button("  처음부터 다시하기  ", type="primary", use_container_width=True, key="restart_Q"):
        initialize_game_Q()
        st.rerun()

with col2:
    max_draws = 20
    is_disabled = (st.session_state.draw_count_Q >= max_draws)
    
    if st.button("다음 유리수 뽑기", disabled=is_disabled, use_container_width=True, key="draw_Q"):
        if st.session_state.pool_Q:
            st.session_state.draw_count_Q += 1
            new_number = st.session_state.pool_Q.pop()
            st.session_state.current_number_Q = new_number
            st.session_state.drawn_history_Q.append(new_number)

# --- 결과 표시 영역 ---
if st.session_state.draw_count_Q == 0:
    st.header("첫 번째 유리수를 뽑아주세요.")
elif is_disabled:
    st.header("🏁 20개의 유리수를 모두 뽑았습니다! 🏁")
else:
    st.header(f"{st.session_state.draw_count_Q}번째 유리수")

st.latex(st.session_state.current_number_Q)

st.divider()

# --- 규칙 및 기록 표시 영역 ---
rule_text = r"""
ℹ️ **유리수 타일 구성 (총 40장)**
- **분모 2:** $\pm\frac{10}{2} \sim \pm\frac{1}{2}$ (각 1장)
- **분모 3:** $-\frac{7}{3}, \pm\frac{5}{3}, \pm\frac{4}{3}, \pm\frac{1}{3}, \frac{7}{3}$(조커) (각 1장)
- **정수:** $\pm5 \sim \pm1$ (각 1장), $0$ (2장)
"""
history_title = "**※ 지금까지 뽑은 유리수들:**"

if st.session_state.drawn_history_Q:
    history_values = ", ".join([f"${s}$" for s in st.session_state.drawn_history_Q])
else:
    history_values = "아직 뽑은 유수가 없습니다."

info_box_content = f"""{rule_text}
---
{history_title}

{history_values}
"""

st.info(info_box_content)