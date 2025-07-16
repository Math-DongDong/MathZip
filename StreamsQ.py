# StreamsQ.py

import streamlit as st
import random
from StreamsSideBar import Draw_sidebar

# 사이드바를 활성화합니다.
Draw_sidebar()

# 유리수 latex를 키우기 위한 CSS문법 추가
st.markdown("""
<style>
.stLatex .katex-display .katex {
    font-size: 15em;  /* 이 값을 조절하여 원하는 크기를 맞추세요 (예: 6em, 7em) */
}
</style>
""", unsafe_allow_html=True)

st.title("유리수 스트림스 카드 뽑기")
st.divider()

# --- '유리수 버전'만의 고유한 게임 초기화 함수 ---
def initialize_game_Q():
    """'유리수 버전'을 위한 게임 상태를 초기화합니다."""
    number_pool = []

    # --- 여기가 핵심 변경점 1: 유리수 규칙에 따라 숫자 풀 생성 ---

    # 규칙 1: ±10/2 ~ ±1/2 (각 1장씩, 총 20장)
    # LaTeX 형식으로 분수를 만듭니다: \frac{분자}{분모}
    for i in range(1, 11):
        number_pool.append(f"\\frac{{{i}}}{{2}}")
        number_pool.append(f"-\\frac{{{i}}}{{2}}")

    # 규칙 2: 분모가 3인 분수들 (총 8장)
    number_pool.append( "\\frac{7}{3}"); number_pool.append("-\\frac{7}{3}")  # ±7/3
    number_pool.append( "\\frac{5}{3}"); number_pool.append("-\\frac{5}{3}")  # ±5/3
    number_pool.append( "\\frac{4}{3}"); number_pool.append("-\\frac{4}{3}")  # ±4/3
    number_pool.append( "\\frac{1}{3}"); number_pool.append("-\\frac{1}{3}")  # ±1/3

    # 규칙 3: ±5 ~ ±1 (각 1장씩, 총 10장)
    # 정수는 문자열 그대로 추가합니다. st.latex는 정수도 잘 표현합니다.
    for i in range(1, 6):
        number_pool.append(str(i))
        number_pool.append(str(-i))

    # 규칙 4: 0 (2장)
    number_pool.extend(["0", "0"])

    # 생성된 숫자 풀을 무작위로 섞습니다.
    random.shuffle(number_pool)
    
    # '유리수 버전'만의 고유한 세션 상태(_Q 접미사)를 초기화합니다.
    st.session_state.pool_Q = number_pool
    st.session_state.draw_count_Q = 0
    st.session_state.current_number_Q = "❔"
    st.session_state.drawn_history_Q = []

# --- 메인 앱 로직 ---
# '유리수 버전' 페이지가 로드될 때, 자신만의 세션 상태를 확인하고 없으면 초기화합니다.
if 'pool_Q' not in st.session_state:
    initialize_game_Q()

# --- 상단 버튼 영역 ---
col1, col_spacer, col2 = st.columns([1,2,1])

with col1:
    # 버튼에 고유한 key를 부여하여 다른 페이지 버튼과 충돌을 방지합니다.
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
    st.header(f"{st.session_state.draw_count_Q}번째 수")

# --- 여기가 핵심 변경점 2: st.markdown 대신 st.latex 사용 ---
# 폰트 크기 조절은 st.latex에서 직접 지원하지 않으므로, 기본 크기로 멋지게 표시됩니다.
st.latex(st.session_state.current_number_Q)

st.divider()

# --- 규칙 및 기록 표시 영역 ---

# --- 여기가 핵심 변경점 3: 규칙 텍스트를 새로운 내용으로 변경 ---
rule_text = r"""
ℹ️ **유리수 타일 구성 (총 40장)**
- **분모 2:** $\pm\frac{10}{2} \sim \pm\frac{1}{2}$ (각 1장)
- **분모 3:** $-\frac{7}{3}, \pm\frac{5}{3}, \pm\frac{4}{3}, \pm\frac{1}{3}, \frac{7}{3}$(조커) (각 1장)
- **정수:** $\pm5 \sim \pm1$ (각 1장), $0$ (2장)
"""
history_title = "**※ 지금까지 뽑은 유리수들:**"

# 기록 표시는 LaTeX 형식을 그대로 보여주면 됩니다.
if st.session_state.drawn_history_Q:
    # st.latex는 리스트를 직접 렌더링하지 않으므로, 문자열로 만듭니다.
    # 각 LaTeX 문자열을 $...$로 감싸 인라인 수식처럼 보이게 합니다.
    history_values = ", ".join([f"${s}$" for s in st.session_state.drawn_history_Q])
else:
    history_values = "아직 뽑은 유수가 없습니다."

info_box_content = f"""{rule_text}
---
{history_title}

{history_values}
"""

st.info(info_box_content)