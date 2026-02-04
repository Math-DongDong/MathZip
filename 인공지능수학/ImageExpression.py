import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import io # 이미지를 바이트 형태로 변환하여 다운로드하기 위해 필요

# --- 앱 제목 ---
st.title("이미지 데이터의 표현")

# 탭 생성
tab1, tab2, tab3 = st.tabs(["🖼️ 이미지 해상도", "흑백이미지의 표현", "컬러이미지의 표현"])
# ==============================================================================
# [TAB 1] 이미지 해상도
# ==============================================================================
with tab1:
    # 1. 이미지 업로드 기능
    uploaded_file = st.file_uploader("이미지 파일을 업로드하세요.", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # 업로드된 파일을 PIL 이미지 객체로 변환
        image = Image.open(uploaded_file)
        
        # 원본 이미지 정보 가져오기
        original_width, original_height = image.size

        # 2. 해상도 조절 UI 및 이미지 처리
        edit, original, result = st.columns([0.2,0.4, 0.4])
        with edit:
            st.subheader("해상도 설정")
            # 가로 길이 입력 (기본값: 원본 크기)
            new_width = st.number_input(
                "가로(Width) 픽셀", 
                min_value=1, 
                value=original_width, 
                step=1
            )
            # 세로 길이 입력 (기본값: 원본 크기)
            new_height = st.number_input(
                "세로(Height) 픽셀", 
                min_value=1, 
                value=original_height, 
                step=1
            )

            # 핵심 변경사항 1: NEAREST 필터 사용
            # LANCZOS 대신 NEAREST를 사용하여 색상을 섞지 않고 픽셀을 그대로 가져옵니다. (계단 현상 생성)
            pixelated_image = image.resize((new_width, new_height), Image.Resampling.NEAREST)
            
            # 핵심 변경사항 2: 화면 표시용 재확대
            # 줄어든 이미지를 그대로 보여주면 너무 작아서 픽셀 느낌이 안 납니다.
            # 원본 크기(혹은 적당한 크기)로 다시 뻥튀기하되, NEAREST를 써서 각진 느낌을 유지합니다.
            preview_image = pixelated_image.resize((original_width, original_height), Image.Resampling.NEAREST)
            # -------------------------------------------------------------------
            
            # 4. 다운로드 버튼 생성 logic
            # 사용자가 다운로드하는 것은 설정한 크기(작은 파일)입니다.
            buf = io.BytesIO()

            # 원본 포맷 유지 (JPEG인 경우 포맷 명시 필요)
            img_format = image.format if image.format else "PNG"
            
            # 실제 저장되는 파일은 줄어든 크기의 이미지 (pixelated_image)
            pixelated_image.save(buf, format=img_format)
            byte_im = buf.getvalue()

            st.download_button(
                label="💾 변환된 이미지 다운로드",
                data=byte_im,
                file_name=f"pixelated_{uploaded_file.name}",
                mime=f"image/{img_format.lower()}"
            )

        with original:
            st.subheader("원본 이미지")
            st.image(image, caption=f"원본: {original_width} x {original_height} px", use_container_width=True)

        with result:
            st.subheader("변환 이미지")
            # 결과 이미지 표시 (미리보기용 확대 이미지 사용)
            # caption에는 실제 파일 크기를 표시
            st.image(preview_image, caption=f"변경됨: {new_width} x {new_height} px", use_container_width=True)
                
    else:
        st.info("👆 위 영역에서 이미지 파일( png, jpg, jpeg )을 먼저 업로드해주세요.")

# ==============================================================================
# [TAB 2] 흑백 이미지 (HTML/JS 전용 버전)
# ==============================================================================
with tab2:
    # 파이썬 개입 없이 아이프레임 내부에서 완결되는 HTML 코드입니다.
    html_code = """

    """

    # HTML 컴포넌트 렌더링
    components.html(html_code, height=800, scrolling=False)    
with tab3:
    st.markdown("컬러이미지의 표현")
