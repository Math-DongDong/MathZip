# Streamlit 기반 돼지게임(Pig Game) 구현
import streamlit as st
import random
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="스트림스 돼지게임", layout="wide")

# 세션 상태 초기화
if 'pig_scores' not in st.session_state:
	st.session_state.pig_scores = [0, 0]
if 'pig_current' not in st.session_state:
	st.session_state.pig_current = 0
if 'pig_turn' not in st.session_state:
	st.session_state.pig_turn = 0  # 0: 플레이어1, 1: 플레이어2
if 'pig_round' not in st.session_state:
	st.session_state.pig_round = 1
if 'pig_history' not in st.session_state:
	st.session_state.pig_history = ["" for _ in range(10)]
if 'pig_dice_counts' not in st.session_state:
	st.session_state.pig_dice_counts = [0]*6
if 'pig_last_dice' not in st.session_state:
	st.session_state.pig_last_dice = None

def pig_reset():
	st.session_state.pig_scores = [0, 0]
	st.session_state.pig_current = 0
	st.session_state.pig_turn = 0
	st.session_state.pig_round = 1
	st.session_state.pig_history = ["" for _ in range(10)]
	st.session_state.pig_dice_counts = [0]*6
	st.session_state.pig_last_dice = None

def pig_roll():
	dice = random.randint(1,6)
	st.session_state.pig_last_dice = dice
	st.session_state.pig_dice_counts[dice-1] += 1
	if dice == 1:
		st.session_state.pig_current = 0
		st.session_state.pig_round = min(st.session_state.pig_round+1, 10)
		st.session_state.pig_turn = 1 - st.session_state.pig_turn
	else:
		st.session_state.pig_current += dice

def pig_hold():
	idx = st.session_state.pig_round-1
	st.session_state.pig_scores[st.session_state.pig_turn] += st.session_state.pig_current
	if idx < 10:
		st.session_state.pig_history[idx] = st.session_state.pig_current
	st.session_state.pig_current = 0
	st.session_state.pig_round = min(st.session_state.pig_round+1, 10)
	st.session_state.pig_turn = 1 - st.session_state.pig_turn

# 상단 점수표 및 UI
st.markdown("<h5>※ 플레이어 간을 선택하고 주사위를 던지면 됩니다.</h5>", unsafe_allow_html=True)
score_cols = st.columns([1, 2, 7])
with score_cols[0]:
	st.markdown(f"<div style='font-size:60px; text-align:center; font-weight:bold'>{st.session_state.pig_turn+1}</div>", unsafe_allow_html=True)
with score_cols[1]:
	st.button("새로시작하기", on_click=pig_reset)
	st.markdown(f"<div style='font-size:22px; margin-top:10px'>총 점수</div>")
	st.markdown(f"<div style='font-size:28px; font-weight:bold'>{st.session_state.pig_scores[st.session_state.pig_turn]}</div>")
	st.markdown(f"<div style='font-size:22px; margin-top:10px'>획득 예정 점수</div>")
	st.markdown(f"<div style='font-size:28px; font-weight:bold'>{st.session_state.pig_current}</div>")
with score_cols[2]:
	rounds = [i+1 for i in range(10)]
	data = {"라운드": rounds, "점수": st.session_state.pig_history}
	df = pd.DataFrame(data)
	st.table(df.set_index("라운드"))

# 버튼
btn_cols = st.columns([2, 2, 6])
with btn_cols[0]:
	if st.button("주사위던지기", key="pig_roll"):
		pig_roll()
with btn_cols[1]:
	if st.button("그만하기", key="pig_hold"):
		pig_hold()

# 하단: 그래프, 안내, 통계표
bottom_cols = st.columns([4, 4, 4])
with bottom_cols[0]:
	st.markdown("#### 주사위 비율")
	fig, ax = plt.subplots(figsize=(3,2))
	total = sum(st.session_state.pig_dice_counts)
	if total > 0:
		ax.bar(range(1,7), [c/total for c in st.session_state.pig_dice_counts], color="#4F81BD")
		ax.set_ylim(0,1)
	else:
		ax.bar(range(1,7), [0]*6, color="#4F81BD")
		ax.set_ylim(0,1)
	ax.set_xticks(range(1,7))
	ax.set_xlabel("주사위 눈")
	ax.set_ylabel("비율")
	st.pyplot(fig)
with bottom_cols[1]:
	st.markdown("#### <게임 방법>")
	st.markdown("""
자기 차례가 되면 주사위를 계속 굴려, 나오는 눈의 수를 더해 나간다.\
이 점수가 이번 라운드의 획득 예정 점수가 된다.\
**그만!**을 누르면 점수가 쌓이고, 1이 나오면 이번 획득 예정 점수는 0점이 된다.\
이 과정을 반복하여 먼저 100점을 넘는 사람이 승리한다.
	""")
with bottom_cols[2]:
	st.markdown("#### 주사위 눈 통계")
	dice_df = pd.DataFrame({
		"주사위 눈": range(1,7),
		"누적": st.session_state.pig_dice_counts,
		"비율": [f"{(c/total*100):.1f}%" if total>0 else "0%" for c in st.session_state.pig_dice_counts]
	})
	st.table(dice_df.set_index("주사위 눈"))

# 승리 조건 안내
if st.session_state.pig_scores[0] >= 100 or st.session_state.pig_scores[1] >= 100:
	winner = 1 if st.session_state.pig_scores[0] >= 100 else 2
	st.success(f"플레이어 {winner} 승리!")
