import streamlit as st
import random

pages = {
    "기타": [
        st.Page("Dice.py", title="주사위 모음")
    ],
    "보드게임": [
        st.Page("Streams.py", title="스트림스")
    ],
}

pg = st.navigation(pages, position="top")

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="동동쌤의 수학모음",
    layout="wide"
)

# --- 페이지 기본 설정 ---
st.title("🔢스트림스 카드 뽑기")
# --- 구분선 ---
st.divider()

# --- 게임 초기화 함수 ---
# 게임 상태를 처음으로 되돌리는 로직을 함수로 묶어 재사용성을 높입니다.
def initialize_game():
    """스트림스 게임에 필요한 숫자 풀과 상태 변수들을 초기화합니다."""
    # 1. 스트림스 규칙에 맞는 숫자 타일 풀(Pool) 생성
    # 1~10: 각 1개, 11~20: 각 2개, 21~30: 각 1개
    number_pool = []
    number_pool.extend(list(range(1, 11)))  # 1부터 10까지 1개씩 추가
    number_pool.extend(list(range(11, 21))) # 11부터 20까지 1개씩 추가
    number_pool.extend(list(range(11, 21))) # 11부터 20까지 두 번째로 추가
    number_pool.extend(list(range(21, 31))) # 21부터 30까지 1개씩 추가
    
    # 생성된 숫자 풀을 무작위로 섞습니다.
    # 이렇게 하면 나중에 맨 앞에서부터 하나씩 뽑기만 하면 됩니다.
    random.shuffle(number_pool)
    
    # 2. 게임 상태를 session_state에 저장
    # st.session_state는 사용자의 행동(버튼 클릭 등)이 있어도 값을 유지시켜주는 스트림릿의 핵심 기능입니다.
    st.session_state.pool = number_pool      # 남은 숫자 풀
    st.session_state.draw_count = 0          # 뽑은 횟수
    st.session_state.current_number = "❔"    # 현재 뽑은 숫자 (처음엔 물음표)
    st.session_state.drawn_history = []      # 뽑았던 숫자들을 기록하는 리스트

# --- 메인 앱 로직 ---

# 앱이 처음 실행될 때만 게임을 초기화합니다.
if 'pool' not in st.session_state:
    initialize_game()

# --- 상단 버튼 영역 ---
# st.columns를 사용하여 화면을 좌우로 나누고 버튼을 배치합니다.
col1, col2 = st.columns(2)

# 왼쪽 컬럼: 초기화 버튼
with col1:
    # '초기화' 버튼을 누르면 initialize_game() 함수를 호출하여 모든 상태를 리셋합니다.
    if st.button("처음부터 다시하기 (초기화)", type="primary"):
        initialize_game()
        # st.rerun()은 스크립트를 즉시 재실행하여 초기화된 화면을 바로 보여줍니다.
        st.rerun() 

# 오른쪽 컬럼: 뽑기 버튼
with col2:
    # 뽑은 횟수가 20번 이상이면 버튼을 비활성화시킵니다.
    is_disabled = (st.session_state.draw_count >= 20)
    
    # '뽑기' 버튼을 누르면 숫자 하나를 뽑는 로직을 실행합니다.
    if st.button("다음 숫자 뽑기", disabled=is_disabled):
        # 남은 숫자 풀이 비어있지 않은지 확인합니다.
        if st.session_state.pool:
            # 1. 횟수 1 증가
            st.session_state.draw_count += 1
            # 2. 미리 섞어둔 풀에서 숫자 하나를 뽑아냅니다(pop).
            new_number = st.session_state.pool.pop()
            # 3. 현재 숫자를 업데이트합니다.
            st.session_state.current_number = new_number
            # 4. 뽑은 숫자 기록에 추가합니다.
            st.session_state.drawn_history.append(new_number)

# --- 결과 표시 영역 ---
st.divider() # 깔끔한 구분선

# 1. 현재 몇 번째 숫자인지 알려주는 정보
# 게임 상태에 따라 다른 메시지를 보여주어 사용자 경험을 향상시킵니다.
if st.session_state.draw_count == 0:
    st.header("버튼을 눌러 첫 번째 숫자를 뽑아주세요.")
elif st.session_state.draw_count >= 20:
    st.header("🏁 20개 숫자를 모두 뽑았습니다! 🏁")
else:
    st.header(f"🔢 {st.session_state.draw_count}번째 숫자")

# 2. 뽑은 숫자를 크고 굵게 중앙에 표시
# st.markdown과 HTML/CSS를 사용하여 스타일을 적용합니다.
st.markdown(
    f"<p style='text-align: center; font-size: 150px; font-weight: bold;'>{st.session_state.current_number}</p>", 
    unsafe_allow_html=True
)

st.divider()

# 3. (보너스) 지금까지 뽑은 숫자 목록을 보여줍니다.
st.write("지금까지 뽑은 숫자들:")
# 뽑은 숫자 리스트를 문자열로 변환하여 보기 좋게 표시합니다.
formatted_history = "  ➡️  ".join(map(str, st.session_state.drawn_history))
st.info(formatted_history or "아직 뽑은 숫자가 없습니다.")