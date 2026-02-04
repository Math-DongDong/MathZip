import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import io # 이미지를 바이트 형태로 변환하여 다운로드하기 위해 필요

# --- 앱 제목 ---
st.title("이미지 데이터의 표현")

# 탭 생성
tab1, tab2, tab3, tab4 = st.tabs(["🖼️ 이미지 해상도", "흑백 이미지", "명암 표현" , "컬러 이미지"])
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
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="bg-white font-sans text-gray-800">

            <!-- 
                메인 컨테이너 
                - w-full: 부모(body) 너비에 맞게 100% 사용
                - px-4: 모바일에서 내용이 화면 끝에 붙지 않도록 최소한의 좌우 여백만 줌
                - max-w-none: 너비 제한 제거
                - shadow/rounded 제거: 배경이 흰색이므로 카드 스타일 제거
            -->
            <div class="w-full px-4 py-6">
                
                <!-- 그리드 레이아웃 -->
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 items-start">
                    
                    <!-- [왼쪽] 입력 섹션 -->
                    <div class="flex flex-col w-full">
                        <!-- 헤더 -->
                        <div class="mb-2 flex items-center gap-2">
                            <span class="bg-blue-100 text-blue-800 text-xs font-bold px-2 py-1 rounded">Step 1</span> 
                            <span class="font-bold text-gray-700">그림 그리기</span>
                        </div>

                        <!-- 컨트롤 패널 (회색 박스) -->
                        <div class="flex flex-wrap items-center gap-3 mb-4 p-3 bg-gray-50 border border-gray-200 rounded">
                            <div class="flex items-center gap-2">
                                <label class="text-sm font-medium text-gray-600">가로 픽셀</label>
                                <input type="number" id="cols" value="7" min="1" max="10" class="w-12 p-1 border border-gray-300 rounded text-center focus:outline-none focus:border-blue-500 text-sm">
                            </div>
                            <div class="flex items-center gap-2">
                                <label class="text-sm font-medium text-gray-600">세로 픽셀</label>
                                <input type="number" id="rows" value="7" min="1" max="10" class="w-12 p-1 border border-gray-300 rounded text-center focus:outline-none focus:border-blue-500 text-sm">
                            </div>
                            <button id="create-btn" class="ml-auto bg-blue-600 hover:bg-blue-700 text-white font-bold py-1.5 px-3 rounded text-sm whitespace-nowrap">
                                표 만들기
                            </button>
                        </div>

                        <!-- 입력 그리드 영역 -->
                        <div id="grid-container" class="flex justify-center p-4 border border-dashed border-gray-300 rounded">
                            <!-- JS로 생성됨 -->
                        </div>
                    </div>

                    <!-- [오른쪽] 결과 섹션 -->
                    <div class="flex flex-col w-full h-full">
                        <!-- 헤더 -->
                        <div class="mb-2 flex items-center gap-2">
                            <span class="bg-green-100 text-green-800 text-xs font-bold px-2 py-1 rounded">Step 2</span>
                            <span class="font-bold text-gray-700">행렬 표현</span>
                        </div>

                        <!-- 버튼 영역 (왼쪽 컨트롤 패널과 높이 맞춤) -->
                        <div class="flex items-center mb-4 p-3 h-[58px] sm:h-auto border border-transparent"> 
                            <button id="show-matrix-btn" class="w-full bg-gray-800 hover:bg-gray-900 text-white font-bold py-1.5 px-4 rounded text-sm flex items-center justify-center gap-2">
                                행렬 변환 결과 보기
                            </button>
                        </div>

                        <!-- 결과 표시 영역 (회색 박스) -->
                        <!-- h-full과 min-h 설정으로 왼쪽 그리드 영역과 균형 맞춤 -->
                        <div class="w-full flex flex-col items-center justify-center bg-gray-50 border border-gray-200 rounded p-4 min-h-[300px] lg:h-[calc(100%-74px)]">
                            
                            <!-- 결과 테이블 래퍼 -->
                            <div id="matrix-output" class="hidden flex flex-col items-center animate-fade-in w-full overflow-x-auto">
                                <div id="matrix-table-wrapper" class="p-2 bg-white rounded border border-gray-200 inline-block">
                                    <!-- 결과 테이블 생성 위치 -->
                                </div>
                            </div>

                            <!-- 안내 문구 -->
                            <div id="placeholder-text" class="text-gray-400 text-sm text-center">
                                버튼을 누르면 행렬이 표시됩니다.
                            </div>
                        </div>
                    </div>

                </div> 
            </div>

            <script>
                document.addEventListener('DOMContentLoaded', () => {
                    const rowsInput = document.getElementById('rows');
                    const colsInput = document.getElementById('cols');
                    const createBtn = document.getElementById('create-btn');
                    const showMatrixBtn = document.getElementById('show-matrix-btn');
                    const gridContainer = document.getElementById('grid-container');
                    
                    const outputContainer = document.getElementById('matrix-output');
                    const outputWrapper = document.getElementById('matrix-table-wrapper');
                    const placeholderText = document.getElementById('placeholder-text');
                    
                    const blackCellClass = 'bg-gray-800';

                    function createGrid() {
                        const rows = parseInt(rowsInput.value, 10);
                        const cols = parseInt(colsInput.value, 10);

                        if (isNaN(rows) || isNaN(cols) || rows <= 0 || cols <= 0) {
                            alert('1부터 10까지의 자연수를 입력해주세요.');
                            return;
                        }
                        if (rows > 10 || cols > 10) {
                            alert('가로와 세로 픽셀은 최대 10까지만 가능합니다.');
                            return;
                        }

                        gridContainer.innerHTML = '';
                        outputContainer.classList.add('hidden'); 
                        placeholderText.style.display = 'block';
                        outputWrapper.innerHTML = '';

                        const table = document.createElement('table');
                        table.className = 'border-collapse shadow-sm bg-white select-none';
                        
                        for (let r = 0; r < rows; r++) {
                            const tr = document.createElement('tr');
                            for (let c = 0; c < cols; c++) {
                                const td = document.createElement('td');
                                td.className = 'w-10 h-10 sm:w-12 sm:h-12 border border-gray-300 cursor-pointer hover:bg-gray-100 transition-colors duration-100';
                                tr.appendChild(td);
                            }
                            table.appendChild(tr);
                        }
                        gridContainer.appendChild(table);
                    }

                    function showMatrix() {
                        const sourceTable = gridContainer.querySelector('table');
                        if (!sourceTable) {
                            alert("먼저 표를 만들어주세요.");
                            return;
                        }

                        outputWrapper.innerHTML = '';
                        outputContainer.classList.remove('hidden');
                        placeholderText.style.display = 'none';

                        const resultTable = document.createElement('table');
                        resultTable.className = 'border-collapse border border-gray-300';

                        for (let r = 0; r < sourceTable.rows.length; r++) {
                            const resultTr = document.createElement('tr');
                            
                            for (let c = 0; c < sourceTable.rows[r].cells.length; c++) {
                                const sourceCell = sourceTable.rows[r].cells[c];
                                const isBlack = sourceCell.classList.contains(blackCellClass);
                                const value = isBlack ? 1 : 0;

                                const resultTd = document.createElement('td');
                                resultTd.textContent = value;
                                
                                let cellClass = 'w-8 h-8 text-center border border-gray-200 text-sm font-mono cursor-default ';
                                
                                if (value === 1) {
                                    cellClass += 'bg-gray-200 text-gray-900 font-bold';
                                } else {
                                    cellClass += 'bg-white text-gray-400';
                                }
                                
                                resultTd.className = cellClass;
                                resultTr.appendChild(resultTd);
                            }
                            resultTable.appendChild(resultTr);
                        }

                        outputWrapper.appendChild(resultTable);
                        
                        if (window.innerWidth < 1024) {
                            outputContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                        }
                    }
                    
                    function handleGridClick(e) {
                        if (e.target.tagName === 'TD') {
                            e.target.classList.toggle(blackCellClass);
                        }
                    }

                    createBtn.addEventListener('click', createGrid);
                    showMatrixBtn.addEventListener('click', showMatrix);
                    gridContainer.addEventListener('click', handleGridClick);

                    createGrid();
                });
            </script>
            
            <style>
                @keyframes fadeIn {
                    from { opacity: 0; transform: translateY(-5px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                .animate-fade-in {
                    animation: fadeIn 0.3s ease-out forwards;
                }
            </style>
        </body>
        </html>
    """

    # HTML 컴포넌트 렌더링
    components.html(html_code, height=650, scrolling=False)    
with tab3:
    st.markdown("명암")

with tab4:
    st.markdown("컬러이미지의 표현")
