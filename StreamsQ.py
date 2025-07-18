# StreamsQ.py

import streamlit as st
import random
from StreamsSideBar import Draw_sidebar

# 사이드바를 활성화합니다.
Draw_sidebar()

# --- 여기가 최종 핵심 변경점 1 (CSS 수정) ---
st.markdown("""
<style>
/* 메인에 표시되는 큰 수식 */
.stMarkdown .katex-display .katex {
    font-size: 6em;
    margin-top: 0.5em;
}

/* 오른쪽 열의 규칙 설명을 위한 사용자 정의 클래스 스타일 */
.rule-text-block {
    font-size: 1.2em !important; /* 글씨 크기를 1.2배로 설정합니다. */
    line-height: 1.6;        /* 줄 간격을 살짝 넓혀 가독성을 높입니다. */
}
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

# --- 여기가 최종 핵심 변경점 2 (Python 코드 수정) ---
with right_col:
    # "유리수 타일 구성"에 대한 설명 텍스트 (Raw String으로 유지)
    rule_text = r"""
    ℹ️ **유리수 타일 구성:**
    - $0$ (2개)
    - 절댓값이 $1 \sim 5$ 인 수
    - 절댓값이 $\frac{1}{2} \sim \frac{10}{2}$ 인 수
    - 절댓값이 $\frac{1}{3}, \frac{2}{3}, \frac{4}{3}, \frac{5}{3}$ 인 수
    """
    
    # st.markdown을 사용하여 div 태그와 위에서 정의한 CSS 클래스를 직접 적용합니다.
    # rule_text 내의 LaTeX 수식을 정상적으로 렌더링하기 위해,
    # Markdown 형식으로 변환하는 과정이 필요합니다. Streamlit이 이 부분을 자동으로 처리해 줍니다.
    # 다만, HTML 구조 안에 넣기 위해 약간의 트릭이 필요할 수 있습니다.
    # Streamlit은 Markdown 콘텐츠를 HTML로 먼저 렌더링하므로, 아래 방식이 더 안정적일 수 있습니다.
    # st.markdown(f'<div class="rule-text-block">{rule_text}</div>', unsafe_allow_html=True)
    # 위 방식이 수식 렌더링에 문제를 일으킬 경우, st.write를 컨테이너 안에 넣는 방법도 고려할 수 있습니다.
    # 하지만 이 경우, 가장 간단한 방법은 st.markdown으로 HTML을 직접 제어하는 것입니다.
    # Streamlit의 Markdown 파서는 $...$를 LaTeX로 잘 처리하므로 f-string 방식이 정상 동작해야 합니다.
    
    # 더 안정적인 렌더링을 위해, 텍스트를 HTML p 태그로 감싸는 것이 좋습니다.
    # Markdown의 리스트(-, *)를 HTML 태그(<ul>, <li>)로 변환해주는 것이 가장 좋습니다.
    
    # 최종 권장 코드:
    html_rule_text = """
    <div class="rule-text-block">
        <p>ℹ️ <strong>유리수 타일 구성:</strong></p>
        <ul>
            <li>$0$ (2개)</li>
            <li>절댓값이 $1 \sim 5$ 인 수</li>
            <li>절댓값이 $\\frac{1}{2} \sim \\frac{10}{2}$ 인 수</li>
            <li>절댓값이 $\\frac{1}{3}, \\frac{2}{3}, \\frac{4}{3}, \\frac{5}{3}$ 인 수</li>
        </ul>
    </div>
    """
    # 백슬래시를 이스케이프 처리해야 할 수 있으므로 \\frac으로 변경합니다.
    st.markdown(html_rule_text, unsafe_allow_html=True)


st.divider() 

history_title = "**※ 지금까지 뽑은 유리수들:**"

if st.session_state.drawn_history_Q:
    history_values =  "  ➡️  ".join([f"${s}$" for s in st.session_state.drawn_history_Q])
else:
    history_values = "아직 뽑은 유리수가 없습니다."

# 제일 아래 뽑은 기록도 st.info를 사용하여 파란 상자에 담습니다.
st.info(f"{history_title} {history_values}")