# StreamsR.py

import streamlit as st
import random
from StreamsSideBar import Draw_sidebar

# 사이드바를 활성화합니다.
Draw_sidebar()

# --- CSS 스타일 (변경 없음) ---
st.markdown("""
<style>
/* 메인에 표시되는 큰 수식 */
.stMarkdown .katex-display .katex {
    font-size: 8em;
}

/* 오른쪽 정보 패널의 폰트 크기를 조절합니다. */
.info-panel {
    font-size: 1.5em; 
}
</style>
""", unsafe_allow_html=True)

st.title("🔢 실수 뽑기")
st.divider()

# [핵심 수정 1] 화면의 규칙을 기준으로 게임 초기화 함수를 완벽하게 재작성합니다.
def initialize_game_R():
    """화면에 표시된 규칙과 100% 일치하도록 숫자 풀(pool)을 생성합니다."""
    number_pool = []

    # 규칙 1: 절댓값이 0, 1, 2, 2.9... (즉, 3)인 수
    # 0, ±1, ±2, ±3 (총 7개)
    number_pool.append("0")
    for i in range(1, 4): # range(1, 5)에서 (1, 4)로 수정하여 4를 제외
        number_pool.append(str(i))
        number_pool.append(str(-i))

    # 규칙 2: 절댓값이 √0 ~ √5, 그리고 √9인 수
    # √0, ±√1, ±√2, ±√3, ±√4, ±√5, ±√9 (총 13개)
    number_pool.append("\\sqrt{0}")
    for i in range(1, 6): # range(1, 10)에서 (1, 6)으로 수정하여 √1 ~ √5 까지만
        number_pool.append(f"\\sqrt{{{i}}}")
        number_pool.append(f"-\\sqrt{{{i}}}")
    number_pool.extend(["\\sqrt{9}", "-\\sqrt{9}"]) # √9를 별도로 추가

    # 규칙 3: 지정된 특정 실수들 (총 6개)
    specific_reals = [
        "-1-\\sqrt{5}", "1+\\sqrt{5}",
        "1-\\sqrt{3}", "-1+\\sqrt{3}", "-2+\\sqrt{3}", "2-\\sqrt{3}"
    ]
    number_pool.extend(specific_reals)
    
    random.shuffle(number_pool)
    
    st.session_state.pool_R = number_pool
    st.session_state.draw_count_R = 0
    st.session_state.current_number_R = "❔"
    st.session_state.drawn_history_R = []
    # 전체 타일 개수를 실제 생성된 풀의 길이로 정확하게 설정합니다.
    # 계산: 7 (정수) + 13 (루트) + 6 (특정 실수) = 26개
    st.session_state.total_tiles_R = len(number_pool)


# --- 이하 로직 대부분 변경 없음 ---

if 'pool_R' not in st.session_state:
    initialize_game_R()

col1, col_spacer, col2 = st.columns([1,2,1])

with col1:
    if st.button("  처음부터 다시하기  ", type="primary", use_container_width=True, key="restart_R"):
        initialize_game_R()
        st.rerun()

with col2:
    is_disabled = (st.session_state.draw_count_R >= 19)
    if st.button("다음 실수 뽑기", disabled=is_disabled, use_container_width=True, key="draw_R"):
        if st.session_state.pool_R:
            st.session_state.draw_count_R += 1
            new_number = st.session_state.pool_R.pop()
            st.session_state.current_number_R = new_number
            st.session_state.drawn_history_R.append(new_number)

if st.session_state.draw_count_R == 0:
    st.header("첫 번째 실수를 뽑아주세요.")
elif st.session_state.draw_count_R >= 20: 
    st.header(f"🏁 20개의 실수를 모두 뽑았습니다! 🏁")
else:
    st.header(f"{st.session_state.draw_count_R}번째 실수")

left_col, right_col = st.columns([1, 1])

with left_col:
    if st.session_state.current_number_R == "❔":
        st.markdown(
            f"<p style='text-align: center; font-size: 150px; font-weight: bold;'>{st.session_state.current_number_R}</p>", 
            unsafe_allow_html=True
        )
    else:
        st.latex(st.session_state.current_number_R)

# [핵심 수정 2] 오른쪽 정보 패널의 내용도 실제 로직과 일치하도록 수정합니다.
with right_col:
    # 전체 타일 개수를 session_state에서 동적으로 가져와 표시합니다.
    total_count = st.session_state.get('total_tiles_R', 26) 
    
    # st.markdown의 f-string을 사용하여 동적 값을 텍스트에 삽입합니다.
    # 또한, 이상했던 수식 표현(/)을 수정하고 가독성을 높입니다.
    st.markdown(f"""
    <div class="info-panel">

    ℹ️ **실수 타일 구성 (총 {total_count}개)**
    - 절댓값이 $0,\\ 1,\\ 2,\\ 2.\\dot{{9}}$ 인 수
    - 절댓값이 $\\sqrt{{0}} \\sim \\sqrt{{5}},\\ \\sqrt{{9}}$ 인 수
    - $-1-\\sqrt{{5}},\\ 1+\\sqrt{{5}}$ 
    - $1-\\sqrt{{3}},\\ -1+\\sqrt{{3}},\\ -2+\\sqrt{{3}},\\ 2-\\sqrt{{3}}$
    </div>
    """, unsafe_allow_html=True)

st.divider() 

history_title = "**※ 지금까지 뽑은 실수들:**"

if st.session_state.drawn_history_R:
    history_values =  "  ➡️  ".join([f"${s}$" for s in st.session_state.drawn_history_R])
else:
    history_values = "아직 뽑은 실수가 없습니다."

st.info(f"{history_title} {history_values}")