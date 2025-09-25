# pig_game_app_v2.py

import streamlit as st
import pandas as pd
import numpy as np
import random
import time
import plotly.graph_objects as go # [추가] Plotly 라이브러리 임포트

# --- 1. 페이지 기본 설정 ---
st.set_page_config(
    page_title="Pig Game",
    page_icon="🎲",
    layout="wide"
)

# --- 2. 사이드바: 게임 설정 ---
with st.sidebar:
    st.header("🎲 게임 설정")
    num_players = st.slider("모둠 수", min_value=2, max_value=10, value=2)
    winning_score = st.number_input("목표 점수", min_value=20, max_value=500, value=100, step=10)
    
    # [수정] 플레이어 이름 입력을 제거하고, '새 게임 시작' 버튼만 남깁니다.
    if st.button("🚀 새 게임 시작", type="primary"):
        st.session_state.clear() 
        st.session_state.num_players = num_players
        st.session_state.winning_score = winning_score
        
        # [수정] 버튼 클릭 시, '1모둠', '2모둠'... 형식으로 플레이어 이름을 자동으로 생성합니다.
        st.session_state.player_names = [f"{i+1}모둠" for i in range(num_players)]
        st.rerun()

# --- 3. 게임 상태 초기화 함수 (변경 없음) ---
def initialize_game():
    if 'player_scores' not in st.session_state:
        st.session_state.player_scores = [0] * st.session_state.num_players
        st.session_state.current_player = 0
        st.session_state.pending_score = 0
        st.session_state.last_roll = "🎲"
        st.session_state.game_over = False
        st.session_state.winner = None
        st.session_state.roll_history = []
        st.session_state.turn_over_message = ""

# --- 4. 핵심 게임 로직 함수 (변경 없음) ---
def next_turn():
    st.session_state.current_player = (st.session_state.current_player + 1) % st.session_state.num_players
    st.session_state.pending_score = 0
    st.session_state.last_roll = "🎲"
    time.sleep(0.5) 

def roll_dice():
    roll = random.randint(1, 6)
    st.session_state.last_roll = roll
    st.session_state.roll_history.append(roll)
    
    if roll == 1:
        st.session_state.pending_score = 0
        st.session_state.turn_over_message = f"앗! 1이 나왔습니다. 점수를 모두 잃고 턴이 넘어갑니다."
        next_turn()
    else:
        st.session_state.pending_score += roll
        st.session_state.turn_over_message = ""

def hold():
    current_player_idx = st.session_state.current_player
    st.session_state.player_scores[current_player_idx] += st.session_state.pending_score
    st.session_state.turn_over_message = f"{st.session_state.pending_score}점을 획득했습니다!"

    if st.session_state.player_scores[current_player_idx] >= st.session_state.winning_score:
        st.session_state.game_over = True
        st.session_state.winner = st.session_state.player_names[current_player_idx]
    else:
        next_turn()

# --- 5. 메인 UI 렌더링 ---
if 'player_scores' not in st.session_state:
    st.info("👈 사이드바에서 설정을 마친 후 '새 게임 시작' 버튼을 눌러주세요.")
else:
    initialize_game()
    active_player_name = st.session_state.player_names[st.session_state.current_player]

    st.header(f"👑 현재 차례: **{active_player_name}**")
    
    score_data = {
        '모둠명': st.session_state.player_names,
        '총 점수': st.session_state.player_scores,
    }
    pending_scores_display = ["-"] * st.session_state.num_players
    if not st.session_state.game_over:
        pending_scores_display[st.session_state.current_player] = f"+ {st.session_state.pending_score}"
    score_data['획득 예정 점수'] = pending_scores_display
    
    score_df = pd.DataFrame(score_data)
    st.dataframe(score_df.set_index('모둠명').T, use_container_width=True) 

    st.divider()
    col1, col2 = st.columns([0.4, 0.6])

    with col1:
        st.markdown(f"<p style='text-align: center; font-size: 100px; font-weight: bold; margin: 0; line-height: 1;'>{st.session_state.last_roll}</p>", unsafe_allow_html=True)
        st.metric(label="이번 라운드 점수", value=f"{st.session_state.pending_score} 점")
        btn_cols = st.columns(2)
        with btn_cols[0]:
            st.button("주사위 던지기", on_click=roll_dice, use_container_width=True, disabled=st.session_state.game_over)
        with btn_cols[1]:
            st.button("그만하기", on_click=hold, use_container_width=True, disabled=st.session_state.game_over)
        if st.session_state.turn_over_message:
            st.info(st.session_state.turn_over_message)

    with col2: 
        with st.expander("📜 게임 방법 보기", expanded=True):
            st.markdown(f"""
            - **목표:** 먼저 **{st.session_state.winning_score}점**에 도달하세요!
            - **진행:**
                1. 자기 차례가 되면 '주사위 던지기'를 계속할 수 있습니다.
                2. 나온 눈의 수가 '이번 라운드 점수'에 계속 더해집니다.
                3. **하지만 주사위 눈이 `1`이 나오면...** 이번 라운드 점수는 **0점**이 되고, 즉시 다음 사람에게 차례가 넘어갑니다.
                4. `1`이 나오기 전에 '그만하기'를 누르면, 이번 라운드 점수가 '총 점수'에 더해지고 차례가 넘어갑니다.
            """)

        # --- [핵심 수정] 주사위 통계 차트 ---
        st.subheader("📊 주사위 눈 비율 (부드러운 꺾은선)")
        if st.session_state.roll_history:
            # 1. 주사위 눈(1~6)에 대한 빈도 계산
            roll_counts = pd.Series(st.session_state.roll_history).value_counts()
            # 2. 전체 주사위 눈(1~6)에 대한 데이터프레임 생성 (던져지지 않은 눈도 0으로 표시하기 위함)
            full_counts = pd.Series(index=range(1, 7), data=0, dtype=int)
            full_counts.update(roll_counts)
            
            # 3. 빈도를 전체 던진 횟수로 나누어 '비율' 계산
            total_rolls = len(st.session_state.roll_history)
            roll_ratio = full_counts / total_rolls

            # 4. Plotly를 사용하여 부드러운 꺾은선 그래프 생성
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=roll_ratio.index, 
                y=roll_ratio.values, 
                mode='lines+markers', 
                name='비율',
                line_shape='spline'  # 이 옵션이 선을 부드럽게 만듭니다!
            ))
            # 5. 차트 레이아웃 설정
            fig.update_layout(
                xaxis_title="주사위 눈",
                yaxis_title="비율",
                yaxis_range=[0, 1] # Y축 범위를 0에서 1로 고정
            )
            # 6. st.plotly_chart로 스트림릿에 표시
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.caption("아직 주사위를 던지지 않았습니다.")

    if st.session_state.game_over:
        st.balloons()
        st.success(f"🎉 **게임 종료! 승자는 {st.session_state.winner} 입니다!** 🎉")
        st.warning("새 게임을 시작하려면 사이드바에서 '새 게임 시작' 버튼을 누르세요.")