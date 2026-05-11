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
if 'game_lost' not in st.session_state:
    st.session_state.game_lost = False
if 'digit_length' not in st.session_state:
    st.session_state.digit_length = 4
if 'current_guess' not in st.session_state:
    st.session_state.current_guess =[]
if 'error_msg' not in st.session_state:
    st.session_state.error_msg = "" # 경고 메시지를 담을 공간 추가
if 'lives' not in st.session_state:
    st.session_state.lives = 5
if 'initial_lives' not in st.session_state:
    st.session_state.initial_lives = 5

def start_new_game(length=None, lives=None):
    if length is None:
        length = st.session_state.digit_length
    if lives is None:
        lives = st.session_state.initial_lives
    st.session_state.target_number = generate_target_number(length)
    st.session_state.history =[]
    st.session_state.game_over = False
    st.session_state.game_lost = False
    st.session_state.digit_length = length
    st.session_state.current_guess =[]
    st.session_state.error_msg = ""
    st.session_state.lives = lives
    st.session_state.initial_lives = lives

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
        
        # 목숨 감소 로직: 정답이 아니면 목숨 1개 감소
        if s != st.session_state.digit_length:
            st.session_state.lives -= 1
            if st.session_state.lives <= 0:
                st.session_state.game_lost = True
        else:
            # 정답을 맞춘 경우
            st.session_state.game_over = True
            
        # 4. 화면을 그리기 전에 알약 버튼 상태를 미리 비워줌 (에러 방지!)
        st.session_state.current_guess =[]

# -----------------------------------------------------------------------------
# 4. 화면 레이아웃 구성
# -----------------------------------------------------------------------------
st.title("⚾ 숫자 야구")

# 게임 진행 중 또는 게임 오버/패배 상태에 따라 다른 레이아웃 표시
if st.session_state.game_over or st.session_state.game_lost:
    # ==========================================
    # [게임 종료 화면] - 별개의 전체 레이아웃
    # ==========================================
    if st.session_state.game_over:
        st.success("🎉 정답을 맞췄습니다!")
        result_type = "승리"
        result_color = "green"
    else:  # game_lost
        st.error("😢 모든 목숨을 소진했습니다...")
        result_type = "패배"
        result_color = "red"
    
    # 중앙 정렬된 결과 표시
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"<h2 style='text-align: center; color: {result_color};'>게임 {result_type}</h2>", unsafe_allow_html=True)
    
    st.divider()
    
    # 게임 정보 표시 (2개 열)
    info_col1, info_col2 = st.columns(2)
    
    with info_col1:
        st.markdown("### 📊 게임 정보")
        st.metric("자릿수", f"{st.session_state.digit_length}자리")
        st.metric("초기 목숨", f"{st.session_state.initial_lives}개")
        if st.session_state.game_lost:
            st.metric("남은 목숨", "0개", delta="-1", delta_color="inverse")
        else:
            st.metric("남은 목숨", f"{st.session_state.lives}개")
    
    with info_col2:
        st.markdown("### 🎯 결과")
        st.metric("시도 횟수", f"{len(st.session_state.history)}번")
        st.metric("정답", f"{st.session_state.target_number}")
        if st.session_state.game_over:
            st.metric("성공률", f"{len(st.session_state.history)} 시도", delta="성공")
        else:
            st.metric("패배 원인", "목숨 소진")
    
    st.divider()
    
    # 시도 기록
    st.markdown("### 📝 입력 기록")
    if st.session_state.history:
        col_left, col_right = st.columns(2)
        
        for idx, (guess, s, b, o) in enumerate(reversed(st.session_state.history)):
            attempt_num = len(st.session_state.history) - idx
            
            result_text = f"**`{attempt_num}번째`**  {guess} : "
            if s > 0: result_text += f"🟢 **{s}S** "
            if b > 0: result_text += f"🟡 **{b}B** "
            if o > 0: result_text += f"🔴 **{o}O**"
            
            if attempt_num <= 10:
                col_left.markdown(f"#### {result_text}")
            else:
                col_right.markdown(f"#### {result_text}")
    else:
        st.caption("기록이 없습니다.")
    
    st.divider()
    
    # 새 게임 시작 버튼
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 새 게임 시작", type="primary", use_container_width=True):
            st.session_state.digit_length = 4
            st.session_state.initial_lives = 5
            start_new_game(4, 5)
            st.rerun()

