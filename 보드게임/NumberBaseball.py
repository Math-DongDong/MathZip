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
    """선택한 자릿수(length)에 맞춰 중복 없는 랜덤 숫자를 생성합니다."""
    digits = list("0123456789")
    first_digit = random.choice(list("123456789")) # 첫 자리는 0 제외
    digits.remove(first_digit)
    rest_digits = random.sample(digits, length - 1)
    return first_digit + "".join(rest_digits)

def check_guess(guess, target):
    """사용자 입력과 정답을 비교하여 S, B, O를 계산합니다."""
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

def start_new_game(length):
    """새로운 게임을 시작할 때 변수들을 초기화하는 함수입니다."""
    st.session_state.target_number = generate_target_number(length)
    st.session_state.history =[]
    st.session_state.game_over = False
    st.session_state.digit_length = length

# 처음 접속 시 게임 세팅
if st.session_state.target_number is None:
    start_new_game(st.session_state.digit_length)

# -----------------------------------------------------------------------------
# 4. 화면 레이아웃 구성
# -----------------------------------------------------------------------------
st.title("⚾ 두근두근 숫자 야구 게임")
st.markdown("---")

# ==========================================
#[상단 레이아웃] 1행: 2개의 열 (게임 설정 / 규칙 설명)
# ==========================================
top_left, top_right = st.columns(2)

# 상단 왼쪽: 팝오버(popover)를 활용한 게임 설정
with top_left:
    st.subheader("⚙️ 게임 준비")
    st.write(f"현재 **{st.session_state.digit_length}자리 숫자** 모드입니다.")
    
    # st.popover를 사용하면 클릭 시 확장되는 메뉴를 만들 수 있습니다.
    with st.popover("🎮 게임 설정 열기"):
        st.markdown("**1. 자릿수 선택**")
        # 현재 설정된 자릿수를 기본값(index)으로 설정
        idx = st.session_state.digit_length - 4 
        selected_length = st.radio(
            "몇 자리 숫자로 게임을 할까요?", 
            (4, 5, 6), 
            index=idx, 
            horizontal=True
        )
        
        st.markdown("**2. 게임 시작**")
        if st.button("🔄 새 게임 시작", type="primary", use_container_width=True):
            start_new_game(selected_length)
            st.rerun() # 설정 적용 후 화면 새로고침

# 상단 오른쪽: 판정 기호 설명
with top_right:
    st.subheader("📖 규칙 및 판정 설명")
    st.success("🟢 **S (스트라이크)** : 숫자와 **위치**가 모두 맞았을 때")
    st.warning("🟡 **B (볼)** : 숫자는 맞췄지만, **위치**가 틀렸을 때")
    st.error("🔴 **O (아웃)** : 내가 입력한 숫자가 정답에 **아예 없을 때**")

st.markdown("---")

# ==========================================
# [하단 레이아웃] 2행: 2개의 열 (숫자 입력란 / 입력 결과 정리)
# ==========================================
bot_left, bot_right = st.columns(2)

# 하단 왼쪽: 숫자 입력란
with bot_left:
    st.subheader("🎯 숫자 입력")
    
    # 정답을 맞추지 않았을 때만 입력 폼 표시
    if not st.session_state.game_over:
        with st.form("guess_form", clear_on_submit=True):
            user_guess = st.text_input(
                f"{st.session_state.digit_length}자리 숫자를 중복 없이 입력하세요:",
                max_chars=st.session_state.digit_length
            )
            submitted = st.form_submit_button("확인 (또는 엔터)")

        # 입력값 검증 로직
        if submitted:
            if len(user_guess) != st.session_state.digit_length:
                st.error(f"⚠️ {st.session_state.digit_length}자리 숫자를 모두 채워주세요!")
            elif not user_guess.isdigit():
                st.error("⚠️ 숫자만 입력해 주세요!")
            elif len(set(user_guess)) != st.session_state.digit_length:
                st.error("⚠️ 중복되는 숫자가 있습니다. 서로 다른 숫자를 입력해 주세요!")
            else:
                # 판정 후 기록 저장
                s, b, o = check_guess(user_guess, st.session_state.target_number)
                st.session_state.history.append((user_guess, s, b, o))
                
                # 정답 처리
                if s == st.session_state.digit_length:
                    st.session_state.game_over = True
                    st.rerun() # 결과를 오른쪽에 띄우기 위해 리런
    else:
        # 정답을 맞춘 후의 화면
        st.success("🎉 정답을 맞췄습니다! 게임이 종료되었습니다.")
        st.info("다시 하려면 상단의 **'게임 설정 열기'** 버튼을 눌러 새 게임을 시작하세요.")

# 하단 오른쪽: 입력 결과(히스토리) 정리
with bot_right:
    st.subheader("📝 입력 결과 기록")
    
    # 게임 종료 시 축하 메시지와 풍선 효과
    if st.session_state.game_over:
        st.balloons()
        st.success(f"🎊 {len(st.session_state.history)}번 만에 정답 `{st.session_state.target_number}`을(를) 맞추셨습니다!")
    
    # 기록이 없을 때 빈 화면 방지 안내문
    if not st.session_state.history:
        st.info("아직 입력한 기록이 없습니다. 왼쪽에서 숫자를 입력해 보세요!")
    else:
        # 최근 입력한 것이 제일 위로 오도록 reversed 사용
        for idx, (guess, s, b, o) in enumerate(reversed(st.session_state.history)):
            attempt_num = len(st.session_state.history) - idx
            
            # S, B, O 여부에 따라 색상을 입혀서 가독성 향상
            result_text = f"**{attempt_num}번째** ➡️ `{guess}` : "
            if s > 0: result_text += f"🟢 **{s}S** "
            if b > 0: result_text += f"🟡 **{b}B** "
            if o > 0: result_text += f"🔴 **{o}O**"
            
            st.markdown(result_text)