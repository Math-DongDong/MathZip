# StreamsQ.py

import streamlit as st
import random
from StreamsSideBar import Draw_sidebar

# 사이드바를 활성화합니다.
Draw_sidebar()

# --- 스타일 정의 (변경 없음) ---
st.markdown("""
<style>
/* 메인에 표시되는 큰 수식 */
.stMarkdown .katex-display .katex {
    font-size: 6em;
    margin: 0.5em 0; 
}

/* [수정된 부분] 오른쪽 정보 패널의 폰트 크기를 조절합니다. */
.info-panel {
    font-size: 2.2em; /* 원하시는 크기로 조절하세요. 예를 들어 1.5em, 2em 등 */
}
</style>
""", unsafe_allow_html=True)

st.title("🔢 유리수 뽑기")
st.divider()

# --- 게임 초기화 로직 (핵심 수정 부분) ---
def initialize_game_Q():
    number_pool = []
    for i in range(1, 7): number_pool.append(f"\\frac{{{i}}}{{2}}"); number_pool.append(f"-\\frac{{{i}}}{{2}}")
    for i in range(1, 4): number_pool.append(str(i)); number_pool.append(str(-i))
    
    # --- [수정된 부분] 화면 규칙과 일치시키기 위해 누락된 숫자를 추가합니다. ---
    number_pool.extend(["2.3", "-2.3", "2.7", "-2.7"])
    
    number_pool.extend(["\\frac{5}{3}", "-\\frac{5}{3}", "\\frac{4}{3}", "-\\frac{4}{3}", "\\frac{2}{3}", "-\\frac{2}{3}", "\\frac{1}{3}", "-\\frac{1}{3}", "0", "0"])
    random.shuffle(number_pool)
    st.session_state.pool_Q, st.session_state.draw_count_Q, st.session_state.current_number_Q, st.session_state.drawn_history_Q = number_pool, 0, "❔", []

# --- 이하 모든 코드는 변경 없음 ---

if 'pool_Q' not in st.session_state:
    initialize_game_Q()

col1, col_spacer, col2 = st.columns([1,2,1])

with col1:
    if st.button("  처음부터 다시하기  ", type="primary", use_container_width=True, key="restart_Q"):
        initialize_game_Q()
        st.rerun()

with col2:
    is_disabled = (st.session_state.draw_count_Q >= 19)
    if st.button("다음 유리수 뽑기", disabled=is_disabled, use_container_width=True, key="draw_Q"):
        if st.session_state.pool_Q:
            st.session_state.draw_count_Q += 1
            new_number = st.session_state.pool_Q.pop()
            st.session_state.current_number_Q = new_number
            st.session_state.drawn_history_Q.append(new_number)

left_col, right_col = st.columns([1, 1])
with left_col:
    if st.session_state.draw_count_Q == 0:
        st.header("첫 번째 유리수를 뽑아주세요.")
    elif st.session_state.draw_count_Q >= 20:
        st.header("🏁 20개의 유리수를 모두 뽑았습니다! 🏁")
    else:
        st.header(f"{st.session_state.draw_count_Q}번째 유리수")

    if st.session_state.current_number_Q == "❔":
        st.markdown(
            f"<p style='text-align: center; font-size: 150px; font-weight: bold;'>{st.session_state.current_number_Q}</p>", 
            unsafe_allow_html=True
        )
    else:
        st.latex(st.session_state.current_number_Q)

with right_col:
    st.markdown(r"""
    <div class="info-panel">

    ℹ️ **유리수 타일 구성(총 32개)**
    - $0$ (2개)
    - 절댓값이 $1,\ 2,\ 3$ 인 수
    - 절댓값이 $2.3,\ 2.7$ 인 수
    - 절댓값이 $\frac{1}{2} \sim \frac{6}{2}$ 인 수
    - 절댓값이 $\frac{1}{3},\ \frac{2}{3},\ \frac{4}{3},\ \frac{5}{3}$ 인 수

    </div>
    """, unsafe_allow_html=True)

st.divider() 

history_title = "**※ 지금까지 뽑은 유리수들:**"

if st.session_state.drawn_history_Q:
    history_values =  "  ➡️  ".join([f"${s}$" for s in st.session_state.drawn_history_Q])
else:
    history_values = "아직 뽑은 유리수가 없습니다."

st.info(f"{history_title} {history_values}")