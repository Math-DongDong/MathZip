
# Streamlit 기반 돼지게임(Pig Game) 대대적 개편
import streamlit as st
import pandas as pd

st.set_page_config(page_title="스트림스 돼지게임", layout="wide")

# --- 상단 타이틀 3분할 ---
title_cols = st.columns([1, 1, 1])
with title_cols[0]:
    st.markdown("<h1 style='margin-bottom:0'>🐷 스트림스 돼지게임</h1>", unsafe_allow_html=True)
with title_cols[1]:
    st.write("")
with title_cols[2]:
    st.write("")
    st.button("새로 시작하기", key="reset_btn")

# --- 본문 1:3 분할 ---
main_cols = st.columns([1, 3])

# 좌측: 주사위 눈 표시
with main_cols[0]:
    st.markdown("#### 주사위 눈")
    st.markdown("""
    <div style='font-size:100px; text-align:center; border:2px solid #bbb; border-radius:20px; width:90%; margin:auto; background:#f9f9f9;'>
    ❔
    </div>
    """, unsafe_allow_html=True)

# 우측: 첨부 이미지와 동일한 구조의 점수표 (가로: 1~8, 세로: 총 점수/획득 예정 점수)
with main_cols[1]:
    st.markdown("#### 점수표 (편집 가능)")
    col_names = [str(i+1) for i in range(8)]
    row_names = ['총 점수', '획득 예정 점수']
    score_table = pd.DataFrame(0, index=row_names, columns=col_names)
    edited_table = st.data_editor(score_table, use_container_width=True, key="score_table_editor")

# (불필요한 잔여 코드 및 들여쓰기 오류 구간 삭제)
