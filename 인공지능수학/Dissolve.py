import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import io # 이미지를 바이트 형태로 변환하여 다운로드하기 위해 필요
import time

    @st.cache_data(show_spinner=False, ttl=300)
    def get_image_arrays(name1, size1, name2, size2, _bytes1, _bytes2, target_w, target_h):
        # 바이트 -> 이미지 -> 리사이즈 -> 배열 변환
        img1 = Image.open(io.BytesIO(_bytes1)).convert('RGB').resize((target_w, target_h))
        img2 = Image.open(io.BytesIO(_bytes2)).convert('RGB').resize((target_w, target_h))
        
        # 0.0 ~ 1.0 범위의 실수형 배열로 변환
        arr1 = np.array(img1, dtype=float) / 255.0
        arr2 = np.array(img2, dtype=float) / 255.0
        
        return arr1, arr2

    # 세션 상태 초기화
    if 'animation_running' not in st.session_state:
        st.session_state.animation_running = False
    if 'current_alpha' not in st.session_state:
        st.session_state.current_alpha = 0.0

    # 이미지 업로드
    with st.expander("📂 이미지 업로드 열기/닫기", expanded=True):
        col_up1, col_up2 = st.columns(2)
        with col_up1:
            file1 = st.file_uploader("첫 번째 이미지", type=["png", "jpg", "jpeg"], key="img1")
        with col_up2:
            file2 = st.file_uploader("두 번째 이미지", type=["png", "jpg", "jpeg"], key="img2")

    if file1 and file2:
        # 서버 부하 방지를 위한 해상도 계산 (최대 800px)
        temp_img = Image.open(file1)
        orig_w, orig_h = temp_img.size
        default_w = 800 if orig_w > 800 else orig_w
        default_h = int(orig_h * (default_w / orig_w))

        # 메인 레이아웃 (3열)
        col1, col2, col3 = st.columns([0.25, 0.5, 0.25])
        with col1:
            st.subheader("⚙️ 설정 및 제어")
            st.caption("해상도 설정")
            
            wcol1, wcol2 = st.columns(2)
            with wcol1:
                target_w = st.number_input("가로", min_value=10,max_value=800, value=default_w,step=10)
            with wcol2:
                target_h = st.number_input("세로", min_value=10, value=default_h, step=10)
            
            auto_mode = st.toggle("자동 실행 여부", value=False)            
            if auto_mode:
                st.caption("디졸브 효과 제어 (자동)")

                # 재생 버튼
                if st.button("⏯️ 재생/일시정지", type="primary", use_container_width=True):
                    st.session_state.animation_running = not st.session_state.animation_running
                    
                    # 재생 시작 시, 알파값이 끝에 있다면 리셋
                    if st.session_state.animation_running and st.session_state.current_alpha >= 1.0:
                        st.session_state.current_alpha = 0.0

                # 상태 표시
                if st.session_state.animation_running:
                    st.success(f"🟢 재생 중...  가중치 {st.session_state.current_alpha:.2f}")
                else:
                    st.info("⏸️ 대기 중")

                # 알파값 설정: 세션 상태값 사용
                alpha = st.session_state.current_alpha
         
            else:
                st.session_state.animation_running = False 
                
                st.caption("디졸브 효과 제어 (수동)")

                # 슬라이더 표시
                manual_alpha = st.slider(
                    "가중치 (Alpha)",
                    min_value=0.0,
                    max_value=1.0,
                    value=st.session_state.current_alpha, # 현재 상태값 유지
                    step=0.01,
                    key="slider_val"
                )

                # 알파값 설정: 슬라이더 값 사용
                alpha = manual_alpha
                
                # 수동 조작 시 세션 상태도 동기화 (나중에 자동 모드 전환 시 부드럽게 이어지도록)
                st.session_state.current_alpha = manual_alpha

        # ---------------------------------------------------------
        # [데이터 처리] 캐시 함수 호출
        # ---------------------------------------------------------
        arr1, arr2 = get_image_arrays(
            file1.name, file1.size,
            file2.name, file2.size,
            file1.getvalue(),
            file2.getvalue(),
            target_w, target_h
        )

        # ---------------------------------------------------------
        # [2열] 결과 및 애니메이션
        # ---------------------------------------------------------
        with col2:
            st.subheader("✨ 결과")

            # 블렌딩 연산
            blended = (arr1 * (1 - alpha)) + (arr2 * alpha)
            
            # 결과 출력
            st.image(
                blended, 
                use_container_width=False,
                clamp=True 
            )

            # 알파값이 0이면 첫번째 사진이 잘보이도록 초 정지
            if alpha == 0.0:
                time.sleep(1)

            # 애니메이션 루프 (자동 모드이고, 재생 중일 때만 실행)
            if auto_mode and st.session_state.animation_running:
                time.sleep(0.4) # 속도 조절
                
                st.session_state.current_alpha += 0.05
                
                # 종료 조건
                if st.session_state.current_alpha > 1.0:
                    st.session_state.current_alpha = 1.0
                    st.session_state.animation_running = False # 종료 시 정지
                
                st.rerun() # 화면 갱신

        # ---------------------------------------------------------
        # [3열] 원본 이미지
        # ---------------------------------------------------------
        with col3:
            st.subheader("소스")
            st.image(arr1, use_container_width=False, clamp=True)
            st.image(arr2, use_container_width=False, clamp=True)

    else:
        st.info("👆 상단의 '이미지 업로드'를 열어 두 개의 이미지를 넣어주세요.")            
