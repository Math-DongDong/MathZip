import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math

col1, col2 = st.columns([4,  1])
with col1:
    st.title("⚖️ 균형을 잡아라")

# 도형 무게 설정
WEIGHTS = {'tri': 5, 'sq': 3, 'cir': 2}
SHAPES = {
    'tri': {'marker': '^', 'color': '#1f77b4', 'name': '삼각형', 'size': 800},
    'sq':  {'marker': 's', 'color': '#10b981', 'name': '사각형', 'size': 600},
    'cir': {'marker': 'o', 'color': '#8b5cf6', 'name': '원',     'size': 600}
}

# -----------------------------------------------------------------------------
# 2. 세션 상태 (Session State) 초기화 (누른 순서 기억)
# -----------------------------------------------------------------------------
if 'left_pan' not in st.session_state:
    st.session_state.left_pan =[]  
if 'right_pan' not in st.session_state:
    st.session_state.right_pan =[]

def modify_shape(side, shape, amount):
    """도형을 추가하거나 빼는 함수 (순서 유지)"""
    if amount > 0:
        st.session_state[side].append(shape)
    elif amount < 0:
        pan_list = st.session_state[side]
        for i in range(len(pan_list) - 1, -1, -1):
            if pan_list[i] == shape:
                pan_list.pop(i)
                break

def reset_scale():
    """저울 초기화"""
    st.session_state.left_pan =[]
    st.session_state.right_pan =[]

# -----------------------------------------------------------------------------
# 3. 무게 계산 로직
# -----------------------------------------------------------------------------
def get_weight(side_list):
    return sum(WEIGHTS[shape] for shape in side_list)

left_weight = get_weight(st.session_state.left_pan)
right_weight = get_weight(st.session_state.right_pan)

# -----------------------------------------------------------------------------
# 4. 화면 레이아웃 구성
# -----------------------------------------------------------------------------
col_left, col_mid, col_right = st.columns([1, 2.5, 1])

# --- 좌측 패널 (왼쪽 저울 조작) ---
with col_left:
    st.write("🔺 삼각형 (무게 5)")
    c1, c2 = st.columns(2)
    c1.button("➕ 추가", key="l_add_tri", on_click=modify_shape, args=('left_pan', 'tri', 1), use_container_width=True)
    c2.button("➖ 빼기", key="l_sub_tri", on_click=modify_shape, args=('left_pan', 'tri', -1), use_container_width=True)
    
    st.write("🟩 사각형 (무게 3)")
    c1, c2 = st.columns(2)
    c1.button("➕ 추가", key="l_add_sq", on_click=modify_shape, args=('left_pan', 'sq', 1), use_container_width=True)
    c2.button("➖ 빼기", key="l_sub_sq", on_click=modify_shape, args=('left_pan', 'sq', -1), use_container_width=True)
    
    st.write("🟣 원 (무게 2)")
    c1, c2 = st.columns(2)
    c1.button("➕ 추가", key="l_add_cir", on_click=modify_shape, args=('left_pan', 'cir', 1), use_container_width=True)
    c2.button("➖ 빼기", key="l_sub_cir", on_click=modify_shape, args=('left_pan', 'cir', -1), use_container_width=True)

# --- 우측 패널 (오른쪽 저울 조작) ---
with col_right:
    st.write("🔺 삼각형 (무게 5)")
    c1, c2 = st.columns(2)
    c1.button("➕ 추가", key="r_add_tri", on_click=modify_shape, args=('right_pan', 'tri', 1), use_container_width=True)
    c2.button("➖ 빼기", key="r_sub_tri", on_click=modify_shape, args=('right_pan', 'tri', -1), use_container_width=True)
    
    st.write("🟩 사각형 (무게 3)")
    c1, c2 = st.columns(2)
    c1.button("➕ 추가", key="r_add_sq", on_click=modify_shape, args=('right_pan', 'sq', 1), use_container_width=True)
    c2.button("➖ 빼기", key="r_sub_sq", on_click=modify_shape, args=('right_pan', 'sq', -1), use_container_width=True)
    
    st.write("🟣 원 (무게 2)")
    c1, c2 = st.columns(2)
    c1.button("➕ 추가", key="r_add_cir", on_click=modify_shape, args=('right_pan', 'cir', 1), use_container_width=True)
    c2.button("➖ 빼기", key="r_sub_cir", on_click=modify_shape, args=('right_pan', 'cir', -1), use_container_width=True)

# --- 중앙 패널 (저울 시각화) ---
with col_mid:
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # 1. 각도 계산
    diff = left_weight - right_weight
    angle_deg = np.clip(diff * 2, -20, 20) 
    angle_rad = math.radians(angle_deg)

    # 2. 🌟 평행 상태(무게가 같을 때) 색상 지정 로직
    # 양변의 무게가 같으면 파란색(#3b82f6), 다르면 검정색('black')으로 변합니다!
    if left_weight == right_weight:
        beam_color = '#3b82f6'
    else:
        beam_color = 'black'

    # 3. 저울의 뼈대 좌표 계산
    pivot_x, pivot_y = 0, 5
    arm_length = 5
    
    left_x = pivot_x - arm_length * math.cos(angle_rad)
    left_y = pivot_y - arm_length * math.sin(angle_rad)
    
    right_x = pivot_x + arm_length * math.cos(angle_rad)
    right_y = pivot_y + arm_length * math.sin(angle_rad)

    # 위에서 떨어지는 지지대 선 (색상 적용)
    ax.plot([0, 0],[5, 12], color=beam_color, lw=4, zorder=1) 
    
    # 양팔 막대기 (색상 적용)
    ax.plot([left_x, right_x], [left_y, right_y], color=beam_color, lw=6, zorder=2)
    
    # 중심 핀, 양끝 핀 (색상 적용)
    ax.scatter([pivot_x, left_x, right_x],[pivot_y, left_y, right_y], color=beam_color, s=100, zorder=3)

    # 4. 누른 순서대로 매달리는 접시(도형) 그리는 함수
    def draw_pan(start_x, start_y, pan_list):
        if not pan_list:
            ax.plot([start_x, start_x],[start_y, start_y - 1.5], color='gray', lw=3, zorder=1)
            return

        bottom_y = start_y - 1.5 - (len(pan_list) - 1) * 1.5
        ax.plot([start_x, start_x], [start_y, bottom_y], color='gray', lw=3, zorder=1)

        current_y = start_y - 1.5
        for shape in pan_list:
            props = SHAPES[shape]
            ax.scatter(start_x, current_y, marker=props['marker'], color=props['color'], s=props['size'], zorder=4, edgecolors='black')
            current_y -= 1.5

    # 양쪽 모빌 그리기
    draw_pan(left_x, left_y, st.session_state.left_pan)
    draw_pan(right_x, right_y, st.session_state.right_pan)

    # 축 설정
    ax.set_xlim(-8, 8)
    ax.set_ylim(-20, 12)
    ax.axis('off')

    st.pyplot(fig)
    
with col2:
    col2.space("medium")
    if st.button("🔄 초기화", use_container_width=True):
        reset_scale()
        st.rerun()