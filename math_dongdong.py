# app.py

import streamlit as st
import random
import time

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="두 개의 주사위",
    page_icon="🎲",
    layout="wide"
)
st.title("🎲주사위 놀이")
# --- 구분선 ---
st.divider()

# --- 상태 초기화 (State Initialization) ---
if 'sign_dice' not in st.session_state:
    st.session_state.sign_dice = '❔'
if 'number_dice' not in st.session_state:
    st.session_state.number_dice = 0

# --- 상단 영역: 부호 주사위 (+, -) ---
st.write("## ➕부호 주사위➖")

if st.button("던지기", key="sign_button"):
    placeholder = st.empty()
    
    # *** 여기가 핵심 변경점 1: 애니메이션 지연 시간 설정 ***
    start_delay = 0.05  # 애니메이션 시작 시의 프레임 간격 (빠름)
    end_delay = 0.4     # 애니메이션 끝날 때의 프레임 간격 (느림)
    total_steps = 20    # 총 애니메이션 스텝 수 (값을 조절해 전체 시간 변경 가능)
    
    signs = ['➕', '➖']
    
    for i in range(total_steps):
        temp_result = random.choice(signs)
        with placeholder.container():
            st.markdown(f"<p style='text-align: center; font-size: 80px;'>{temp_result}</p>", unsafe_allow_html=True)
        
        # *** 여기가 핵심 변경점 2: 진행도에 따라 지연 시간을 점차 늘림 ***
        # 현재 진행도 계산 (0.0에서 1.0 사이의 값)
        progress = i / total_steps
        # 현재 지연 시간 계산 (선형적으로 증가)
        current_delay = start_delay + (progress * (end_delay - start_delay))
        
        # 마지막 프레임이 아니면 계산된 지연 시간만큼 멈춤
        if i < total_steps - 1:
            time.sleep(current_delay)

    final_result = random.choice(signs)
    with placeholder.container():
        st.markdown(f"<p style='text-align: center; font-size: 80px;'>{final_result}</p>", unsafe_allow_html=True)
    st.session_state.sign_dice = final_result

else:
    st.markdown(f"<p style='text-align: center; font-size: 80px;'>{st.session_state.sign_dice}</p>", unsafe_allow_html=True)

# --- 구분선 ---
st.divider()

# --- 하단 영역: 숫자 주사위 (1-6) ---
st.write("## 🔢숫자 주사위🎲")

if st.button("던지기", key="number_button"):
    placeholder = st.empty()

    # 숫자 주사위에도 동일한 감속 로직 적용
    start_delay = 0.05
    end_delay = 0.4
    total_steps = 20
    
    for i in range(total_steps):
        temp_result = random.randint(1, 6)
        with placeholder.container():
            st.markdown(f"<p style='text-align: center; font-size: 100px;'>{temp_result}</p>", unsafe_allow_html=True)
        
        progress = i / total_steps
        current_delay = start_delay + (progress * (end_delay - start_delay))
        
        if i < total_steps - 1:
            time.sleep(current_delay)
            
    final_result = random.randint(1, 6)
    with placeholder.container():
        st.markdown(f"<p style='text-align: center; font-size: 100px;'>{final_result}</p>", unsafe_allow_html=True)
    st.session_state.number_dice = final_result

else:
    st.markdown(f"<p style='text-align: center; font-size: 100px;'>{st.session_state.number_dice}</p>", unsafe_allow_html=True)