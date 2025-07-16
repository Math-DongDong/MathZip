
import streamlit as st
import random
from StreamsSideBar import Draw_sidebar

# 사이드바를 활성화합니다.
Draw_sidebar()

# --- 여기가 핵심 변경점입니다 ---
# CSS 스타일 규칙을 정보 상자 전체에 적용되도록 수정합니다.
st.markdown("""
<style>
/* 1. 메인에 표시되는 큰 수식을 위한 스타일 (변경 없음) */
.stMarkdown .katex-display .katex {
    font-size: 6em;
    margin-top: 0.5em;
}

/* 2. 정보 상자(st.info) 안의 모든 컨텐츠(텍스트와 수식)의 크기를 함께 키웁니다. */
[data-testid="stAlertContentInfo"] {
    font-size: 1.25em; /* 이 값을 1.5em, 1.8em 등으로 조절하여 원하시는 크기를 찾으세요. */
}
</style>
""", unsafe_allow_html=True)

st.title("🔢 유리수 스트림스 카드 뽑기")
st.divider()

# --- '유리수 버전'만의 고유한 게임 초기화 함수 ---
def initialize_game_Q():
    """'유리수 버전'을 위한 게임 상태를 초기화합니다."""
    number_pool = []
    for i in range(1, 11): number_pool.append(f"\\frac{{{i}}}{{2}}"); number_pool.append(f"-\\frac{{{i}}}{{2}}")
    for i in range(1, 6): number_pool.append(str(i)); number_pool.append(str(-i))
    number_pool.extend(["\\frac{5}{3}", "-\\frac{5}{3}", "\\frac{4}{3}", "-\\frac{4}{3}", "\\frac{2}{3}", "-\\frac{2}{3}", "\\frac{1}{3}", "-\\frac{1}{3}", "0", "0"])
    random.shuffle(number_pool)
    st.session_state.pool_Q, st.session_state.draw_count_Q, st.session_state.current_number_Q, st.session_state.drawn_history_Q = number_pool, 0, "❔", []

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
    is_disabled = (st.session_state.draw_count_Q >= 20)
    
    if st.button("다음 유리수 뽑기", disabled=is_disabled, use_container_width=True, key="draw_Q"):
        if st.session_state.pool_Q:
            st.session_state.draw_count_Q += 1
            new_number = st.session_state.pool_Q.pop()
            st.session_state.current_number_Q = new_number
            st.session_state.drawn_history_Q.append(new_number)

# --- 결과 표시 영역 ---
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

# --- 규칙 및 기록 표시 영역 ---
st.divider()

rule_text = r"""
ℹ️ **유리수 타일 구성:**
- 절댓값이 $\frac{1}{2} \sim \frac{10}{2}$ 인 수
- 절댓값이 $\frac{1}{3}, \frac{2}{3}, \frac{4}{3}, \frac{5}{3}$ 인 수
- 절댓값이 $1 \sim 5$ 인 수
- $0$ (2개)
"""
history_title = "**※ 지금까지 뽑은 유리수들:**"

# 규칙 설명만 st.info에 담아 표시합니다.
st.info(rule_text)

if st.session_state.drawn_history_Q:
    history_values =  "  ➡️  ".join([f"${s}$" for s in st.session_state.drawn_history_Q])
else:
    history_values = "아직 뽑은 유리수가 없습니다."

# 뽑은 기록만 별도의 st.markdown으로 표시합니다.
st.markdown(f"{history_title} {history_values}")