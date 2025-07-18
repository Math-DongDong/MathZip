# StreamsQ.py

import streamlit as st
import random
from StreamsSideBar import Draw_sidebar

# 사이드바를 활성화합니다.
Draw_sidebar()

# --- 여기가 최종 핵심 변경점 1 ---
# .rule-text-block 관련 CSS 코드를 모두 삭제했습니다.
st.markdown("""
<style>
/* 메인에 표시되는 큰 수식 */
.stMarkdown .katex-display .katex {
    font-size: 6em;
    margin-top: 0.5em;
}

/* 오른쪽 열 스타일을 제거했으므로 관련 클래스 정의가 없습니다. */

</style>
""", unsafe_allow_html=True)

st.title("🔢 유리수 타일 뽑기")
st.divider()

# --- 게임 초기화 로직 등 (변경 없음) ---
def initialize_game_Q():
    number_pool = []
    for i in range(1, 11): number_pool.append(f"\\frac{{{i}}}{{2}}"); number_pool.append(f"-\\frac{{{i}}}{{2}}")
    for i in range(1, 6): number_pool.append(str(i)); number_pool.append(str(-i))
    number_pool.extend(["\\frac{5}{3}", "-\\frac{5}{3}", "\\frac{4}{3}", "-\\frac{4}{3}", "\\frac{2}{3}", "-\\frac{2}{3}", "\\frac{1}{3}", "-\\frac{1}{3}", "0", "0"])
    random.shuffle(number_pool)
    st.session_state.pool_Q, st.session_state.draw_count_Q, st.session_state.current_number_Q, st.session_state.drawn_history_Q = number_pool, 0, "❔", []

if 'pool_Q' not in st.session_state:
    initialize_game_Q()

col1, col_spacer, col2 = st.columns([1,2,1])

with col1:
    if st.button("  처음부터 다시하기  ", type="primary", use_container_width=True, key="restart_Q"):
        initialize_game_Q()
        st.rerun()

with col2:
    is_disabled = (st.session_state.draw_count_Q >= 20)
    if st.button("다음 유리수 뽑기", disabled=is_disabled, use_container_width=True, key="draw_Q"):
        if st.session_state.pool_Q:
            st.session_state.draw_count_Q += 1
            new_number = st.session_state.pool_Q.pop()
            st.session_state.current_number_Q = new_number
            st.session_state.drawn_history_Q.append(new_number)

if st.session_state.draw_count_Q == 0:
    st.header("첫 번째 유리수를 뽑아주세요.")
elif st.session_state.draw_count_Q >= 20:
    st.header("🏁 20개의 유리수를 모두 뽑았습니다! 🏁")
else:
    st.header(f"{st.session_state.draw_count_Q}번째 유리수")

left_col, right_col = st.columns([2, 1])

with left_col:
    if st.session_state.current_number_Q == "❔":
        st.markdown(
            f"<p style='text-align: center; font-size: 150px; font-weight: bold;'>{st.session_state.current_number_Q}</p>", 
            unsafe_allow_html=True
        )
    else:
        st.latex(st.session_state.current_number_Q)

# --- 여기가 최종 핵심 변경점 2 ---
with right_col:
    # <div> 태그를 감싸던 st.markdown 두 줄을 제거했습니다.
    # 이제 순수하게 st.write만 남아 기본 스타일로 출력됩니다.

    # "유리수 타일 구성" 텍스트
    st.write(ℹ️ **유리수 타일 구성:**)
    st.write(r"- $0$ (2개)")
    st.write(r"- 절댓값이 $1 \sim 5$ 인 수")
    st.write(r"- 절댓값이 $\frac{1}{2} \sim \frac{10}{2}$ 인 수")
    st.write(r"- 절댓값이 $\frac{1}{3}, \frac{2}{3}, \frac{4}{3}, \frac{5}{3}$ 인 수")              
    
st.divider() 

history_title = "**※ 지금까지 뽑은 유리수들:**"

if st.session_state.drawn_history_Q:
    history_values =  "  ➡️  ".join([f"${s}$" for s in st.session_state.drawn_history_Q])
else:
    history_values = "아직 뽑은 유리수가 없습니다."

st.info(f"{history_title} {history_values}")