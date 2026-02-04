import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import io # 이미지를 바이트 형태로 변환하여 다운로드하기 위해 필요

# --- 앱 제목 ---
st.title("이미지 자료의 표현 방법")

# 탭 생성
tab1, tab2 = st.tabs(["🖼️ 이미지 해상도 조절기", "흑백이미지의 표현"])
with tab1:
    # 1. 이미지 업로드 기능
    uploaded_file = st.file_uploader("이미지 파일을 업로드하세요.", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # 업로드된 파일을 PIL 이미지 객체로 변환
        image = Image.open(uploaded_file)
        
        # 원본 이미지 정보 가져오기
        original_width, original_height = image.size


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

            # 이미지 리사이징 (LANCZOS 필터 사용: 고품질 리사이징 알고리즘)
            resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 4. 다운로드 버튼 생성 logic
            # 이미지를 메모리 버퍼(RAM)에 저장하여 다운로드 가능한 형태로 변환
            buf = io.BytesIO()
        
            # 원본 포맷 유지 (JPEG인 경우 포맷 명시 필요)
            img_format = image.format if image.format else "PNG"
            resized_image.save(buf, format=img_format)
            byte_im = buf.getvalue()

            st.download_button(
                label="💾 변환된 이미지 다운로드",
                data=byte_im,
                file_name=f"resized_{uploaded_file.name}",
                mime=f"image/{img_format.lower()}"
            )

        with original:
            st.subheader("원본 이미지")
            st.image(image, caption=f"원본: {original_width} x {original_height} px", use_container_width=True)

        with result:
                
            st.subheader("변환 이미지")
            
            # 결과 이미지 표시
            st.image(resized_image, caption=f"변경됨: {new_width} x {new_height} px", use_container_width=True)
                
            
    else:
        st.info("👆 위 영역에서 이미지 파일( png, jpg, jpeg )을 먼저 업로드해주세요.")

with tab2:
    st.markdown("흑백이미지의 표현")
