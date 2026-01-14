import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ripser import ripser
from persim import plot_diagrams

# --------------------------------------------------------------------------------
# 1. 페이지 설정 및 스타일
# --------------------------------------------------------------------------------
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; color: #4B4B4B; text-align: center; margin-bottom: 1rem; }
    .sub-header { font-size: 1.5rem; color: #007BFF; margin-top: 1rem; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🧬 TDA: 지속구간 다이어그램(Persistence Diagram) 실습</div>', unsafe_allow_html=True)
st.info("데이터 분포의 위상적 특징(구멍, 연결 성분 등)을 시각화하여 데이터의 모양을 분석해 봅시다.")

# --------------------------------------------------------------------------------
# 2. 데이터 초기화 및 입력 (Normal 10개, High BP 10개)
# --------------------------------------------------------------------------------
col_input1, col_input2 = st.columns(2)

# 기본 데이터 생성 (예시: 정상군은 (2,2) 근처, 고혈압군은 (6,6) 근처에 군집)
default_normal = pd.DataFrame({
    'x': [1.8, 2.1, 2.5, 1.5, 2.9, 3.1, 2.2, 1.9, 2.8, 2.0],
    'y': [2.2, 1.9, 2.8, 2.1, 2.5, 3.2, 3.0, 1.8, 2.1, 2.4]
})

default_high_bp = pd.DataFrame({
    'x': [5.8, 6.1, 6.5, 5.5, 6.9, 7.1, 6.2, 5.9, 6.8, 6.0],
    'y': [6.2, 5.9, 6.8, 6.1, 6.5, 7.2, 7.0, 5.8, 6.1, 6.4]
})

with col_input1:
    st.markdown("### 🟢 정상군 데이터 (10개)")
    df_normal = st.data_editor(default_normal, num_rows="dynamic", key="normal_data", height=300)

with col_input2:
    st.markdown("### 🔴 고혈압군 데이터 (10개)")
    df_high_bp = st.data_editor(default_high_bp, num_rows="dynamic", key="high_bp_data", height=300)

# --------------------------------------------------------------------------------
# 3. 데이터 병합 및 1차 분석 (기본 데이터)
# --------------------------------------------------------------------------------
st.divider()
st.markdown('<div class="sub-header">1️⃣ 기본 데이터 분석 결과</div>', unsafe_allow_html=True)

# 데이터프레임을 Numpy 배열로 변환
try:
    X_normal = df_normal.to_numpy()
    X_high = df_high_bp.to_numpy()
    
    # 두 집합 합치기
    X_original = np.vstack([X_normal, X_high])
    
    col_res1, col_res2 = st.columns(2)

    # (1) 산점도 그리기
    with col_res1:
        st.write("##### 📊 데이터 산점도 (Scatter Plot)")
        fig1, ax1 = plt.subplots(figsize=(5, 5))
        ax1.scatter(X_normal[:, 0], X_normal[:, 1], c='green', label='Normal')
        ax1.scatter(X_high[:, 0], X_high[:, 1], c='red', label='High BP')
        ax1.legend()
        ax1.set_title("Data Distribution")
        ax1.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig1)

    # (2) 지속구간 다이어그램 그리기
    with col_res2:
        st.write("##### 🕸️ 지속구간 다이어그램 (Persistence Diagram)")
        # Ripser 실행 (maxdim=1: 0차원(연결성분), 1차원(구멍/루프) 까지 계산)
        diagrams_original = ripser(X_original, maxdim=1)['dgms']
        
        fig2, ax2 = plt.subplots(figsize=(5, 5))
        plot_diagrams(diagrams_original, show=False, ax=ax2)
        ax2.set_title("Persistence Diagram (Original)")
        st.pyplot(fig2)
        
        st.caption("""
        - **H0 (파란 점)**: 연결 성분 (데이터 덩어리)
        - **H1 (주황 점)**: 구멍 (Loop)
        """)

except Exception as e:
    st.error(f"데이터 형식이 올바르지 않습니다. 숫자만 입력해주세요. ({e})")

# --------------------------------------------------------------------------------
# 4. 추가 데이터 입력 및 2차 분석
# --------------------------------------------------------------------------------
st.divider()
st.markdown('<div class="sub-header">2️⃣ 추가 데이터 입력 및 변화 확인</div>', unsafe_allow_html=True)

st.write("아래 표에 **새로운 데이터**를 추가해보세요. 위상적 구조(H0, H1)가 어떻게 변하는지 확인합니다.")

# 추가 데이터 초기값 (빈 데이터프레임)
default_new = pd.DataFrame({'x': [4.0], 'y': [4.0]}) # 예시로 중간값 하나 넣어둠
df_new = st.data_editor(default_new, num_rows="dynamic", key="new_data")

if not df_new.empty:
    try:
        X_new_points = df_new.to_numpy()
        
        # 기존 데이터 + 새로운 데이터 병합
        X_final = np.vstack([X_original, X_new_points])
        
        col_new1, col_new2 = st.columns(2)

        # (1) 업데이트된 산점도
        with col_new1:
            st.write("##### 📊 업데이트된 산점도")
            fig3, ax3 = plt.subplots(figsize=(5, 5))
            ax3.scatter(X_normal[:, 0], X_normal[:, 1], c='green', label='Normal', alpha=0.3)
            ax3.scatter(X_high[:, 0], X_high[:, 1], c='red', label='High BP', alpha=0.3)
            # 새로운 데이터는 파란색 별모양으로 강조
            ax3.scatter(X_new_points[:, 0], X_new_points[:, 1], c='blue', marker='*', s=200, label='New Data')
            ax3.legend()
            ax3.set_title("Data Distribution (Updated)")
            ax3.grid(True, linestyle='--', alpha=0.6)
            st.pyplot(fig3)

        # (2) 업데이트된 지속구간 다이어그램
        with col_new2:
            st.write("##### 🕸️ 업데이트된 지속구간 다이어그램")
            diagrams_final = ripser(X_final, maxdim=1)['dgms']
            
            fig4, ax4 = plt.subplots(figsize=(5, 5))
            plot_diagrams(diagrams_final, show=False, ax=ax4)
            ax4.set_title("Persistence Diagram (Final)")
            st.pyplot(fig4)
            
            st.success("새로운 데이터가 추가되어 위상적 특징이 다시 계산되었습니다!")

    except Exception as e:
        st.error(f"추가 데이터 오류: {e}")

else:
    st.warning("추가 데이터를 입력하면 그래프가 생성됩니다.")