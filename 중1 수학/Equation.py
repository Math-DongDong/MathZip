import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math

# -----------------------------------------------------------------------------
# 1. 페이지 및 기본 설정
# -----------------------------------------------------------------------------
st.title("⚖️ 균형을 잡아라")

# 도형 기본 시각화 설정 (무게는 제외)
SHAPES = {
    'tri': {'marker': '^', 'color': '#1f77b4', 'name': '삼각형', 'size': 800},
    'sq':  {'marker': 's', 'color': '#10b981', 'name': '사각형', 'size': 600},
    'cir': {'marker': 'o', 'color': '#8b5cf6', 'name': '원',     'size': 600}
}

# -----------------------------------------------------------------------------
# 2. 공통 함수 정의
# -----------------------------------------------------------------------------
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

def reset_scale(left_key, right_key):
    """특정 탭의 저울 초기화"""
    st.session_state[left_key] = []
    st.session_state[right_key] =[]

def get_weight(side_list, weight_dict):
    """주어진 무게 사전을 바탕으로 총 무게 계산"""
    return sum(weight_dict[shape] for shape in side_list)

def draw_balance_scale(left_wt, right_wt, left_list, right_list):
    """저울을 그리는 공통 함수"""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    diff = left_wt - right_wt
    angle_deg = np.clip(diff * 2, -20, 20) 
    angle_rad = math.radians(angle_deg)

    if left_wt == right_wt:
        beam_color = '#3b82f6' # 평행 시 파란색
    else:
        beam_color = 'black'

    pivot_x, pivot_y = 0, 5
    arm_length = 5
    
    left_x = pivot_x - arm_length * math.cos(angle_rad)
    left_y = pivot_y - arm_length * math.sin(angle_rad)
    
    right_x = pivot_x + arm_length * math.cos(angle_rad)
    right_y = pivot_y + arm_length * math.sin(angle_rad)

    ax.plot([0, 0],[5, 12], color=beam_color, lw=4, zorder=1) 
    ax.plot([left_x, right_x], [left_y, right_y], color=beam_color, lw=6, zorder=2)
    ax.scatter([pivot_x, left_x, right_x],[pivot_y, left_y, right_y], color=beam_color, s=100, zorder=3)

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

    draw_pan(left_x, left_y, left_list)
    draw_pan(right_x, right_y, right_list)

    ax.set_xlim(-8, 8)
    ax.set_ylim(-20, 12)
    ax.axis('off')
    st.pyplot(fig)

# -----------------------------------------------------------------------------
# 3. 탭 구성
# -----------------------------------------------------------------------------
tab1, tab2 = st.tabs(["⚖️ 균형을 잡아라", "🕵️‍♂️ 등식의 성질"])

# =============================================================================
#[TAB 1] 균형을 잡아라 (기존 코드)
# =============================================================================
with tab1:
    T1_WEIGHTS = {'tri': 5, 'sq': 3, 'cir': 2}
    
    if 't1_left' not in st.session_state: st.session_state.t1_left =[]  
    if 't1_right' not in st.session_state: st.session_state.t1_right =[]

    t1_l_wt = get_weight(st.session_state.t1_left, T1_WEIGHTS)
    t1_r_wt = get_weight(st.session_state.t1_right, T1_WEIGHTS)

    t1_col_left, t1_col_mid, t1_col_right = st.columns([1, 2.5, 1])

    with t1_col_left:
        st.subheader("왼쪽 접시")
        st.write("🔺 삼각형 (무게 5)")
        c1, c2 = st.columns(2)
        c1.button("➕ 추가", key="t1_l_add_tri", on_click=modify_shape, args=('t1_left', 'tri', 1), use_container_width=True)
        c2.button("➖ 빼기", key="t1_l_sub_tri", on_click=modify_shape, args=('t1_left', 'tri', -1), use_container_width=True)
        
        st.write("🟩 사각형 (무게 3)")
        c1, c2 = st.columns(2)
        c1.button("➕ 추가", key="t1_l_add_sq", on_click=modify_shape, args=('t1_left', 'sq', 1), use_container_width=True)
        c2.button("➖ 빼기", key="t1_l_sub_sq", on_click=modify_shape, args=('t1_left', 'sq', -1), use_container_width=True)
        
        st.write("🟣 원 (무게 2)")
        c1, c2 = st.columns(2)
        c1.button("➕ 추가", key="t1_l_add_cir", on_click=modify_shape, args=('t1_left', 'cir', 1), use_container_width=True)
        c2.button("➖ 빼기", key="t1_l_sub_cir", on_click=modify_shape, args=('t1_left', 'cir', -1), use_container_width=True)

    with t1_col_right:
        st.subheader("오른쪽 접시")
        st.write("🔺 삼각형 (무게 5)")
        c1, c2 = st.columns(2)
        c1.button("➕ 추가", key="t1_r_add_tri", on_click=modify_shape, args=('t1_right', 'tri', 1), use_container_width=True)
        c2.button("➖ 빼기", key="t1_r_sub_tri", on_click=modify_shape, args=('t1_right', 'tri', -1), use_container_width=True)
        
        st.write("🟩 사각형 (무게 3)")
        c1, c2 = st.columns(2)
        c1.button("➕ 추가", key="t1_r_add_sq", on_click=modify_shape, args=('t1_right', 'sq', 1), use_container_width=True)
        c2.button("➖ 빼기", key="t1_r_sub_sq", on_click=modify_shape, args=('t1_right', 'sq', -1), use_container_width=True)
        
        st.write("🟣 원 (무게 2)")
        c1, c2 = st.columns(2)
        c1.button("➕ 추가", key="t1_r_add_cir", on_click=modify_shape, args=('t1_right', 'cir', 1), use_container_width=True)
        c2.button("➖ 빼기", key="t1_r_sub_cir", on_click=modify_shape, args=('t1_right', 'cir', -1), use_container_width=True)

        st.write("") 
        st.write("") 
        if st.button("🔄 초기화", key="t1_reset", use_container_width=True):
            reset_scale('t1_left', 't1_right')
            st.rerun()

    with t1_col_mid:
        draw_balance_scale(t1_l_wt, t1_r_wt, st.session_state.t1_left, st.session_state.t1_right)

