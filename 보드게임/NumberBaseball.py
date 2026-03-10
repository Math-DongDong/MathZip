import streamlit as st
import random

# -----------------------------------------------------------------------------
# 1. 페이지 기본 설정
# -----------------------------------------------------------------------------
st.set_page_config(page_title="숫자 야구 게임", page_icon="⚾", layout="wide")

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
# 알약(pills) 상태를 실시간으로 관리하기 위한 세션 상태 추가
if 'current_guess' not in st.session_state:
    st.session_state.current_guess =[]

def start_new_game(length):
    st.session_state.target_number = generate_target_number(length)
    st.session_state.history =[]
    st.session_state.game_over = False
    st.session_state.digit_length = length
    st.session_state.current_guess =[] # 새 게임 시 입력칸도 초기화

if st.session_state.target_number is None:
    start_new_game(st.session_state.digit_length)

# -----------------------------------------------------------------------------
# 4. 화면 레이아웃 구성
# -----------------------------------------------------------------------------
st.title("⚾ 두근두근 숫자 야구 게임")
st.markdown("---")

# ==========================================
# [상단 레이아웃] 1행
# ==========================================
top_left, top_right = st.columns(2)

with top_left:
    st.subheader("⚙️ 게임 준비")
    st.write(f"현재 **{st.session_state.digit_length}자리 숫자** 모드입니다.")
    
    with st.popover("🎮 게임 설정 열기"):
        st.markdown("**1. 자릿수 선택**")
        idx = st.session_state.digit_length - 4 
        selected_length = st.radio("몇 자리 숫자로 할까요?", (4, 5, 6), index=idx, horizontal=True)
        
        st.markdown("**2. 게임 시작**")
        if st.button("🔄 새 게임 시작", type="primary", use_container_width=True):
            start_new_game(selected_length)
            st.rerun()

with top_right:
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
        
        # 1. 큼직한 실시간 숫자 디스플레이 (전광판 느낌)
        # 선택된 숫자가 있으면 간격을 띄워 예쁘게 보여주고, 없으면 빈칸( _ )으로 표시합니다.
        current_selection = st.session_state.current_guess
        if current_selection:
            display_text = " ".join(current_selection)
            # HTML과 CSS를 활용해 크고 파란색의 텍스트로 렌더링합니다.
            st.markdown(f"<h1 style='text-align: center; color: #1E88E5; letter-spacing: 15px; font-size: 50px;'>{display_text}</h1>", unsafe_allow_html=True)
        else:
            placeholder_text = "_ " * st.session_state.digit_length
            st.markdown(f"<h1 style='text-align: center; color: #B0BEC5; letter-spacing: 15px; font-size: 50px;'>{placeholder_text}</h1>", unsafe_allow_html=True)
        
        # 2. 터치형 알약 버튼 (st.form 제거)
        # key="current_guess"를 부여하여, 클릭할 때마다 위 디스플레이가 즉시 반응합니다.
        st.pills(
            f"👇 {st.session_state.digit_length}개의 숫자를 선택하세요:",
            options=[str(i) for i in range(10)],
            selection_mode="multi",
            key="current_guess" # 세션 상태와 직접 연결!
        )
        
        # 3. 입력 완료 버튼
        if st.button("확인 (입력 완료)", type="primary", use_container_width=True):
            user_guess = "".join(st.session_state.current_guess)
            
            if len(user_guess) != st.session_state.digit_length:
                st.error(f"⚠️ {st.session_state.digit_length}개의 숫자를 모두 선택해 주세요!")
            else:
                s, b, o = check_guess(user_guess, st.session_state.target_number)
                st.session_state.history.append((user_guess, s, b, o))
                
                # 입력을 완료했으므로 알약 버튼(화면)을 다시 비워줍니다.
                st.session_state.current_guess =[] 
                
                if s == st.session_state.digit_length:
                    st.session_state.game_over = True
                
                st.rerun() # 변경된 상태(기록 추가, 버튼 리셋)를 반영하기 위해 새로고침
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