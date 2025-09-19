import streamlit as st
import random # 각 탭에서 중복 import하는 대신 맨 위로 이동

# --- [핵심 수정] 스타일 정의를 맨 위로 통합 ---
# 이 스타일은 앱 전체의 모든 탭에 적용됩니다.
st.markdown("""
<style>
/* 메인에 표시되는 큰 수식 (st.latex) */
.stMarkdown .katex-display .katex {
    font-size: 6em; 
    margin: 0.5em 0;
}
/* 유리수/실수 탭의 정보 패널 폰트 크기 및 줄 간격 조절 */
.info-panel {
    font-size: 2.2em;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# 게임판 PDF 파일 읽기
pdf_path = "스트림스_게임판.pdf"
PDFbyte = None
# 파일이 없을 경우를 대비해 try-except 구문으로 감싸는 것이 더 안정적입니다.
try:
    with open(pdf_path, "rb") as pdf_file:
        PDFbyte = pdf_file.read()
except FileNotFoundError:
    # PDF 파일이 없어도 앱이 멈추지 않도록 처리
    pass

# --- 탭 구성 ---
tabs = st.tabs([
    "게임방법", "기본 버전", "정수 버전", "유리수 버전", "실수 버전"
])

# --- 1. 게임방법 탭 ---
with tabs[0]:
    st.title("🔢 스트림스 규칙 소개")
    st.video("https://youtu.be/gq4UmK0MRbE?si=caJJ4gh-hdnC8OvL")
    st.divider()
    if PDFbyte:
        st.download_button(
            label="게임판 다운로드",
            data=PDFbyte,
            file_name="스트림스_게임판.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("게임판 PDF 파일('스트림스_게임판.pdf')을 찾을 수 없습니다.")


# --- 2. 기본 버전 탭 ---
with tabs[1]:
    st.title("🔢 숫자 뽑기")
    st.divider()
    def initialize_game():
        number_pool = []
        number_pool.extend(list(range(1, 11)))
        number_pool.extend(list(range(11, 21)))
        number_pool.extend(list(range(11, 21)))
        number_pool.extend(list(range(21, 31)))
        random.shuffle(number_pool)
        st.session_state.pool = number_pool
        st.session_state.draw_count = 0
        st.session_state.current_number = "❔"
        st.session_state.drawn_history = []
    if 'pool' not in st.session_state:
        initialize_game()
    col1, col_spacer, col2 = st.columns([1,2,1])
    with col1:
        if st.button("  처음부터 다시하기  ", type="primary",use_container_width=True, key="restart_base"):
            initialize_game()
            st.rerun()
    with col2:
        is_disabled = (st.session_state.draw_count >= 20)
        if st.button("다음 숫자 뽑기", disabled=is_disabled, use_container_width=True, key="draw_base"):
            if st.session_state.pool:
                st.session_state.draw_count += 1
                new_number = st.session_state.pool.pop()
                st.session_state.current_number = new_number
                st.session_state.drawn_history.append(new_number)
    if st.session_state.draw_count == 0:
        st.header("첫 번째 숫자를 뽑아주세요.")
    elif st.session_state.draw_count >= 20:
        st.header("🏁 숫자를 모두 뽑았습니다! 🏁")
    else:
        st.header(f"{st.session_state.draw_count}번째 숫자")
    st.markdown(f"<p style='text-align: center; font-size: 150px; font-weight: bold;'>{st.session_state.current_number}</p>", unsafe_allow_html=True)
    st.divider()
    rule_text = "ℹ️ **숫자 타일 구성:** 1 ~ 10 (각 1개), 11 ~ 20 (각 2개), 21 ~ 30 (각 1개)"
    history_title = "**※ 지금까지 뽑은 숫자들:**"
    if st.session_state.drawn_history:
        history_values = "  ➡️  ".join(map(str, st.session_state.drawn_history))
    else:
        history_values = "아직 뽑은 숫자가 없습니다."
    info_box_content = f"""{rule_text}\n---\n{history_title} {history_values}"""
    st.info(info_box_content)

# --- 3. 정수 버전 탭 ---
with tabs[2]:
    st.title("🔢 정수 뽑기")
    st.divider()
    def initialize_game_Z():
        number_pool = []
        number_pool.extend(list(range(-15, -4)))
        for num in range(-4, 5):
            number_pool.extend([num] * 2)
        number_pool.extend(list(range(5, 16)))
        random.shuffle(number_pool)
        st.session_state.pool_Z = number_pool
        st.session_state.draw_count_Z = 0
        st.session_state.current_number_Z = "❔"
        st.session_state.drawn_history_Z = []
    if 'pool_Z' not in st.session_state:
        initialize_game_Z()
    col1, col_spacer, col2 = st.columns([1,2,1])
    with col1:
        if st.button("  처음부터 다시하기  ", type="primary",use_container_width=True, key="restart_Z"):
            initialize_game_Z()
            st.rerun()
    with col2:
        is_disabled = (st.session_state.draw_count_Z >= 20)
        if st.button("다음 정수 뽑기", disabled=is_disabled, use_container_width=True, key="draw_Z"):
            if st.session_state.pool_Z:
                st.session_state.draw_count_Z += 1
                new_number = st.session_state.pool_Z.pop()
                st.session_state.current_number_Z = new_number
                st.session_state.drawn_history_Z.append(new_number)
    if st.session_state.draw_count_Z == 0:
        st.header("첫 번째 정수를 뽑아주세요.")
    elif st.session_state.draw_count_Z >= 20:
        st.header("🏁 20개의 정수를 모두 뽑았습니다! 🏁")
    else:
        st.header(f"{st.session_state.draw_count_Z}번째 정수")
    st.markdown(f"<p style='text-align: center; font-size: 150px; font-weight: bold;'>{st.session_state.current_number_Z}</p>", unsafe_allow_html=True)
    st.divider()
    rule_text = "ℹ️ **정수 타일 구성:** -15 ~ -5 (각 1개), -4 ~ 4 (각 2개), 5 ~ 15 (각 1개)"
    history_title = "**※ 지금까지 뽑은 정수들:**"
    if st.session_state.drawn_history_Z:
        history_values = "  ➡️  ".join(map(str, st.session_state.drawn_history_Z))
    else:
        history_values = "아직 뽑은 정수가 없습니다."
    info_box_content = f"""{rule_text}\n---\n{history_title} {history_values}"""
    st.info(info_box_content)

# --- 4. 유리수 버전 탭 ---
with tabs[3]:
    st.title("🔢 유리수 뽑기")
    st.divider()
    def initialize_game_Q():
        number_pool = []
        for i in range(1, 7): number_pool.append(f"\\frac{{{i}}}{{2}}"); number_pool.append(f"-\\frac{{{i}}}{{2}}")
        for i in range(1, 4): number_pool.append(str(i)); number_pool.append(str(-i))
        number_pool.extend(["2.3", "-2.3", "2.7", "-2.7"])
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
        is_disabled = (st.session_state.draw_count_Q >= 32)
        if st.button("다음 유리수 뽑기", disabled=is_disabled, use_container_width=True, key="draw_Q"):
            if st.session_state.pool_Q:
                st.session_state.draw_count_Q += 1
                new_number = st.session_state.pool_Q.pop()
                st.session_state.current_number_Q = new_number
                st.session_state.drawn_history_Q.append(new_number)
    left_col, right_col = st.columns([1, 1])
    with left_col:
        if st.session_state.draw_count_Q == 0: st.header("첫 번째 유리수를 뽑아주세요.")
        elif st.session_state.draw_count_Q >= 32: st.header("🏁 모든 유리수를 뽑았습니다! 🏁")
        else: st.header(f"{st.session_state.draw_count_Q}번째 유리수")
        if st.session_state.current_number_Q == "❔":
            st.markdown(f"<p style='text-align: center; font-size: 150px; font-weight: bold;'>{st.session_state.current_number_Q}</p>", unsafe_allow_html=True)
        else:
            st.latex(st.session_state.current_number_Q)
    with right_col:
        # [핵심 수정] "부수 효과"를 활용한 커스텀 HTML/CSS 정보 패널
        st.markdown(r"""
        <div class="info-panel">
                    
        ℹ️ **유리수 타일 구성(총 32개)**
        - $0$ (2개)
        - 절댓값이 $1,\ 2,\ 3$ 인 수
        - 절댓값이 $2.3,\ 2.7$ 인 수
        - 절댓값이 $\frac{1}{2}, \dots, \frac{6}{2}$ 인 수
        - 절댓값이 $\frac{1}{3},\ \frac{2}{3},\ \frac{4}{3},\ \frac{5}{3}$ 인 수
        </div>
        """, unsafe_allow_html=True)
    st.divider() 
    history_title = "**※ 지금까지 뽑은 유리수들:**"
    if st.session_state.drawn_history_Q:
        history_values =  "  ➡️  ".join([f"${s}$" for s in st.session_state.drawn_history_Q])
    else:
        history_values = "아직 뽑은 유리수가 없습니다."
    st.info(f"{history_title}\n\n{history_values}")

# --- 5. 실수 버전 탭 ---
with tabs[4]:
    st.title("🔢 실수 뽑기")
    st.divider()
    def initialize_game_R():
        number_pool = []
        number_pool.append("0")
        for i in range(1, 3): number_pool.append(str(i)); number_pool.append(str(-i))
        number_pool.extend(["2.\\dot{9}", "-2.\\dot{9}"])
        number_pool.append("\\sqrt{0}")
        for i in range(1, 6): number_pool.append(f"\\sqrt{{{i}}}"); number_pool.append(f"-\\sqrt{{{i}}}")
        number_pool.extend(["\\sqrt{9}", "-\\sqrt{9}"])
        specific_reals = ["-1-\\sqrt{5}", "1+\\sqrt{5}", "1-\\sqrt{3}", "-1+\\sqrt{3}", "-2+\\sqrt{3}", "2-\\sqrt{3}"]
        number_pool.extend(specific_reals)
        random.shuffle(number_pool)
        st.session_state.pool_R, st.session_state.draw_count_R, st.session_state.current_number_R, st.session_state.drawn_history_R = number_pool, 0, "❔", []
    if 'pool_R' not in st.session_state:
        initialize_game_R()
    col1, col_spacer, col2 = st.columns([1,2,1])
    with col1:
        if st.button("  처음부터 다시하기  ", type="primary", use_container_width=True, key="restart_R"):
            initialize_game_R()
            st.rerun()
    with col2:
        is_disabled = (st.session_state.draw_count_R >= 26)
        if st.button("다음 실수 뽑기", disabled=is_disabled, use_container_width=True, key="draw_R"):
            if st.session_state.pool_R:
                st.session_state.draw_count_R += 1
                new_number = st.session_state.pool_R.pop()
                st.session_state.current_number_R = new_number
                st.session_state.drawn_history_R.append(new_number)
    left_col, right_col = st.columns([2, 3])
    with left_col:
        if st.session_state.draw_count_R == 0: st.header("첫 번째 실수를 뽑아주세요.")
        elif st.session_state.draw_count_R >= 26: st.header("🏁 모든 실수를 모두 뽑았습니다! 🏁")
        else: st.header(f"{st.session_state.draw_count_R}번째 실수")
        if st.session_state.current_number_R == "❔":
            st.markdown(f"<p style='text-align: center; font-size: 150px; font-weight: bold;'>{st.session_state.current_number_R}</p>", unsafe_allow_html=True)
        else:
            st.latex(st.session_state.current_number_R)
    with right_col:
        # [핵심 수정] "부수 효과"를 활용한 커스텀 HTML/CSS 정보 패널
        st.markdown(r"""
        <div class="info-panel">
                    
        ℹ️ **실수 타일 구성 (총 26개)**
        - 절댓값이 $0,\ 1,\ 2,\ 2.\dot{9}$ 인 수
        - 절댓값이 $\sqrt{0}, \dots, \sqrt{5}$ 및 $\sqrt{9}$ 인 수
        - $-1-\sqrt{5},\ 1+\sqrt{5}$
        - $1-\sqrt{3},\ -1+\sqrt{3},\ -2+\sqrt{3},\ 2-\sqrt{3}$
        </div>
        """, unsafe_allow_html=True)
    st.divider() 
    history_title = "**※ 지금까지 뽑은 실수들:**"
    if st.session_state.drawn_history_R:
        history_values =  "  ➡️  ".join([f"${s}$" for s in st.session_state.drawn_history_R])
    else:
        history_values = "아직 뽑은 실수가 없습니다."
    st.info(f"{history_title}\n\n{history_values}")