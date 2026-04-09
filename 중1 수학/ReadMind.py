import streamlit as st
import random

st.title("🔮 생각을 읽는 마법구슬")

# -----------------------------------------------------------------------------
# 1. 페이지 기본 설정
# -----------------------------------------------------------------------------
EMOJIS =['🍎', '🐶', '🚗', '🎈', '⭐', '🍀', '🌈', '🔥', '💧', '☀️', 
          '🌙', '⛄', '☂️',  '🍕', '🎸', '💎', '🚀', '🐢']

# -----------------------------------------------------------------------------
# 2. 세션 상태 및 초기화/진행 함수 정의
# -----------------------------------------------------------------------------
def init_game():
    target = random.choice(EMOJIS)
    
    mapping = {}
    for i in range(100):
        if i % 9 == 0:
            mapping[i] = target
        else:
            mapping[i] = random.choice(EMOJIS)
            
    st.session_state.mapping = mapping
    st.session_state.target_emoji = target
    st.session_state.revealed = False
    st.session_state.step = 1

def next_step():
    if st.session_state.step < 4:
        st.session_state.step += 1

def reveal_answer():
    st.session_state.revealed = True

if 'mapping' not in st.session_state:
    init_game()

# -----------------------------------------------------------------------------
# 3. 화면 레이아웃 구성
# -----------------------------------------------------------------------------
col_left, col_right = st.columns([1, 2.2])

# ==========================================
#[왼쪽 열] 조작 버튼 ➡️ 단계별 안내 ➡️ 결과 이모지
# ==========================================
with col_left:
    # 1. 상단 버튼 영역
    btn1, btn2 = st.columns(2)
    with btn1:
        st.button("🔄 새로하기", width='stretch', on_click=init_game)
    with btn2:
        if st.session_state.step < 4:
            st.button("➡️ 다음 단계", width='stretch', on_click=next_step)
        else:
            st.button("✨ 정답은?", width='stretch', on_click=reveal_answer, type="primary")
            
    
    # 2. ⬅️ [수정됨] 단계별 안내 문구 (버튼 바로 아래 위치 & 하나씩만 등장)
    step = st.session_state.step
    if step == 1:
        st.success("① 1부터 99 사이의 숫자 중 하나를 생각한다.")
    elif step == 2:
        st.info("② 생각한 숫자의 각 자리수 숫자를 더한다. (예: 34라면 3+4=7)")
    elif step == 3:
        st.warning("③ 처음 생각한 숫자에서 ②의 결과를 뺀다. (예: 34-7=27)")
    elif step == 4:
        st.error("④ 오른쪽 표에서 ③의 결과에 해당하는 기호를 찾는다!")
    
    # 3. 결과 이모지 화면 (가장 하단으로 이동)
    display_char = st.session_state.target_emoji if st.session_state.revealed else "❓"
    st.markdown(f"<h1 style='text-align: center; font-size: 200px; margin: 0;'>{display_char}</h1>", unsafe_allow_html=True)

# ==========================================
#[오른쪽 열] 10x10 그리드 표 (칼각 정렬 적용)
# ==========================================
with col_right:
    for row_idx in range(10):
        cols = st.columns(10)
        
        for col_idx in range(10):
            num = row_idx * 10 + col_idx
            emoji = st.session_state.mapping[num]
            tile = cols[col_idx].container(border=False)
            
            tile.markdown(
                f"<div style='display: flex; align-items: center; justify-content: center; font-size: 24px; padding-top: 10px;'>"
                f"<span style='font-size: 16px; color: #555; width: 24px; text-align: right; margin-right: 12px;'>{num}</span>"
                f"<span>{emoji}</span>"
                f"</div>", 
                unsafe_allow_html=True
            )