import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image

# 커스텀 CSS 적용
st.markdown("""
<style>
/* 탭1 - 표의 머릿글과 왼쪽 인덱스 숨기기*/
#tabs-bui9-tabpanel-0 .e10e2fxn5 {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# 함수정의(탭2, 탭3 공통)
@st.cache_data(show_spinner=False, ttl=300)
def load_excel_data(file):
    return pd.read_excel(file, header=None)

def df_to_image(df, scale_factor=20):
    # 유효 범위(0~255) 클리핑 및 형변환
    data = df.fillna(0).clip(0, 255).to_numpy().astype(np.uint8)
    
    img = Image.fromarray(data)
    original_w, original_h = img.size
    
    # 화면에 잘 보이도록 확대 (최소 500px)
    target_w = max(500, original_w * scale_factor)
    target_h = int(target_w * (original_h / original_w))
    
    # NEAREST 옵션으로 픽셀화 효과 유지
    img_resized = img.resize((target_w, target_h), Image.Resampling.NEAREST)
    return img_resized, (original_w, original_h)

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

        # 3. 데이터 분석 표 (하단)
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
    # 초기 원본 데이터(source_df)를 확정하기 위한 변수
    source_df = None

    # 엑셀 업로드 창
    with st.expander("📂 픽셀 데이터 업로드 열기/닫기", expanded=True):
        uploaded_file = st.file_uploader(
            "그레이 필터 이미지의 픽셀 데이터(Excel) 업로드",
            type=['xlsx']
        )

    if uploaded_file is not None:
        source_df = load_excel_data(uploaded_file)

    # 앱이 처음 실행되거나, 소스 데이터가 아예 없을 때 초기화
    if "current_df" not in st.session_state:
        st.session_state.current_df = None

    # 소스 데이터가 로드되었는데, 현재 작업 중인 데이터가 없다면 초기화
    if st.session_state.current_df is None and source_df is not None:
        st.session_state.current_df = source_df.copy()

    if st.session_state.current_df is not None:
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            # 연산 버튼 설정
            with st.container(horizontal=True):
                operation = st.selectbox(
                    "연산 종류",
                    ("➕ 덧셈","➖ 뺄셈","✖️ 곱셈")
                )

                number = st.number_input(
                    "연산할 값",
                    min_value=0.0,
                    max_value=30.0, # 연산값은 좀 더 자유롭게
                    value=10.0,
                    step=1.0,
                    format="%.1f"
                )
        with p_col2:
            st.space()
            with st.container(horizontal=True):    
                if st.button("🔄 원본 불러오기", type="secondary", width='stretch'):
                    st.session_state.current_df = source_df.copy()
                    st.rerun()

                run_calc = st.button("🚀 연산 실행", type="primary", width='stretch')


        # --- [B] 연산 로직 (누적 적용) ---
        if run_calc:
            # 현재 화면에 떠있는 데이터를 가져옴 (누적 연산을 위해)
            df_calc = st.session_state.current_df.copy()

            if "덧셈" in operation:
                df_calc = df_calc + number
            elif "뺄셈" in operation:
                df_calc = df_calc - number
            elif "곱셈" in operation:
                df_calc = df_calc * number

            # 클리핑 (0~255 유지) 및 정수 변환
            df_calc = df_calc.clip(0, 255)
            df_calc = np.round(df_calc, 0).astype(int)
            
            # [중요] 연산 결과를 '현재 데이터'로 업데이트 (누적 효과)
            st.session_state.current_df = df_calc
            st.rerun() # 화면 갱신


        # --- [C] 결과 화면 (Left: Dataframe / Right: Image) ---
        col_left, col_right = st.columns(2, gap="large")
        with col_left:
            # 데이터프레임의 크기 정보
            curr_r, curr_c = st.session_state.current_df.shape
            st.caption(f"연산이 누적되어 적용된 행렬( {curr_r} x {curr_c} )입니다.")

            # [요청사항] 원본/연산 데이터를 여기서 확인
            st.dataframe(
                st.session_state.current_df,
                height=500,
                width='stretch'
            )

        with col_right:
            st.caption("왼쪽 행렬을 기반으로 표현된 이미지입니다.")
            
            # 이미지 변환 함수 호출
            pixelated_img, original_size = df_to_image(st.session_state.current_df)
            
            # 이미지 출력
            st.image(
                pixelated_img,
                width='stretch',
                clamp=True # 0-255 범위 준수
            )

    else:
        # 데이터가 없을 때 안내
        st.info("👆 상단의 '픽셀 데이터 업로드'를 열어 엑셀파일(xlxs)을 먼저 업로드해주세요.")

with tab3:
    # ==============================================================================
    # 2. 데이터 업로드 (Expander)
    # ==============================================================================
    Uploaded_df1, Uploaded_df2 = None, None

    with st.expander("📂 픽셀 데이터 2개 업로드 (행렬 A, B)", expanded=True):
        col_up1, col_up2 = st.columns(2)
        with col_up1:
            file1 = st.file_uploader("행렬 A (엑셀 파일)", type=['xlsx'], key="file1")
        with col_up2:
            file2 = st.file_uploader("행렬 B (엑셀 파일)", type=['xlsx'], key="file2")

    if file1 and file2:
        Uploaded_df1 = load_excel_data(file1)
        Uploaded_df2 = load_excel_data(file2)
        
        # 크기 검증
        if Uploaded_df1.shape != Uploaded_df2.shape:
            st.error(f"⚠️ 두 행렬의 크기가 다릅니다! (A: {Uploaded_df1.shape}, B: {Uploaded_df2.shape})")
        else:
            A_col, B_col = st.columns(2)
            with A_col:
                st.markdown("#### 🅰️ 행렬 A")
                st.dataframe(Uploaded_df1, height=300, width='stretch')
            with B_col:
                st.markdown("#### 🅱️ 행렬 B")
                st.dataframe(Uploaded_df2, height=300, width='stretch')

            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                with st.container(horizontal=True):
                    scalar1 = st.number_input(
                        "행렬 A의 실수배 (k₁)", 
                        min_value=0.0,
                        value=1.0, 
                        step=0.1, 
                        format="%.1f",
                        key="scalar1"
                    )

                    operation = st.selectbox(
                        "연산", 
                        ("➕", "➖"), 
                        
                    )

                    scalar2 = st.number_input(
                        "행렬 B의 실수배 (k₂)", 
                        value=1.0, 
                        min_value=0.0,
                        step=0.1, 
                        format="%.1f", 
                        key="scalar2"
                    )

            with btn_col2:
                st.space()
                with st.container(horizontal=True):
                    if st.button("🔄 결과 초기화",width='stretch'):
                        st.session_state.final_result = None
                        st.rerun()

                    if st.button("🚀 계산 실행: (k₁ × A) " + operation + " (k₂ × B)", type="primary", width='stretch'):            
                        # 1. 실수배 적용
                        term1 = Uploaded_df1 * scalar1
                        term2 = Uploaded_df2 * scalar2
                        
                        # 2. 덧셈/뺄셈 연산
                        if operation == "➕":
                            res_df = term1 + term2
                        else:
                            res_df = term1 - term2
                            
                        # 3. 데이터 보정 (0~255 클리핑 & 정수 변환)
                        res_df = res_df.fillna(0) # NaN 방지
                        res_df = res_df.clip(0, 255)
                        res_df = np.round(res_df, 0).astype(int)
                        
                        # 4. 결과 저장
                        st.session_state.final_result = res_df
                        st.rerun()

            # ==============================================================================
            # 4. 결과 확인 (하단)
            # ==============================================================================

            if "final_result" in st.session_state and st.session_state.final_result is not None:
                result_col1, result_col2 = st.columns(2)
                
                # [결과 데이터프레임]
                with result_col1:
                    st.markdown("#### 결과 행렬")
                    st.dataframe(
                        st.session_state.final_result,
                        height=500,
                        width='stretch'
                    )
                    
                # [결과 이미지]
                with result_col2:
                    st.markdown("#### 결과 이미지")
                    
                    # 이미지 변환 (확대 포함)
                    img_res, orig_size = df_to_image(st.session_state.final_result)
                    
                    st.image(
                        img_res,
                        caption=f"Result Image ({orig_size[0]}x{orig_size[1]})",
                        width='stretch',
                        clamp=True
                    )
                    

    elif Uploaded_df1 is None or Uploaded_df2 is None:
        st.info("👆 위에서 두 개의 엑셀 파일(xlxs)을 모두 업로드해주세요.")

    with st.container(horizontal=True):
        st.space("stretch")
        st.page_link("https://matharticle.streamlit.app/Dissolve", label="디졸브 효과", icon="🔀", width="content")

with tab4:
    st.text("평행 이동 및 방향 변환 제작 예정...")
