import streamlit as st
import random

# -----------------------------------------------------------------------------
# 2. 게임 로직 함수 정의
# -----------------------------------------------------------------------------
def generate_target_number(length):
    digits = list("0123456789")
    first_digit = random.choice(list("123456789"))
    digits.remove(first_digit)
    rest_digits = random.sample(digits, length - 1)
    return first_digit + "".join(rest_digits)

def check_guess(guess, target):
    strikes = sum(1 for i in range(len(guess)) if guess[i] == target[i])
    balls = sum(1 for i in range(len(guess)) if guess[i] != target[i] and guess[i] in target)
    outs = len(target) - strikes - balls
    return strikes, balls, outs

# -----------------------------------------------------------------------------
# 3. 세션 상태(Session State) 초기화
# -----------------------------------------------------------------------------
if 'target_number' not in st.session_state:
    st.session_state.target_number = None
if 'history' not in st.session_state:
    st.session_state.history =[]
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'digit_length' not in st.session_state:
    st.session_state.digit_length = 4
if 'current_guess' not in st.session_state:
    st.session_state.current_guess =[]
if 'error_msg' not in st.session_state:
    st.session_state.error_msg = "" # 경고 메시지를 담을 공간 추가

def start_new_game(length=None):
    if length is None:
        length = st.session_state.digit_length
    st.session_state.target_number = generate_target_number(length)
    st.session_state.history =[]
    st.session_state.game_over = False
    st.session_state.digit_length = length
    st.session_state.current_guess =[]
    st.session_state.error_msg = ""

if st.session_state.target_number is None:
    start_new_game()

# ⭐ [핵심 해결책] 확인 버튼을 눌렀을 때 실행될 콜백(Callback) 함수
def handle_submit():
    # 1. 입력된 숫자 가져오기
    user_guess = "".join(st.session_state.current_guess)
    
    # 2. 자릿수 검사
    if len(user_guess) != st.session_state.digit_length:
        st.session_state.error_msg = f"⚠️ {st.session_state.digit_length}개의 숫자를 모두 선택해 주세요!"
    else:
        # 3. 정상 입력 시 로직 처리
        st.session_state.error_msg = "" # 에러 메시지 초기화
        s, b, o = check_guess(user_guess, st.session_state.target_number)
        st.session_state.history.append((user_guess, s, b, o))
        
        if s == st.session_state.digit_length:
            st.session_state.game_over = True
            
        # 4. 화면을 그리기 전에 알약 버튼 상태를 미리 비워줌 (에러 방지!)
        st.session_state.current_guess =[]

# -----------------------------------------------------------------------------
# 4. 화면 레이아웃 구성
# -----------------------------------------------------------------------------
st.title("⚾ 숫자 야구")

# ==========================================
# [상단 레이아웃] 1행
# ==========================================
top_left, top_right = st.columns(2)

with top_left:
    with st.popover("🎮 게임 설정 열기"):
        idx = st.session_state.digit_length - 4 
        selected_length = st.radio("몇 자리 숫자로 할까요?", (4, 5, 6), index=idx, horizontal=True)
        if st.button("🔄 새 게임 시작", type="primary", use_container_width=True):
            start_new_game(selected_length)
            st.rerun()

with top_right:
    with st.container(horizontal=True):
        st.subheader("📖 규칙 및 판정 설명")
        st.success("🟢 **S (스트라이크)** : 숫자와 **위치**가 모두 맞았을 때")
        st.warning("🟡 **B (볼)** : 숫자는 맞췄지만, **위치**가 틀렸을 때")
        st.error("🔴 **O (아웃)** : 내가 입력한 숫자가 정답에 **아예 없을 때**")

st.markdown("---")

# ==========================================
# [하단 레이아웃] 2행
# ==========================================
bot_left, bot_right = st.columns(2)

# 하단 왼쪽: 숫자 입력란 (실시간 디스플레이 + st.pills)
with bot_left:
    st.subheader("🎯 숫자 입력")
    
    if not st.session_state.game_over:
        st.info("💡 **버튼을 터치**하면 아래에 숫자가 표시됩니다.")
        
        # 1. 큼직한 실시간 숫자 디스플레이
        current_selection = st.session_state.current_guess
        if current_selection:
            display_text = " ".join(current_selection)
            st.markdown(f"<h1 style='text-align: center; color: #1E88E5; letter-spacing: 15px; font-size: 50px;'>{display_text}</h1>", unsafe_allow_html=True)
        else:
            placeholder_text = "_ " * st.session_state.digit_length
            st.markdown(f"<h1 style='text-align: center; color: #B0BEC5; letter-spacing: 15px; font-size: 50px;'>{placeholder_text}</h1>", unsafe_allow_html=True)
        
        # 2. 에러 메시지 표시 로직 (콜백 함수에서 발생한 메시지 띄우기)
        if st.session_state.error_msg:
            st.error(st.session_state.error_msg)
            # 한 번 보여준 에러 메시지는 다음 행동 시 지워지도록 초기화
            st.session_state.error_msg = ""
        
        # 3. 터치형 알약 버튼
        st.pills(
            f"👇 {st.session_state.digit_length}개의 숫자를 선택하세요:",
            options=[str(i) for i in range(10)],
            selection_mode="multi",
            key="current_guess"
        )
        
        # 4. 입력 완료 버튼 (⭐⭐⭐ on_click 옵션 추가 ⭐⭐⭐)
        st.button(
            "확인 (입력 완료)", 
            type="primary", 
            use_container_width=True, 
            on_click=handle_submit # 이 버튼을 누르면 위에서 정의한 handle_submit 함수가 먼저 실행됩니다!
        )
            
    else:
        st.success("🎉 정답을 맞췄습니다! 게임이 종료되었습니다.")
        st.info("다시 하려면 상단의 **'게임 설정 열기'** 버튼을 눌러 새 게임을 시작하세요.")

# 하단 오른쪽: 입력 결과(히스토리) 정리
with bot_right:
    st.subheader("📝 입력 결과 기록")
    
    if st.session_state.game_over:
        st.balloons()
        st.success(f"🎊 {len(st.session_state.history)}번 만에 정답 `{st.session_state.target_number}`을(를) 맞추셨습니다!")
    
    if not st.session_state.history:
        st.info("아직 입력한 기록이 없습니다. 왼쪽에서 숫자를 선택해 보세요!")
    else:
        for idx, (guess, s, b, o) in enumerate(reversed(st.session_state.history)):
            attempt_num = len(st.session_state.history) - idx
            
            result_text = f"**{attempt_num}번째** ➡️ `{guess}` : "
            if s > 0: result_text += f"🟢 **{s}S** "
            if b > 0: result_text += f"🟡 **{b}B** "
            if o > 0: result_text += f"🔴 **{o}O**"
            
            st.markdown(result_text)