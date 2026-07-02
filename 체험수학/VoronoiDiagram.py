import streamlit as st
import streamlit.components.v1 as components

st.markdown("<h1 style='text-align: center;'>보로노이 다이어그램</h1>", unsafe_allow_html=True)

HTML='''
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <!-- 모바일 기기 대응을 위한 뷰포트 설정 -->
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>보로노이 & 델로네 다이어그램 웹앱</title>
        
        <!-- Bootstrap 5 CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        
        <style>
            /* 기본 배경은 흰색으로 설정 */
            body {
                background-color: #ffffff;
                font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', sans-serif;
            }

            /* 시각화 영역 컨테이너 스타일 */
            #visualization-container {
                position: relative;
                width: 100%;
                height: 60vh; /* 화면 높이의 60% 사용 */
                min-height: 400px;
                border: 2px dashed #dee2e6;
                border-radius: 0.5rem;
                overflow: hidden;
                background-color: #f8f9fa;
            }

            /* 배경 이미지 스타일 (SVG 뒤에 배치) */
            #bg-image {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                object-fit: cover; /* 이미지가 꽉 차게, 필요시 contain으로 변경 가능 */
                opacity: 0.7; /* 다이어그램이 잘 보이도록 투명도 조절 */
                pointer-events: none; /* 이미지는 클릭 이벤트를 받지 않도록 설정 */
            }

            /* SVG 그리기 영역 (가장 위에 배치) */
            #drawing-area {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 10;
            }

            /* 생성점(Point) 커서 스타일 */
            .point {
                cursor: grab;
            }
            .point:active {
                cursor: grabbing;
            }
        </style>
    </head>
    <body>

    <div class="container py-4">
        <!-- 컨트롤 패널 (Bootstrap Card 사용) -->
        <div class="card mb-4 shadow-sm">
            <div class="card-body">
                <div class="row g-3 align-items-end">
                    <!-- 생성점 수 입력 -->
                    <div class="col-12 col-md-3">
                        <label for="pointCount" class="form-label">생성점 개수</label>
                        <input type="number" class="form-control" id="pointCount" value="15" min="3" max="100">
                    </div>
                    <!-- 생성 버튼 -->
                    <div class="col-12 col-md-2">
                        <button id="generateBtn" class="btn btn-primary w-100">랜덤 생성</button>
                    </div>
                    
                    <!-- 배경 이미지 업로드 -->
                    <div class="col-12 col-md-4">
                        <label for="imageUpload" class="form-label">배경 이미지 첨부 (옵션)</label>
                        <input class="form-control" type="file" id="imageUpload" accept="image/*">
                    </div>

                    <!-- 체크박스 옵션 -->
                    <div class="col-12 col-md-3">
                        <div class="form-check form-switch">
                            <input class="form-check-input" type="checkbox" id="showVoronoi" checked>
                            <label class="form-check-label" for="showVoronoi">보로노이 다이어그램 (빨간선)</label>
                        </div>
                        <div class="form-check form-switch mt-2">
                            <input class="form-check-input" type="checkbox" id="showDelaunay" checked>
                            <label class="form-check-label" for="showDelaunay">델로네 삼각형 (파란선)</label>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 시각화 화면 -->
        <div id="visualization-container" class="shadow-sm">
            <img id="bg-image" src="" alt="" style="display: none;">
            <svg id="drawing-area"></svg>
        </div>
        
        <p class="text-muted mt-2 text-center small">
            * 점을 마우스나 터치로 드래그하여 위치를 자유롭게 이동해 보세요.
        </p>
    </div>

    <!-- Bootstrap 5 JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.css"></script>
    <!-- D3.js 핵심 라이브러리 -->
    <script src="https://d3js.org/d3.v7.min.js"></script>

    <script>
        // ----------------------------------------------------
        // 1. 상태 변수 및 DOM 요소 초기화
        // ----------------------------------------------------
        let points = []; // 생성점 배열: [{x, y}, {x, y}, ...]
        
        const container = document.getElementById('visualization-container');
        const svgElement = document.getElementById('drawing-area');
        const svg = d3.select("#drawing-area");
        
        // UI 컨트롤 요소
        const generateBtn = document.getElementById('generateBtn');
        const pointCountInput = document.getElementById('pointCount');
        const imageUpload = document.getElementById('imageUpload');
        const bgImage = document.getElementById('bg-image');
        const showVoronoiCheckbox = document.getElementById('showVoronoi');
        const showDelaunayCheckbox = document.getElementById('showDelaunay');

        // ----------------------------------------------------
        // 2. 점 생성 및 다이어그램 그리기 함수
        // ----------------------------------------------------

        // 무작위 점 생성 함수
        function generateRandomPoints() {
            const count = parseInt(pointCountInput.value);
            const width = container.clientWidth;
            const height = container.clientHeight;
            
            points = [];
            for (let i = 0; i < count; i++) {
                points.push({
                    x: Math.random() * (width - 40) + 20, // 가장자리 여백
                    y: Math.random() * (height - 40) + 20
                });
            }
            draw();
        }

        // 보로노이 및 델로네 다이어그램 계산 및 렌더링 함수
        function draw() {
            // 기존 그림 지우기
            svg.selectAll("*").remove();

            if (points.length < 3) return;

            const width = container.clientWidth;
            const height = container.clientHeight;

            // D3 Delaunay 객체 생성 (x, y 접근자 지정)
            const delaunay = d3.Delaunay.from(points, d => d.x, d => d.y);
            // Voronoi 객체 생성 (화면 크기에 맞게 바운딩 박스 설정)
            const voronoi = delaunay.voronoi([0, 0, width, height]);

            // 델로네 삼각형 그리기 (체크박스 확인)
            if (showDelaunayCheckbox.checked) {
                svg.append("path")
                    .attr("d", delaunay.render())
                    .attr("fill", "none")
                    .attr("stroke", "rgba(0, 123, 255, 0.5)") // 파란색 반투명
                    .attr("stroke-width", 1.5);
            }

            // 보로노이 다이어그램 그리기 (체크박스 확인)
            if (showVoronoiCheckbox.checked) {
                svg.append("path")
                    .attr("d", voronoi.render())
                    .attr("fill", "none")
                    .attr("stroke", "rgba(220, 53, 69, 1)") // 빨간색
                    .attr("stroke-width", 2);
            }

            // 드래그 이벤트 정의
            const drag = d3.drag()
                .on("start", function(event, d) {
                    d3.select(this).attr("stroke", "black").attr("stroke-width", 3);
                })
                .on("drag", function(event, d) {
                    // 드래그 중인 점의 좌표 업데이트
                    d.x = Math.max(0, Math.min(width, event.x)); // 화면 밖으로 나가지 않게
                    d.y = Math.max(0, Math.min(height, event.y));
                    // 좌표가 바뀌었으므로 화면 전체 다시 그리기
                    draw();
                })
                .on("end", function(event, d) {
                    d3.select(this).attr("stroke", "white").attr("stroke-width", 1.5);
                });

            // 생성점(원) 그리기 및 드래그 이벤트 바인딩
            svg.selectAll("circle")
                .data(points)
                .enter()
                .append("circle")
                .attr("class", "point")
                .attr("cx", d => d.x)
                .attr("cy", d => d.y)
                .attr("r", 6)
                .attr("fill", "#212529") // 짙은 회색/검정
                .attr("stroke", "white")
                .attr("stroke-width", 1.5)
                .call(drag); // 드래그 활성화
        }

        // ----------------------------------------------------
        // 3. 이벤트 리스너 등록
        // ----------------------------------------------------

        // 생성 버튼 클릭 시
        generateBtn.addEventListener('click', generateRandomPoints);

        // 체크박스 변경 시 즉시 다시 그리기
        showVoronoiCheckbox.addEventListener('change', draw);
        showDelaunayCheckbox.addEventListener('change', draw);

        // 이미지 업로드 처리 (FileReader API 사용)
        imageUpload.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(event) {
                    bgImage.src = event.target.result;
                    bgImage.style.display = 'block'; // 숨겨진 이미지 보이기
                };
                reader.readAsDataURL(file);
            } else {
                bgImage.style.display = 'none';
            }
        });

        // 창 크기 조절 시 (모바일 회전 등) 다시 계산하여 그리기
        window.addEventListener('resize', () => {
            if(points.length > 0) draw();
        });

        // ----------------------------------------------------
        // 4. 초기 실행
        // ----------------------------------------------------
        // 스크립트가 로드되면 기본값으로 점을 생성합니다.
        generateRandomPoints();

    </script>
    </body>
    </html>
'''

components.html(HTML, height=650, scrolling=True)