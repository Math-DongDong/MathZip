import streamlit as st
import random
import time

st.title("🎲 주사위 모음")

# -----------------------------------------------------------------------------
# 2. 콜백(Callback) 함수 정의
# -----------------------------------------------------------------------------
# 연산 pill에서 '없음'을 눌렀을 때의 똑똑한 동작을 제어하는 함수입니다.
def on_op_change():
    curr = st.session_state.op_pills
    prev = st.session_state.get('prev_op_pills',[])
    
    # 1) '없음'을 방금 새로 선택한 경우 -> 다른 연산을 모두 지우고 '없음'만 남김
    if "🚫 없음" in curr and "🚫 없음" not in prev:
        st.session_state.op_pills = ["🚫 없음"]
    # 2) '없음'이 있는 상태에서 다른 연산을 선택한 경우 -> '없음'을 지움
    elif "🚫 없음" in curr and len(curr) > 1:
        curr.remove("🚫 없음")
        st.session_state.op_pills = curr
    # 3) 사용자가 모든 선택을 해제해버린 경우 -> 다시 '없음'으로 되돌림
    elif len(curr) == 0:
        st.session_state.op_pills = ["🚫 없음"]
        
    # 현재 상태를 이전 상태로 저장 (다음 비교를 위해)
    st.session_state.prev_op_pills = st.session_state.op_pills

# -----------------------------------------------------------------------------
# 3. 세션 상태(Session State) 초기화
# -----------------------------------------------------------------------------
# UI의 기본값을 설정합니다.
if 'op_pills' not in st.session_state:
    st.session_state.op_pills = ["🚫 없음"]
    st.session_state.prev_op_pills = ["🚫 없음"]
if 'sign_pill' not in st.session_state:
    st.session_state.sign_pill = "미포함"
if 'dice_result' not in st.session_state:
    st.session_state.dice_result = "❔"

# -----------------------------------------------------------------------------
# 4. 설정 UI 영역 (st.pills 활용)
# -----------------------------------------------------------------------------
with st.expander("⚙️ 주사위 설정 열기"):
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.write("**1. 연산 기호** (다중 선택 가능)")
        st.pills(
            "연산", 
            options=["➕ 덧셈", "➖ 뺄셈", "✖️ 곱셈", "➗ 나눗셈", "🚫 없음"],
            selection_mode="multi", # 여러 개 선택 가능
            key="op_pills",
            on_change=on_op_change, # 클릭할 때마다 위에서 만든 함수 실행
            label_visibility="collapsed"
        )

    with col2:
        st.write("**2. 부호(+, -) 포함 여부**")
        st.pills(
            "부호",
            options=["포함", "미포함"],
            selection_mode="single", # 무조건 하나만 선택
            key="sign_pill",
            label_visibility="collapsed"
        )


# -----------------------------------------------------------------------------
# 5. 주사위 결과 생성 로직
# -----------------------------------------------------------------------------
def generate_dice_face(ops_list, include_sign):
    """현재 설정된 pill 값들을 바탕으로 주사위의 텍스트를 조합하는 함수입니다."""
    
    # 1. 연산자 결정 (선택된 것들 중 랜덤으로 하나 뽑기)
    op_map = {"➕ 덧셈": "➕", "➖ 뺄셈": "➖", "✖️ 곱셈": "✖️", "➗ 나눗셈": "➗"}
    valid_ops = [op_map[op] for op in ops_list if op in op_map]
    
    op_str = ""
    if valid_ops:
        op_str = random.choice(valid_ops) + " " # 예: "➕ "
        
    # 2. 부호 결정 (+ 또는 -)
    sign_str = ""
    if include_sign == "포함":
        sign_str = random.choice(["+", "-"]) # 예: "-"
        
    # 3. 숫자 결정 (1~6)
    num_str = str(random.randint(1, 6))      # 예: "5"
    
    # 음수가 연산과 같이 나오는 경우 괄호로 묶기 (부호 포함 시 양수도 괄호)
    if sign_str and op_str:
        num_part = f"({sign_str}{num_str})"
    else:
        num_part = f"{sign_str}{num_str}"
    
    # 최종 조합 리턴 (연산자와 숫자 부분을 분리해서 리턴)
    return op_str, num_part

# -----------------------------------------------------------------------------
# 6. 주사위 굴리기 애니메이션 및 결과 화면
# -----------------------------------------------------------------------------
# 버튼을 엄청 크고 돋보이게 만듭니다.
if st.button("🎲 주사위 굴리기", type="primary"):
    placeholder = st.empty()
    start_delay = 0.05
    end_delay = 0.4
    total_steps = 15
    
    # 안전 장치: 값이 비어있을 경우 기본값 세팅
    curr_ops = st.session_state.op_pills if st.session_state.op_pills else ["🚫 없음"]
    curr_sign = st.session_state.sign_pill if st.session_state.sign_pill else "미포함"
    
    # 애니메이션(드르르륵 굴러가는 효과)
    for i in range(total_steps):
        op, num = generate_dice_face(curr_ops, curr_sign)
        temp_result = f"<small>{op}</small>{num}"
        with placeholder.container():
            st.markdown(f"<h1 style='text-align: center; font-size: 130px; padding: 40px 0;'>{temp_result}</h1>", unsafe_allow_html=True)
        
        # 갈수록 느려지는 효과 (마찰력 구현)
        progress = i / total_steps
        current_delay = start_delay + (progress * (end_delay - start_delay))
        if i < total_steps - 1:
            time.sleep(current_delay)

    # 최종 결과 고정
    op, num = generate_dice_face(curr_ops, curr_sign)
    final_result = f"<small>{op}</small>{num}"
    st.session_state.dice_result = final_result # 저장
    
    with placeholder.container():
        # 결과는 파란색으로 조금 더 예쁘게 강조!
        st.markdown(f"<h1 style='text-align: center; font-size: 130px; padding: 40px 0; color: #1E88E5;'>{final_result}</h1>", unsafe_allow_html=True)

else:
    # 평상시(버튼 누르기 전) 화면
    st.markdown(f"<h1 style='text-align: center; font-size: 130px; padding: 40px 0;'>{st.session_state.dice_result}</h1>", unsafe_allow_html=True)