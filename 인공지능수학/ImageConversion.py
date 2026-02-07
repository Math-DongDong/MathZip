import streamlit as st
import numpy as np
import pandas as pd
import streamlit.components.v1 as components
from PIL import Image
import io # 이미지를 바이트 형태로 변환하여 다운로드하기 위해 필요
import time

# --- 앱 제목 ---
st.title("이미지 데이터의 변환")

# 탭 생성
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔘 그레이 필터", "💡 밝기 조절", "➕ 합성" , "↔️ 평행이동 및 방향 변환"," 🔀 디졸브 효과"])

# ==============================================================================
# [TAB 1] 그레이 필터
# ==============================================================================
with tab1:
    st.markdown("""
    <style>
    // 표의 머릿글과 왼쪽 기준 제거
    .e15vb32f5 {
                display: none;
    }
                
    .block-container {
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

    # ==============================================================================
    # 1. 이미지 업로드
    # ==============================================================================
    with st.expander("📂 이미지 업로드 열기/닫기", expanded=True):
        uploaded_file = st.file_uploader("이미지 파일을 업로드하세요 (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # 이미지 열기 및 RGB 변환
        image_pil = Image.open(uploaded_file).convert('RGB')
        original_width, original_height = image_pil.size

        col_set, col_orig, col_res = st.columns([0.2, 0.4, 0.4], gap="medium")

        # --------------------------------------------------------------------------
        # [1열] 해상도 설정 및 엑셀 다운로드
        # --------------------------------------------------------------------------
        with col_set:
            st.subheader("⚙️ 해상도 설정")
            
            st.caption("해상도 조절")
            # 가로 길이 입력 (기본값: 원본)
            new_width = st.number_input(
                "가로(Width) 픽셀", 
                min_value=1, 
                value=original_width, 
                step=10
            )
            # 세로 길이 입력 (기본값: 원본)
            new_height = st.number_input(
                "세로(Height) 픽셀", 
                min_value=1, 
                value=original_height, 
                step=10
            )
            
            st.info(f"변환 크기: {new_width} x {new_height}")

            # --- 이미지 처리 로직 (설정값 기반) ---
            # 1. 리사이징 
            resized_pil = image_pil.resize((new_width, new_height), Image.Resampling.NEAREST)
            resized_arr = np.array(resized_pil)

            # 2. 그레이스케일 변환 (단순 평균법)
            # axis=2 : R,G,B 채널의 평균을 구함 -> (H, W) 크기의 2차원 배열 생성
            gray_matrix = np.mean(resized_arr, axis=2).astype(np.uint8)

            # 3. 시각화용 3채널 변환 (R=G=B)
            # (H, W) -> (H, W, 3)
            gray_display_arr = np.stack((gray_matrix, gray_matrix, gray_matrix), axis=2)
            gray_display_pil = Image.fromarray(gray_display_arr)

            st.divider()

            # --- 엑셀 다운로드 로직 ---
            st.caption("💾 데이터 다운로드")
            
            # 엑셀 파일 생성 (메모리 내)
            output = io.BytesIO()
            
            # Pandas를 이용해 2차원 배열(gray_matrix)을 데이터프레임으로 변환
            df_gray = pd.DataFrame(gray_matrix)
            
            # 엑셀 쓰기 (인덱스와 헤더는 제거하여 순수 숫자만 저장)
            # 용량이 클 수 있으므로 Spinner 표시
            with st.spinner("엑셀 파일 생성 중..."):
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df_gray.to_excel(writer, index=False, header=False, sheet_name='Pixel_Data')
                
                excel_data = output.getvalue()

            # 다운로드 버튼
            st.download_button(
                label="📥 픽셀 데이터(Excel) 받기",
                data=excel_data,
                file_name=f"gray_matrix_{new_width}x{new_height}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            st.caption("※ 해상도가 높으면 다운로드에 시간이 걸릴 수 있습니다.")

        # --------------------------------------------------------------------------
        # [2열] 원본 이미지
        # --------------------------------------------------------------------------
        with col_orig:
            st.subheader("원본 이미지")
            st.image(
                image_pil, 
                caption=f"Original: {original_width} x {original_height} px", 
                use_container_width=True
            )

        # --------------------------------------------------------------------------
        # [3열] 결과 (그레이스케일) 이미지
        # --------------------------------------------------------------------------
        with col_res:
            st.subheader("그레이 필터 적용")
            st.image(
                gray_display_pil, 
                caption=f"Grayscale: {new_width} x {new_height} px", 
                use_container_width=True
            )

    else:
        st.info("👆 상단의 '이미지 업로드'를 열어 이미지 파일( png, jpg, jpeg )을 먼저 업로드해주세요.")            
# ==============================================================================
# [TAB 2] 밝기 조절
# ==============================================================================
with tab2:
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
            st.image(image, caption=f"원본: {original_width} x {original_height} px", width='stretch')

        with result:
            st.subheader("변환 이미지")
            # 결과 이미지 표시 (미리보기용 확대 이미지 사용)
            # caption에는 실제 파일 크기를 표시
            st.image(preview_image, caption=f"변경됨: {new_width} x {new_height} px", width='stretch')
                
    else:
        st.info("👆 위 영역에서 이미지 파일( png, jpg, jpeg )을 먼저 업로드해주세요.")



with tab3:
    html_code2 = """
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <script src="https://cdn.tailwindcss.com"></script>
            <style>
                /* 숫자 입력 화살표 제거 */
                input[type=number]::-webkit-inner-spin-button, 
                input[type=number]::-webkit-outer-spin-button { 
                    -webkit-appearance: none; 
                    margin: 0; 
                }
            </style>
        </head>
        <body class="bg-white font-sans text-gray-800">

            <div class="w-full px-4 py-6">
                
                <!-- 컨트롤 패널 -->
                <div class="flex flex-col items-center mb-8">
                    
                    <!-- 설정 박스 -->
                    <div class="flex flex-col md:flex-row items-start md:items-center gap-4 p-4 w-full">
                        <!-- 왼쪽 그룹: 크기 입력 + 초기화 -->
                        <div class="flex flex-wrap items-center gap-2 w-full md:w-auto">
                            <div class="flex items-center gap-2">
                                <label class="text-sm font-medium text-gray-600">가로 픽셀</label>
                                <input type="number" id="cols" value="4" min="1" max="11" class="w-12 p-2 border border-gray-300 rounded text-center focus:outline-none focus:border-blue-500 text-sm">
                            </div>
                            <div class="flex items-center gap-2">
                                <label class="text-sm font-medium text-gray-600">세로 픽셀</label>
                                <input type="number" id="rows" value="4" min="1" max="11" class="w-12 p-2 border border-gray-300 rounded text-center focus:outline-none focus:border-blue-500 text-sm">
                            </div>

                            <button id="create-btn" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-5 rounded text-sm shadow transition-colors">
                                새로 만들기
                            </button>
                        </div>

                        <!-- spacer to push the right-group to the far right -->
                        <div class="hidden md:flex flex-1"></div>

                        <!-- 오른쪽 그룹: 클릭값 + 이미지 변환 -->
                        <div class="flex items-center gap-2 w-full md:w-auto">
                            <div class="flex items-center gap-2 bg-purple-50 px-3 py-1.5 rounded border border-purple-100">
                                <span class="text-lg">🖌️</span>
                                <label class="text-sm font-bold text-purple-700">클릭 값</label>
                                <input type="number" id="paint-val" value="255" min="0" max="255" class="w-14 p-2 border border-purple-300 rounded text-center text-purple-700 font-bold focus:outline-none focus:ring-2 focus:ring-purple-500 text-sm" title="칸을 클릭할 때 이 값이 입력됩니다.">
                            </div>

                            <button id="merge-btn" class="bg-gray-800 hover:bg-black text-white text-sm font-bold py-2 px-4 rounded-lg shadow-lg transform transition active:scale-95 whitespace-nowrap">
                                이미지 변환
                            </button>
                        </div>
                    </div>
                </div>

                <!-- 메인 워크스페이스 -->
                <div class="flex flex-col sm:flex-row items-start gap-6 lg:gap-10">
                    
                    <!-- [입력 영역] -->
                    <div class="flex flex-col sm:flex-row gap-6">
                        
                        <!-- Red Channel -->
                        <div class="flex flex-col items-center group w-full sm:w-auto">
                            <div class="text-red-600 font-bold mb-2 text-sm bg-red-50 px-3 py-1 rounded border border-red-100">R (Red)</div>
                            <div id="container-r" class="border-2 border-red-100 rounded p-1 bg-white shadow-sm group-hover:border-red-300 transition-colors"></div>
                        </div>

                        <!-- Green Channel -->
                        <div class="flex flex-col items-center group w-full sm:w-auto">
                            <div class="text-green-600 font-bold mb-2 text-sm bg-green-50 px-3 py-1 rounded border border-green-100">G (Green)</div>
                            <div id="container-g" class="border-2 border-green-100 rounded p-1 bg-white shadow-sm group-hover:border-green-300 transition-colors"></div>
                        </div>

                        <!-- Blue Channel -->
                        <div class="flex flex-col items-center group w-full sm:w-auto">
                            <div class="text-blue-600 font-bold mb-2 text-sm bg-blue-50 px-3 py-1 rounded border border-blue-100">B (Blue)</div>
                            <div id="container-b" class="border-2 border-blue-100 rounded p-1 bg-white shadow-sm group-hover:border-blue-300 transition-colors"></div>
                        </div>
                    </div>

                    <!-- [합성 액션] -->
                    <!-- 제거: 버튼을 상단 컨트롤 박스에 통합하여 동일 행의 우측에 배치함 -->

                    <!-- [결과 영역] -->
                    <div class="flex flex-col items-center">
                        <div class="text-gray-800 font-bold mb-2 text-sm bg-gray-100 px-3 py-1 rounded border border-gray-200">Result (Image)</div>
                        
                        <div id="container-result" class="border border-gray-300 rounded p-1 bg-white shadow-md min-w-[120px] min-h-[120px] flex items-center justify-center relative">
                            <span class="text-xs text-gray-400">결과 대기 중</span>
                        </div>
                        
                        <!-- 안내 문구 (요청사항 반영) -->
                        <div class="mt-3 text-center">

                            <div id="pixel-info" class="text-xs font-bold mt-2 h-4 text-gray-700"></div>
                        </div>
                    </div>

                </div>
            </div>

            <script>
                document.addEventListener('DOMContentLoaded', () => {
                    const rowsInput = document.getElementById('rows');
                    const colsInput = document.getElementById('cols');
                    const paintValInput = document.getElementById('paint-val'); // 브러시 값 입력창
                    
                    const createBtn = document.getElementById('create-btn');
                    const mergeBtn = document.getElementById('merge-btn');
                    
                    const containerR = document.getElementById('container-r');
                    const containerG = document.getElementById('container-g');
                    const containerB = document.getElementById('container-b');
                    const containerResult = document.getElementById('container-result');
                    const pixelInfo = document.getElementById('pixel-info');

                    // 초기 실행
                    createAllGrids();

                    createBtn.addEventListener('click', createAllGrids);
                    mergeBtn.addEventListener('click', updateResultImage);

                    // 브러시 값 범위 체크
                    paintValInput.addEventListener('change', function() {
                        let val = parseInt(this.value);
                        if (val < 0) this.value = 0;
                        if (val > 255) this.value = 255;
                    });

                    function createAllGrids() {
                        const rows = parseInt(rowsInput.value, 10);
                        const cols = parseInt(colsInput.value, 10);

                        if (rows > 11 || cols > 11) {
                            alert('가로와 세로 픽셀은 최대 11까지만 가능합니다.');
                            return;
                        }
                        if (rows < 1 || cols < 1) {
                            alert('1부터 11까지의 자연수를 입력해주세요.');
                            return;
                        }

                        // 입력 테이블 생성 (초기값 0으로 통일하여 깔끔하게 시작)
                        createInputTable(containerR, rows, cols, 'red');
                        createInputTable(containerG, rows, cols, 'green');
                        createInputTable(containerB, rows, cols, 'blue');

                        // 결과창 초기화
                        containerResult.innerHTML = '';
                        createResultPlaceholder(rows, cols);
                        pixelInfo.innerText = '';
                    }

                    function createInputTable(container, rows, cols, colorTheme) {
                        container.innerHTML = '';
                        const table = document.createElement('table');
                        table.className = 'border-collapse';
                        // Make table responsive: width fills container and uses fixed layout
                        table.style.width = '100%';
                        table.style.tableLayout = 'fixed';

                        let inputStyleClass = '';
                        if (colorTheme === 'red') inputStyleClass = 'focus:border-red-500 text-red-700 selection:bg-red-200';
                        else if (colorTheme === 'green') inputStyleClass = 'focus:border-green-500 text-green-700 selection:bg-green-200';
                        else if (colorTheme === 'blue') inputStyleClass = 'focus:border-blue-500 text-blue-700 selection:bg-blue-200';

                        for (let r = 0; r < rows; r++) {
                            const tr = document.createElement('tr');
                            for (let c = 0; c < cols; c++) {
                                const td = document.createElement('td');
                                td.className = 'border border-gray-200 p-0.5';
                                td.style.width = `calc(100% / ${cols})`;

                                // Create a square container using the padding-top trick so height follows width
                                const square = document.createElement('div');
                                square.style.position = 'relative';
                                square.style.width = '100%';
                                square.style.paddingTop = '100%';

                                const input = document.createElement('input');
                                input.type = 'number';
                                input.min = 0;
                                input.max = 255;
                                input.placeholder = "0"; // 빈 칸일 때 0처럼 보이게 힌트
                                // absolutely position the input to fill the square
                                input.style.position = 'absolute';
                                input.style.top = '0';
                                input.style.left = '0';
                                input.style.width = '100%';
                                input.style.height = '100%';
                                input.style.boxSizing = 'border-box';
                                input.className = `text-center text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-opacity-50 font-mono transition-all ${inputStyleClass}`;
                                
                                // [핵심 기능] 클릭 시 '클릭 값'으로 자동 채우기
                                input.addEventListener('click', function() {
                                    const brushValue = paintValInput.value;
                                    // 값이 비어있거나 다를 때만 변경 (사용자 경험 고려)
                                    // 혹은 무조건 변경을 원하면 조건문 제거 가능. 여기선 무조건 변경.
                                    this.value = brushValue;
                                    
                                    // 클릭할 때 시각적 피드백 (반짝임)
                                    this.classList.add('bg-gray-100');
                                    setTimeout(() => this.classList.remove('bg-gray-100'), 150);
                                });

                                // 수동 입력 시 범위 제한
                                input.addEventListener('input', function() {
                                    if (this.value === '') return;
                                    let val = parseInt(this.value);
                                    if (val < 0) this.value = 0;
                                    if (val > 255) this.value = 255;
                                });

                                square.appendChild(input);
                                td.appendChild(square);
                                tr.appendChild(td);
                            }
                            table.appendChild(tr);
                        }
                        container.appendChild(table);
                    }

                    function createResultPlaceholder(rows, cols) {
                        const table = document.createElement('table');
                        table.className = 'border-collapse';
                        table.style.width = '100%';
                        table.style.tableLayout = 'fixed';
                        for (let r = 0; r < rows; r++) {
                            const tr = document.createElement('tr');
                            for (let c = 0; c < cols; c++) {
                                const td = document.createElement('td');
                                td.className = 'border border-gray-300 bg-gray-50 p-0'; 
                                td.style.width = `calc(100% / ${cols})`;
                                const square = document.createElement('div');
                                square.style.position = 'relative';
                                square.style.width = '100%';
                                square.style.paddingTop = '100%';

                                const inner = document.createElement('div');
                                inner.style.position = 'absolute';
                                inner.style.top = '0';
                                inner.style.left = '0';
                                inner.style.width = '100%';
                                inner.style.height = '100%';
                                inner.className = 'bg-gray-50';
                                square.appendChild(inner);
                                td.appendChild(square);
                                tr.appendChild(td);
                            }
                            table.appendChild(tr);
                        }
                        containerResult.appendChild(table);
                    }

                    function updateResultImage() {
                        const rows = parseInt(rowsInput.value);
                        const cols = parseInt(colsInput.value);

                        const inputsR = containerR.querySelectorAll('input');
                        const inputsG = containerG.querySelectorAll('input');
                        const inputsB = containerB.querySelectorAll('input');

                        containerResult.innerHTML = '';
                        const table = document.createElement('table');
                        table.className = 'border-collapse cursor-crosshair'; 
                        table.style.width = '100%';
                        table.style.tableLayout = 'fixed';

                        let index = 0;
                        for (let r = 0; r < rows; r++) {
                            const tr = document.createElement('tr');
                            for (let c = 0; c < cols; c++) {
                                const td = document.createElement('td');
                                
                                // 값이 비어있으면 0으로 처리 (|| 0)
                                const rVal = inputsR[index].value === '' ? 0 : parseInt(inputsR[index].value);
                                const gVal = inputsG[index].value === '' ? 0 : parseInt(inputsG[index].value);
                                const bVal = inputsB[index].value === '' ? 0 : parseInt(inputsB[index].value);

                                td.className = 'border border-gray-300 transition-colors duration-300 p-0';
                                td.style.width = `calc(100% / ${cols})`;

                                const square = document.createElement('div');
                                square.style.position = 'relative';
                                square.style.width = '100%';
                                square.style.paddingTop = '100%';

                                const inner = document.createElement('div');
                                inner.style.position = 'absolute';
                                inner.style.top = '0';
                                inner.style.left = '0';
                                inner.style.width = '100%';
                                inner.style.height = '100%';
                                inner.style.backgroundColor = `rgb(${rVal}, ${gVal}, ${bVal})`;
                                inner.dataset.rgb = `RGB(${rVal}, ${gVal}, ${bVal})`;
                                inner.addEventListener('mouseover', function() {
                                    pixelInfo.textContent = this.dataset.rgb;
                                    pixelInfo.style.color = 'black'; 
                                });

                                square.appendChild(inner);
                                td.appendChild(square);
                                tr.appendChild(td);
                                index++;
                            }
                            table.appendChild(tr);
                        }
                        containerResult.appendChild(table);
                        pixelInfo.textContent = "마우스를 올리면 픽셀의 RGB 값 확인 가능";
                    }
                });
            </script>
        </body>
        </html>
    """
    
    # HTML 컴포넌트 렌더링
    components.html(html_code2, height=800, scrolling=True)    
with tab4:
    st.text("평행")

with tab5:
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
