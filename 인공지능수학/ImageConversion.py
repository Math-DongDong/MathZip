import streamlit as st
import numpy as np
import pandas as pd
import streamlit.components.v1 as components
from PIL import Image
import io # 이미지를 바이트 형태로 변환하여 다운로드하기 위해 필요

# 커스텀 CSS 적용
st.markdown("""
<style>
/* 표의 머릿글과 왼쪽 인덱스 숨기기 (필요시) */
.e10e2fxn5 {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# --- 앱 제목 ---
st.title("이미지 데이터의 변환")

# 탭 생성
tab1, tab2, tab3, tab4= st.tabs(["🔘 그레이 필터", "💡 밝기 조절", "➕ 합성" , "↔️ 평행이동 및 방향 변환"])

# ==============================================================================
# [TAB 1] 그레이 필터
# ==============================================================================
with tab1:

    # 함수 정의 (RGB 데이터 시각화)
    def display_channel_data(image_array, title_prefix):
        st.markdown(f"#### 📊 {title_prefix}의 RGB 채널")
        st.caption("좌측 상단(0,0)부터 **8x8 픽셀** 영역의 숫자(0~255)입니다.")
        slice_size = 8
        
        # 배열 크기가 8보다 작을 경우 에러 방지
        rows = min(slice_size, image_array.shape[0])
        cols = min(slice_size, image_array.shape[1])

        # 채널 분리
        r_channel = image_array[:rows, :cols, 0]
        g_channel = image_array[:rows, :cols, 1]
        b_channel = image_array[:rows, :cols, 2]

        # 데이터프레임 생성
        df_r = pd.DataFrame(r_channel)
        df_g = pd.DataFrame(g_channel)
        df_b = pd.DataFrame(b_channel)

        # 3열 배치
        c1, c2, c3 = st.columns(3)
        with c1:
            st.write("🔴 Red")
            st.table(df_r)
        with c2:
            st.write("🟢 Green")
            st.table(df_g)
        with c3:
            st.write("🔵 Blue")
            st.table(df_b)

    # 이미지 업로드 창 생성
    with st.expander("📂 이미지 업로드 열기/닫기", expanded=True):
        uploaded_file = st.file_uploader("이미지 파일을 업로드하세요.", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # 1. 이미지 열기 (무조건 RGB 3채널로 변환)
        image = Image.open(uploaded_file).convert('RGB')
        original_width, original_height = image.size

        # 메인 레이아웃 ( 원본 | 결과)
        col_orig, col_res = st.columns(2, gap="medium")
        # [1열] 원본
        with col_orig:
            st.subheader("원본 이미지")
            st.image(image, caption=f"원본 이미지 ( 해상도: {original_width}x{original_height} px )", width='stretch')

        # [2열] 결과 (Gray)
        with col_res:
            st.subheader("그레이 필터")

            # 1) 그레이스케일 변환 (단순 평균법)
            # (H, W, 3) -> (H, W) : 채널 축(axis=2) 기준 평균
            gray_matrix = np.round(np.mean(np.array(image), axis=2)).astype(np.uint8)

            # 2) 다시 3채널로 복구 (시각화 및 통일성을 위해 R=G=B로 만듦)
            # (H, W) -> (H, W, 3)
            gray_stacked_arr = np.stack((gray_matrix, gray_matrix, gray_matrix), axis=2)
            gray_small_pil = Image.fromarray(gray_stacked_arr)

            # 3) 원본 크기로 뻥튀기 (각진 느낌 유지)
            preview_pil = gray_small_pil.resize((original_width, original_height), Image.Resampling.NEAREST)
            
            st.image(preview_pil, caption="그레이 필터 적용", width='stretch')

        # --------------------------------------------------------------------------
        # 3. 데이터 분석 표 (하단)
        # --------------------------------------------------------------------------
        st.divider()
        
        # (1) 원본 데이터
        original_array = np.array(image)
        display_channel_data(original_array, "원본 이미지")

        st.divider()

        # (2) 변환된 데이터 (주의: gray_stacked_arr 사용)
        # 그레이스케일이므로 R, G, B 표의 숫자가 모두 똑같아야 정상입니다.
        display_channel_data(gray_stacked_arr, "그레이 필터 이미지")

    else:
            st.info("👆 상단의 '이미지 업로드'를 열어 이미지 파일( png, jpg, jpeg )을 먼저 업로드해주세요.")    

    with st.container(horizontal=True):
        st.space("stretch")
        st.page_link("https://matharticle.streamlit.app/grayscale", label="그레이 필터 이미지 데이터 다운로드", icon="🔀", width="content")
                
    
# ==============================================================================
# [TAB 2] 밝기 조절
# ==============================================================================
with tab2:
    st.text("밝기")

with tab3:
    with st.container(horizontal=True):
        st.space("stretch")
        st.page_link("https://matharticle.streamlit.app/Dissolve", label="디졸브 효과", icon="🔀", width="content")

with tab4:
    st.text("평행")
