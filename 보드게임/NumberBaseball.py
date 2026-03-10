import streamlit as st
import random

# -----------------------------------------------------------------------------
# 1. 페이지 기본 설정
# -----------------------------------------------------------------------------
# 웹 페이지의 탭 이름과 레이아웃(넓게 쓰기)을 설정합니다.
st.set_page_config(page_title="숫자 야구 게임", page_icon="⚾", layout="wide")

# -----------------------------------------------------------------------------
# 2. 게임 로직 함수 정의
# -----------------------------------------------------------------------------
def generate_target_number(length):
    """
    선택한 자릿수(length)에 맞춰 중복 없는 랜덤 숫자를 생성하는 함수입니다.
    맨 앞자리에 0이 오지 않도록 처리합니다.
    """
    digits = list("0123456789")
    # 첫 번째 자리는 1~9 중에서 선택
    first_digit = random.choice(list("123456789"))
    digits.remove(first_digit)
    
    # 나머지 자리는 남은 숫자 중에서 중복 없이 선택
    rest_digits = random.sample(digits, length - 1)
    return first_digit + "".join(rest_digits)

def check_guess(guess, target):
    """
    사용자의 입력값(guess)과 정답(target)을 비교하여 스트라이크, 볼, 아웃을 계산합니다.
    """
    strikes = 0
    balls = 0
    
    for i in range(len(guess)):
        if guess[i] == target[i]:
            strikes += 1  # 숫자와 위치가 모두 맞으면 스트라이크
        elif guess[i] in target:
            balls += 1    # 숫자는 있지만 위치가 다르면 볼
            
    # 아웃(O)은 정답에 아예 포함되지 않은 숫자의 개수입니다.
    outs = len(target) - strikes - balls 
    return strikes, balls, outs

# -----------------------------------------------------------------------------
# 3. 세션 상태(Session State) 초기화
# -----------------------------------------------------------------------------
# 스트림릿은 화면이 새로고침 될 때마다 변수가 초기화되므로, 게임 데이터를 유지하기 위해 session_state를 사용합니다.

if 'target_number' not in st.session_state:
    st.session_state.target_number = None  # 맞춰야 할 정답 숫자
if 'history' not in st.session_state:
    st.session_state.history =[]          # 사용자가 입력한 기록들
if 'game_over' not in st.session_state:
    st.session_state.game_over = False     # 게임 종료 여부
if 'digit_length' not in st.session_state:
    st.session_state.digit_length = 4      # 기본은 4자리 게임

# 새 게임을 시작하는 함수
def start_new_game(length):
    st.session_state.target_number = generate_target_number(length)
    st.session_state.history =[]
    st.session_state.game_over = False
    st.session_state.digit_length = length

# 처음 실행 시 새 게임 시작
if st.session_state.target_number is None:
    start_new_game(st.session_state.digit_length)

# -----------------------------------------------------------------------------
# 4. 화면 레이아웃 구성 (2개의 열)
# -----------------------------------------------------------------------------
st.title("⚾ 두근두근 숫자 야구 게임")
st.markdown("---")

# 왼쪽(게임 화면)과 오른쪽(설명 화면)을 1.2 : 1 비율로 나눕니다.
col_left, col_right = st.columns([1.2, 1])

# ==========================================
# [오른쪽 열] 게임 플레이 방법 및 S, B, O 설명
# ==========================================
with col_right:
    st.subheader("📖 게임 방법 및 규칙")
    st.info("""
    **숫자 야구 게임**은 컴퓨터가 숨긴 숫자를 맞추는 추리 게임이에요!
    중복되지 않는 숫자를 맞혀야 합니다. (예: 1234 가능, 1123 불가능)
    """)
    
    st.markdown("### 🔍 판정 기호 설명")
    st.success("🟢 **S (스트라이크)**\n\n숫자와 **위치**가 모두 맞았을 때! (최고예요!)")
    st.warning("🟡 **B (볼)**\n\n숫자는 맞췄지만, **위치**가 틀렸을 때! (아쉬워요, 자리를 바꿔보세요!)")
    st.error("🔴 **O (아웃)**\n\n내가 입력한 숫자가 정답에 **아예 없을 때**! (새로운 숫자를 찾아보세요!)")
    
    st.markdown("---")
    st.markdown("### 💡 예시 (정답이 `1234`일 때)")
    st.markdown("- 입력 `1567` ➡️ **1S 0B 3O** (1은 자리까지 맞았어요!)")
    st.markdown("- 입력 `4321` ➡️ **0S 4B 0O** (숫자는 다 맞았는데 자리가 다 틀렸어요!)")
    st.markdown("- 입력 `5678` ➡️ **0S 0B 4O** (맞는 숫자가 하나도 없어요, 완전 아웃!)")

# ==========================================
# [왼쪽 열] 게임 플레이 공간 (숫자 입력란)
# ==========================================
with col_left:
    st.subheader("🎮 게임을 시작해 볼까요?")
    
    # 1. 자릿수 선택 (4, 5, 6자리)
    selected_length = st.radio(
        "몇 자리 숫자 야구를 할까요?",
        (4, 5, 6),
        horizontal=True
    )
    
    # 자릿수를 변경하거나 '새 게임 시작' 버튼을 누르면 초기화
    if st.button("🔄 새 게임 시작", type="primary"):
        start_new_game(selected_length)
        st.rerun() # 화면 새로고침
        
    st.write(f"현재 **{st.session_state.digit_length}자리 숫자**를 맞추고 있습니다! (숫자 중복 없음)")

    # 2. 숫자 입력 폼
    # 폼(form)을 사용하면 엔터키를 쳤을 때 깔끔하게 입력되고, 입력창(clear_on_submit)을 비울 수 있습니다.
    with st.form("guess_form", clear_on_submit=True):
        user_guess = st.text_input(
            "숫자를 입력하세요 (엔터 또는 확인 버튼 클릭):",
            max_chars=st.session_state.digit_length
        )
        submitted = st.form_submit_button("확인")

    # 3. 입력값 검증 및 결과 확인 로직
    if submitted and not st.session_state.game_over:
        # 오류 체크: 길이, 숫자여부, 중복여부
        if len(user_guess) != st.session_state.digit_length:
            st.error(f"⚠️ {st.session_state.digit_length}자리 숫자를 입력해 주세요!")
        elif not user_guess.isdigit():
            st.error("⚠️ 숫자만 입력해 주세요!")
        elif len(set(user_guess)) != st.session_state.digit_length:
            st.error("⚠️ 중복되는 숫자가 있습니다. 서로 다른 숫자를 입력해 주세요!")
        else:
            # 정상 입력 시 스트라이크, 볼, 아웃 계산
            s, b, o = check_guess(user_guess, st.session_state.target_number)
            
            # 입력 기록 저장 (사용자 입력, 스트라이크, 볼, 아웃)
            st.session_state.history.append((user_guess, s, b, o))
            
            # 정답을 맞춘 경우
            if s == st.session_state.digit_length:
                st.session_state.game_over = True
                st.balloons() # 축하 효과 🎉
                st.success(f"🎉 정답입니다! {len(st.session_state.history)}번 만에 맞추셨어요!")
    
    # 4. 입력 기록(히스토리) 보여주기
    if st.session_state.history:
        st.markdown("### 📝 입력 기록")
        for idx, (guess, s, b, o) in enumerate(reversed(st.session_state.history)):
            attempt_num = len(st.session_state.history) - idx
            # 시각적으로 예쁘게 보여주기 위한 텍스트 구성
            st.markdown(f"**{attempt_num}번째 시도** : `{guess}` ➡️ **{s}S {b}B {o}O**")