# =============================================================================
# [TAB 2] 등식의 성질 (미지수)
# =============================================================================
with tab2:
    # 학생들은 모르는 '숨겨진 무게' 설정 (임의로 삼각형=2, 사각형=3, 원=5 로 설정)
    # 삼각형 + 사각형 = 원 (2 + 3 = 5) 식이 성립하도록 세팅했습니다.
    T2_HIDDEN_WEIGHTS = {'tri': 2, 'sq': 3, 'cir': 5}
    
    if 't2_left' not in st.session_state: st.session_state.t2_left =[]  
    if 't2_right' not in st.session_state: st.session_state.t2_right =[]

    t2_l_wt = get_weight(st.session_state.t2_left, T2_HIDDEN_WEIGHTS)
    t2_r_wt = get_weight(st.session_state.t2_right, T2_HIDDEN_WEIGHTS)

    t2_col_left, t2_col_mid, t2_col_right = st.columns([1, 2.5, 1])

    with t2_col_left:
        st.subheader("왼쪽 접시")
        st.write("🔺 삼각형 (무게 ?)")
        c1, c2 = st.columns(2)
        c1.button("➕ 추가", key="t2_l_add_tri", on_click=modify_shape, args=('t2_left', 'tri', 1), use_container_width=True)
        c2.button("➖ 빼기", key="t2_l_sub_tri", on_click=modify_shape, args=('t2_left', 'tri', -1), use_container_width=True)
        
        st.write("🟩 사각형 (무게 ?)")
        c1, c2 = st.columns(2)
        c1.button("➕ 추가", key="t2_l_add_sq", on_click=modify_shape, args=('t2_left', 'sq', 1), use_container_width=True)
        c2.button("➖ 빼기", key="t2_l_sub_sq", on_click=modify_shape, args=('t2_left', 'sq', -1), use_container_width=True)
        
        st.write("🟣 원 (무게 ?)")
        c1, c2 = st.columns(2)
        c1.button("➕ 추가", key="t2_l_add_cir", on_click=modify_shape, args=('t2_left', 'cir', 1), use_container_width=True)
        c2.button("➖ 빼기", key="t2_l_sub_cir", on_click=modify_shape, args=('t2_left', 'cir', -1), use_container_width=True)

    with t2_col_right:
        st.subheader("오른쪽 접시")
        st.write("🔺 삼각형 (무게 ?)")
        c1, c2 = st.columns(2)
        c1.button("➕ 추가", key="t2_r_add_tri", on_click=modify_shape, args=('t2_right', 'tri', 1), use_container_width=True)
        c2.button("➖ 빼기", key="t2_r_sub_tri", on_click=modify_shape, args=('t2_right', 'tri', -1), use_container_width=True)
        
        st.write("🟩 사각형 (무게 ?)")
        c1, c2 = st.columns(2)
        c1.button("➕ 추가", key="t2_r_add_sq", on_click=modify_shape, args=('t2_right', 'sq', 1), use_container_width=True)
        c2.button("➖ 빼기", key="t2_r_sub_sq", on_click=modify_shape, args=('t2_right', 'sq', -1), use_container_width=True)
        
        st.write("🟣 원 (무게 ?)")
        c1, c2 = st.columns(2)
        c1.button("➕ 추가", key="t2_r_add_cir", on_click=modify_shape, args=('t2_right', 'cir', 1), use_container_width=True)
        c2.button("➖ 빼기", key="t2_r_sub_cir", on_click=modify_shape, args=('t2_right', 'cir', -1), use_container_width=True)

        st.write("") 
        st.write("") 
        if st.button("🔄 초기화", key="t2_reset", use_container_width=True):
            reset_scale('t2_left', 't2_right')
            st.rerun()

    with t2_col_mid:
        draw_balance_scale(t2_l_wt, t2_r_wt, st.session_state.t2_left, st.session_state.t2_right)