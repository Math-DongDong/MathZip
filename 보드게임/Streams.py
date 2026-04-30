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
pdf_path = "./기타/스트림스_게임판.pdf"
PDFbyte = None
# 파일이 없을 경우를 대비해 try-except 구문으로 감싸는 것이 더 안정적입니다.
try:
    with open(pdf_path, "rb") as pdf_file:
        PDFbyte = pdf_file.read()
except FileNotFoundError:
    # PDF 파일이 없어도 앱이 멈추지 않도록 처리
    pass

st.title("🔢 스트림스")

# --- 탭 구성 ---
tabs = st.tabs(["게임방법", "기본 버전", "정수 버전", "유리수 버전"])

# --- 1. 게임방법 탭 ---
with tabs[0]:
    st.video("https://youtu.be/gq4UmK0MRbE?si=caJJ4gh-hdnC8OvL")
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
    def initialize_game(joker=False):
        number_pool = []
        number_pool.extend(list(range(1, 11)))
        number_pool.extend(list(range(11, 21)))
        number_pool.extend(list(range(11, 21)))
        number_pool.extend(list(range(21, 31)))
        if joker:
            number_pool.append("⭐")
        random.shuffle(number_pool)
        st.session_state.pool = number_pool
        st.session_state.draw_count = 0
        st.session_state.current_number = "❔"
        st.session_state.drawn_history = []
        st.session_state.last_joker_base = joker

    if 'joker_base' not in st.session_state:
        st.session_state.joker_base = False

    if 'pool' not in st.session_state:
        initialize_game(st.session_state.joker_base)

    # 첫 번째 뽑기 전까지만 조커 체크박스 토글이 반영되도록 (풀 재생성)
    if st.session_state.draw_count == 0 and st.session_state.get('last_joker_base') != st.session_state.joker_base:
        initialize_game(st.session_state.joker_base)

    col1, col_spacer, col2 = st.columns([1,2,1])
    with col1:
        if st.button("  처음부터 다시하기  ", type="primary",width='stretch', key="restart_base"):
            initialize_game(st.session_state.joker_base)
            st.rerun()
    with col_spacer:
        st.checkbox("⭐ 카드 추가", key="joker_base", disabled=(st.session_state.draw_count > 0))
    with col2:
        is_disabled = (st.session_state.draw_count >= 19)
        if st.button("다음 숫자 뽑기", disabled=is_disabled, width='stretch', key="draw_base"):
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
    def initialize_game_Z(joker=False):
        number_pool = []
        number_pool.extend(list(range(-15, -4)))
        for num in range(-4, 5):
            number_pool.extend([num] * 2)
        number_pool.extend(list(range(5, 16)))
        if joker:
            number_pool.append("⭐")
        random.shuffle(number_pool)
        st.session_state.pool_Z = number_pool
        st.session_state.draw_count_Z = 0
        st.session_state.current_number_Z = "❔"
        st.session_state.drawn_history_Z = []
        st.session_state.last_joker_Z = joker

    if 'joker_Z' not in st.session_state:
        st.session_state.joker_Z = False

    if 'pool_Z' not in st.session_state:
        initialize_game_Z(st.session_state.joker_Z)

    if st.session_state.draw_count_Z == 0 and st.session_state.get('last_joker_Z') != st.session_state.joker_Z:
        initialize_game_Z(st.session_state.joker_Z)

    col1, col_spacer, col2 = st.columns([1,2,1])
    with col1:
        if st.button("  처음부터 다시하기  ", type="primary",width='stretch', key="restart_Z"):
            initialize_game_Z(st.session_state.joker_Z)
            st.rerun()
    with col_spacer:
        st.checkbox("⭐ 카드 추가", key="joker_Z", disabled=(st.session_state.draw_count_Z > 0))

    with col2:
        is_disabled = (st.session_state.draw_count_Z >= 19)
        if st.button("다음 정수 뽑기", disabled=is_disabled, width='stretch', key="draw_Z"):
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
    def initialize_game_Q(joker=False):
        number_pool = []
        for i in range(1, 7): number_pool.append(f"\\frac{{{i}}}{{2}}"); number_pool.append(f"-\\frac{{{i}}}{{2}}")
        number_pool.extend(["2.7", "-2.7"])
        number_pool.extend(["\\frac{5}{3}", "-\\frac{5}{3}", "\\frac{4}{3}", "-\\frac{4}{3}", "\\frac{2}{3}", "-\\frac{2}{3}", "\\frac{1}{3}", "-\\frac{1}{3}", "0","\\frac{1}{2}","\\frac{3}{2}","\\frac{5}{2}","-\\frac{1}{2}","-\\frac{3}{2}","-\\frac{5}{2}"])
        if joker:
            number_pool.append("⭐")
        random.shuffle(number_pool)
        st.session_state.pool_Q, st.session_state.draw_count_Q, st.session_state.current_number_Q, st.session_state.drawn_history_Q = number_pool, 0, "❔", []
        st.session_state.last_joker_Q = joker
    if 'joker_Q' not in st.session_state:
        st.session_state.joker_Q = False

    if 'pool_Q' not in st.session_state:
        initialize_game_Q(st.session_state.joker_Q)

    # 첫 번째 뽑기 전까지만 조커 체크박스 토글이 반영되도록 (풀 재생성)
    if st.session_state.draw_count_Q == 0 and st.session_state.get('last_joker_Q') != st.session_state.joker_Q:
        initialize_game_Q(st.session_state.joker_Q)

    col1, col_spacer, col2 = st.columns([1,2,1])
    with col1:
        if st.button("  처음부터 다시하기  ", type="primary", width='stretch', key="restart_Q"):
            initialize_game_Q(st.session_state.joker_Q)
            st.rerun()
    with col_spacer:   
        st.checkbox("⭐ 카드 추가", key="joker_Q", disabled=(st.session_state.draw_count_Q > 0))
    with col2:
        is_disabled = (st.session_state.draw_count_Q >= 19)
        if st.button("다음 유리수 뽑기", disabled=is_disabled, width='stretch', key="draw_Q"):
            if st.session_state.pool_Q:
                st.session_state.draw_count_Q += 1
                new_number = st.session_state.pool_Q.pop()
                st.session_state.current_number_Q = new_number
                st.session_state.drawn_history_Q.append(new_number)
    left_col, right_col = st.columns([1, 1])
    with left_col:
        if st.session_state.draw_count_Q == 0: st.header("첫 번째 유리수를 뽑아주세요.")
        elif st.session_state.draw_count_Q >= 20: st.header("🏁 모든 유리수를 뽑았습니다! 🏁")
        else: st.header(f"{st.session_state.draw_count_Q}번째 유리수")
        if st.session_state.current_number_Q in ("❔", "⭐"):
            st.markdown(f"<p style='text-align: center; font-size: 150px; font-weight: bold;'>{st.session_state.current_number_Q}</p>", unsafe_allow_html=True)
        else:
            st.latex(st.session_state.current_number_Q)
    with right_col:
        # [핵심 수정] "부수 효과"를 활용한 커스텀 HTML/CSS 정보 패널
        st.markdown(r"""
        <div class="info-panel">
                    
        ℹ️ **유리수 타일 구성(총 27개)**
        - 절댓값이 $0,\ 1,\ 2,\ 2.7$ 인 수
        - 절댓값이 $\frac{1}{2},\ \frac{3}{2},\ \frac{5}{2}$ 인 수
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