else:
    # ==========================================
    # [게임 진행 화면] - 기본 레이아웃
    # ==========================================
    
    # ==========================================
    # [상단 레이아웃] 1행
    # ==========================================
    with st.container(horizontal=True):
        st.success("🟢 **S** : 숫자와 **위치**가 모두 맞았을 때")
        st.warning("🟡 **B** : 숫자는 맞췄지만, **위치**가 틀렸을 때")
        st.error("🔴 **O** : 내가 입력한 숫자가 정답에 **아예 없을 때**")
    
    # ==========================================
    # [하단 레이아웃] 2행
    # ==========================================
    bot_left, bot_right = st.columns([0.3,0.7])
    
    # 하단 왼쪽: 숫자 입력란 (실시간 디스플레이 + st.pills)
    with bot_left:
        st.subheader(f"🎯 {st.session_state.digit_length}자리 숫자 입력")
        
        # 목숨 표시
        lives_display = "❤️ " * st.session_state.lives + "🖤 " * (st.session_state.initial_lives - st.session_state.lives)
        st.markdown(f"<h3 style='text-align: center;'>{lives_display}</h3>", unsafe_allow_html=True)
        st.caption(f"남은 목숨: {st.session_state.lives}/{st.session_state.initial_lives}")

        with st.popover("🎮 게임 설정 열기"):
            idx = st.session_state.digit_length - 4 
            selected_length = st.radio("몇 자리 숫자로 할까요?", (4, 5, 6), index=idx, horizontal=True)
            selected_lives = st.slider("초기 목숨 개수", min_value=3, max_value=10, value=st.session_state.initial_lives)
            if st.button("🔄 새 게임 시작", type="primary", use_container_width=True):
                start_new_game(selected_length, selected_lives)
                st.rerun()
    
        # 1. 큼직한 실시간 숫자 디스플레이
        current_selection = st.session_state.current_guess
        if current_selection:
            display_text = " ".join(current_selection)
            st.markdown(f"<h1 style='text-align: center; color: #1E88E5; letter-spacing: 15px; font-size: 50px;'>{display_text}</h1>", unsafe_allow_html=True)
        else:
            placeholder_text = "_ " * st.session_state.digit_length
            st.markdown(f"<h1 style='text-align: center; color: #B0BEC5; letter-spacing: 15px; font-size: 50px;'>{placeholder_text}</h1>", unsafe_allow_html=True)
        
        # 2. 에러 메시지 표시 로직
        if st.session_state.error_msg:
            st.error(st.session_state.error_msg)
            st.session_state.error_msg = ""
        
        # 3. 터치형 알약 버튼
        st.pills(
            f"👇 {st.session_state.digit_length}개의 숫자를 선택하세요:",
            options=[str(i) for i in range(10)],
            selection_mode="multi",
            key="current_guess"
        )
        
        # 4. 입력 완료 버튼
        st.button(
            "확인 (입력 완료)", 
            type="primary", 
            use_container_width=True, 
            on_click=handle_submit
        )
    
    # 하단 오른쪽: 입력 결과(히스토리) 정리
    with bot_right:
        st.subheader("📝 입력 결과 기록")
        
        if not st.session_state.history:
            st.caption("아직 입력한 기록이 없습니다.")
        else:
            col_left, col_right = st.columns(2)
            
            for idx, (guess, s, b, o) in enumerate(reversed(st.session_state.history)):
                attempt_num = len(st.session_state.history) - idx
                
                result_text = f"**`{attempt_num}번째`**  {guess} : "
                if s > 0: result_text += f"🟢 **{s}S** "
                if b > 0: result_text += f"🟡 **{b}B** "
                if o > 0: result_text += f"🔴 **{o}O**"
                
                if attempt_num <= 10:
                    col_left.markdown(f"#### {result_text}")
                else:
                    col_right.markdown(f"#### {result_text}")
