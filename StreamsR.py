# StreamsR.py

import streamlit as st
import random
from StreamsSideBar import Draw_sidebar

# 사이드바를 활성화합니다.
Draw_sidebar()

# [핵심 수정 1] 유리수 버전의 CSS 스타일을 그대로 가져옵니다.
# 폰트 크기는 보기 좋게 1.2em으로 조정했으며, 원하시면 얼마든지 변경 가능합니다.
st.markdown("""
<style>
/* 메인에 표시되는 큰 수식 */
.stMarkdown .katex-display .katex {
    font-size: 8em;
}

/* 오른쪽 정보 패널의 폰트 크기를 조절합니다. */
.info-panel {
    font-size: 1.5em; /* 텍스트가 너무 크면 1.0em 이나 1.1em으로 조정하세요. */
}
</style>
""", unsafe_allow_html=True)

st.title("🔢 실수 뽑기")
st.divider()

# [핵심 수정 2] 새로운 실수 타일 구성에 맞게 게임 초기화 함수를 완전히 재작성합니다.
def initialize_game_R():
    """요청하신 규칙에 따라 실수가 담긴 숫자 풀(pool)을 생성합니다."""
    number_pool = []

    # 규칙 1: 절댓값이 0에서 4인 수 (정수)
    # 0, ±1, ±2, ±3, ±4 (총 9개)
    number_pool.append("0")
    for i in range(1, 5):
        number_pool.append(str(i))
        number_pool.append(str(-i))

    # 규칙 2: 절댓값이 루트0에서 루트9인 수
    # ±√0, ±√1, ..., ±√9 (정수와 겹치는 것도 있지만, 표현을 위해 모두 추가)
    # LaTeX 문법을 사용하기 위해 백슬래시를 두 번 (\\) 사용합니다.
    number_pool.append("\\sqrt{0}")
    for i in range(1, 10):
        number_pool.append(f"\\sqrt{{{i}}}")
        number_pool.append(f"-\\sqrt{{{i}}}")

    # 규칙 3: 지정된 특정 실수들 (총 8개)
    specific_reals = [
        "-2-\\sqrt{5}", "-1-\\sqrt{5}", "1-\\sqrt{3}", "-2+\\sqrt{3}",
        "2-\\sqrt{3}", "-3+\\sqrt{3}", "1+\\sqrt{5}", "2+\\sqrt{5}"
    ]
    number_pool.extend(specific_reals)
    
    random.shuffle(number_pool)
    
    # 세션 상태 변수 이름을 '_R' 접미사를 붙여 유리수 버전과 겹치지 않게 합니다.
    st.session_state.pool_R = number_pool
    st.session_state.draw_count_R = 0
    st.session_state.current_number_R = "❔"
    st.session_state.drawn_history_R = []
    # 전체 타일 개수를 저장하여 버튼 비활성화에 사용합니다. (총 9 + 19 + 8 = 36개)
    st.session_state.total_tiles_R = len(number_pool)


# 메인 앱 로직
if 'pool_R' not in st.session_state:
    initialize_game_R()

# --- 상단 버튼 영역 ---
col1, col_spacer, col2 = st.columns([1,2,1])

with col1:
    if st.button("  처음부터 다시하기  ", type="primary", use_container_width=True, key="restart_R"):
        initialize_game_R()
        st.rerun()

with col2:
    # [수정된 부분] 20개를 뽑으면 버튼이 비활성화되도록 조건을 변경합니다.
    is_disabled = (st.session_state.draw_count_R >= 19)
    if st.button("다음 실수 뽑기", disabled=is_disabled, use_container_width=True, key="draw_R"):
        if st.session_state.pool_R:
            st.session_state.draw_count_R += 1
            new_number = st.session_state.pool_R.pop()
            st.session_state.current_number_R = new_number
            st.session_state.drawn_history_R.append(new_number)

# --- 결과 표시 헤더 ---
if st.session_state.draw_count_R == 0:
    st.header("첫 번째 실수를 뽑아주세요.")
elif st.session_state.draw_count_R >= 20: # 이 부분도 20으로 맞춰주면 더 일관성 있습니다.
    st.header(f"🏁 20개의 실수를 모두 뽑았습니다! 🏁")
else:
    st.header(f"{st.session_state.draw_count_R}번째 실수")

# [핵심 수정 3] 유리수 버전처럼 좌우 레이아웃을 적용합니다.
left_col, right_col = st.columns([1, 1])

with left_col:
    # 현재 뽑힌 숫자를 표시하는 로직
    if st.session_state.current_number_R == "❔":
        # 처음에는 물음표를 큰 텍스트로 표시
        st.markdown(
            f"<p style='text-align: center; font-size: 150px; font-weight: bold;'>{st.session_state.current_number_R}</p>", 
            unsafe_allow_html=True
        )
    else:
        # 뽑힌 후에는 st.latex를 사용하여 수식을 아름답게 표시
        st.latex(st.session_state.current_number_R)

with right_col:
    # 오른쪽에는 타일 구성 정보를 표시
    # 하나의 st.markdown 블록과 사용자 정의 div를 사용하여 스타일을 일관되게 적용
    st.markdown(r"""
    <div class="info-panel">

    ℹ️ **실수 타일 구성(총 30개)**
    - 절댓값이 $0,\ 1,\ 2,\ 3.\dot{9}$ 인 수
    - 절댓값이 $\sqrt{0} \sim \sqrt{9}$ 인 수
    - $-1-\sqrt{5},\ 1+\sqrt{5}$ 
    - $1-\sqrt{3},\ -2+\sqrt{3},\ 2-\sqrt{3},\ -3+\sqrt{3}$
    </div>
    """, unsafe_allow_html=True)

st.divider() 

# [핵심 수정 4] 하단의 기록 표시 부분도 LaTeX 수식이 잘 보이도록 수정합니다.
history_title = "**※ 지금까지 뽑은 실수들:**"

if st.session_state.drawn_history_R:
    # 각 숫자 문자열을 $...$로 감싸 LaTeX 수식으로 만듭니다.
    history_values =  "  ➡️  ".join([f"${s}$" for s in st.session_state.drawn_history_R])
else:
    history_values = "아직 뽑은 실수가 없습니다."

st.info(f"{history_title} {history_values}")