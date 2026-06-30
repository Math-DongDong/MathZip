import streamlit as st
import streamlit.components.v1 as components
import os

st.markdown("<h1 style='text-align: center; color: #d97706;'>성냥개비 퍼즐</h1>", unsafe_allow_html=True)

# -------------------------------------------------------------------
# 🌟 [수정된 부분] 1. 파이썬 서버가 직접 파일 목록을 읽어옵니다.
# -------------------------------------------------------------------
# 현재 앱이 실행되는 저장소 기준, 깃허브 Raw 이미지 기본 주소 (저장소 이름 확인 필요)
# 만약 로컬 서버라면 이 방식을 조금 수정해야 하지만, Streamlit Cloud 배포 기준입니다.
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/Math-DongDong/MathZip/main/기타/성냥개비퍼즐(54문제)"

# 54개의 문제 주소를 파이썬에서 리스트로 미리 만듭니다. 
# (파일 이름을 알고 있다면 직접 적는 것이 가장 빠르고 안전합니다.)
# 예시로 1.jpg 부터 54.jpg 라고 가정하고 리스트를 생성합니다. 
# ⚠️ 주의: 실제 파일 확장자나 이름 형식에 맞게 수정이 필요할 수 있습니다!
image_urls = [f"{GITHUB_RAW_BASE}/{i}.jpg" for i in range(1, 55)]

# 파이썬 리스트를 자바스크립트 배열 형식의 문자열로 변환합니다.
js_image_urls = str(image_urls)


# -------------------------------------------------------------------
# 2. HTML 내부에 파이썬이 읽어온 주소를 심어줍니다.
# -------------------------------------------------------------------
HTML = f'''
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background-color: #ffffff; color: #334155; margin: 0; }}
            #drawCanvas {{
                width: 100%;
                max-height: 470px;
                aspect-ratio: 4 / 3; 
                border: 2px solid #cbd5e1;
                border-radius: 12px;
                touch-action: none; 
                background-color: #ffffff;
                background-size: contain; 
                background-position: center;
                background-repeat: no-repeat;
                box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05);
                cursor: crosshair;
            }}
            @media (max-width: 768px) {{
                #drawCanvas {{ max-height: 470px; min-height: 470px; aspect-ratio: auto; }}
            }}
            .tool-btn {{
                background: #f8fafc; color: #475569; border: 1px solid #cbd5e1; border-radius: 6px; 
                padding: 6px 12px; font-size: 0.9rem; font-weight: bold; cursor: pointer; 
                transition: all 0.2s;
            }}
            .tool-btn:hover {{ background: #e2e8f0; }}
            .tool-btn.active {{ background: #3b82f6; color: white; border-color: #3b82f6; }}
        </style>
    </head>
    <body class="p-2 md:p-6">

        <div class="max-w-6xl mx-auto bg-white p-2 md:p-4">
            
            <!-- [게임 화면] (로딩 화면 제거됨) -->
            <div id="game-section" class="flex flex-col md:flex-row gap-6">
                
                <div class="w-full md:w-64 lg:w-72 flex flex-col gap-4 shrink-0 md:mt-12">
                    <div class="bg-slate-50 p-4 rounded-xl border border-slate-200 flex flex-row md:flex-col justify-around md:justify-center gap-2 md:gap-6 text-center shadow-sm">
                        <div><span class="text-xs sm:text-sm text-slate-500">총 문제</span><br><span id="total-cnt" class="text-lg sm:text-2xl font-bold text-slate-900">0</span></div>
                        <div><span class="text-xs sm:text-sm text-slate-500">해결한 문제</span><br><span id="solved-cnt" class="text-lg sm:text-2xl font-bold text-green-600">0</span></div>
                        <div><span class="text-xs sm:text-sm text-slate-500">다시 볼 문제</span><br><span id="unknown-cnt" class="text-lg sm:text-2xl font-bold text-orange-500">0</span></div>
                        <div><span class="text-xs sm:text-sm text-slate-500">남은 문제</span><br><span id="remain-cnt" class="text-lg sm:text-2xl font-bold text-blue-600">0</span></div>
                    </div>

                    <div class="grid grid-cols-2 md:grid-cols-1 gap-2 md:gap-3">
                        <button onclick="markUnknown()" class="bg-slate-100 hover:bg-slate-200 border border-slate-200 text-slate-700 font-bold py-2 md:py-3 rounded-lg transition text-xs sm:text-sm shadow-sm flex items-center justify-center gap-1">
                            ❓ 나중에 풀기
                        </button>
                        <button onclick="markSolved()" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 md:py-3 rounded-lg transition shadow-sm text-xs sm:text-sm flex items-center justify-center gap-1">
                            ✅ 해결했습니다!
                        </button>
                    </div>
                </div>

                <div class="flex-1 flex flex-col min-w-0">
                    <div class="flex justify-between items-center flex-wrap gap-3 mb-3">
                        <div class="font-bold text-sm md:text-base text-slate-700">💡 화면에 바로 그려서 풀어보세요!</div>
                        <div class="flex gap-2 flex-wrap">
                            <button id="btn-line" class="tool-btn active" onclick="setTool('line')">📏 직선</button>
                            <button id="btn-pen" class="tool-btn" onclick="setTool('pen')">✏️ 자유선</button>
                            <button id="btn-eraser" class="tool-btn" onclick="setTool('eraser')">🧽 지우개</button>
                            <button onclick="clearCanvas()" class="bg-red-50 hover:bg-red-100 text-red-600 border border-red-200 font-bold py-1 px-3 rounded-lg transition text-sm">🗑️ 모두 지우기</button>
                        </div>
                    </div>
                    <canvas id="drawCanvas" width="1600" height="1200"></canvas>
                </div>
            </div>

            <div id="end-section" class="hidden text-center p-10 bg-green-50 border border-green-200 rounded-2xl mt-6">
                <div class="text-5xl mb-4">🎉</div>
                <h2 class="text-xl md:text-2xl font-bold text-green-700 mb-4">모든 문제를 완료했습니다! 정말 수고하셨습니다.</h2>
                <button onclick="restartGame()" class="bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg shadow-md transition transform active:scale-95">
                    🔄 처음부터 다시하기
                </button>
            </div>
        </div>

        <script>
            // 🌟 [핵심] 파이썬에서 넣어준 이미지 URL 리스트를 바로 가져다 씁니다!
            // 더 이상 GitHub API를 호출하지 않으므로 트래픽/제한 문제가 전혀 없습니다.
            const rawUrls = {js_image_urls}; 
            let originalProblems = rawUrls; 
            
            let problemPool = [];      
            let solvedCount = 0;
            let unknownCount = 0;
            let currentProblemUrl = null;

            const gameSection = document.getElementById('game-section');
            const endSection = document.getElementById('end-section');
            
            const totalCntEl = document.getElementById('total-cnt');
            const solvedCntEl = document.getElementById('solved-cnt');
            const unknownCntEl = document.getElementById('unknown-cnt');
            const remainCntEl = document.getElementById('remain-cnt');

            window.onload = () => {{
                restartGame();
            }};

            function shuffle(array) {{
                for (let i = array.length - 1; i > 0; i--) {{
                    const j = Math.floor(Math.random() * (i + 1));
                    [array[i], array[j]] = [array[j], array[i]];
                }}
                return array;
            }}

            function restartGame() {{
                problemPool = [...originalProblems];
                shuffle(problemPool);
                solvedCount = 0;
                unknownCount = 0;
                
                endSection.classList.add('hidden');
                gameSection.classList.remove('hidden');

                nextProblem();
            }}

            function nextProblem() {{
                if (problemPool.length === 0) {{
                    gameSection.classList.add('hidden');
                    endSection.classList.remove('hidden');
                    return;
                }}

                currentProblemUrl = problemPool.shift();
                
                // ⚠️ 공백이나 한글 이름 인코딩 문제 방지를 위해 encodeURI 적용
                canvas.style.backgroundImage = `url('${{encodeURI(currentProblemUrl)}')`;
                clearCanvas(); 
                updateDashboard();
            }}

            function markSolved() {{
                solvedCount++;
                nextProblem();
            }}

            function markUnknown() {{
                unknownCount++;
                problemPool.push(currentProblemUrl);
                shuffle(problemPool); 
                nextProblem();
            }}

            function updateDashboard() {{
                totalCntEl.innerText = originalProblems.length;
                solvedCntEl.innerText = solvedCount;
                unknownCntEl.innerText = unknownCount;
                remainCntEl.innerText = problemPool.length + 1; 
            }}

            // --- 3. 캔버스 그림판 로직 ---
            const canvas = document.getElementById('drawCanvas');
            const ctx = canvas.getContext('2d', {{ willReadFrequently: true }});
            
            let drawing = false;
            let startX = 0, startY = 0;
            let lastX = 0, lastY = 0;
            let currentTool = 'line';
            let savedImageData = null;

            function setTool(tool) {{
                currentTool = tool;
                document.querySelectorAll('.tool-btn').forEach(btn => btn.classList.remove('active', 'bg-blue-600', 'text-white'));
                const activeBtn = document.getElementById('btn-' + tool);
                activeBtn.classList.add('active');
                
                activeBtn.style.backgroundColor = '#3b82f6'; 
                activeBtn.style.color = 'white';
                activeBtn.style.borderColor = '#3b82f6';
                
                document.querySelectorAll('.tool-btn:not(.active)').forEach(btn => {{
                    btn.style.backgroundColor = ''; 
                    btn.style.color = '';
                    btn.style.borderColor = '';
                }});
            }}
            setTool('line');

            function setPosition(e) {{
                const rect = canvas.getBoundingClientRect();
                const scaleX = canvas.width / rect.width;
                const scaleY = canvas.height / rect.height;
                
                let clientX = e.clientX;
                let clientY = e.clientY;

                if (e.touches && e.touches.length > 0) {{
                    clientX = e.touches[0].clientX;
                    clientY = e.touches[0].clientY;
                }}

                return {{ 
                    x: (clientX - rect.left) * scaleX, 
                    y: (clientY - rect.top) * scaleY 
                }};
            }}

            function startDraw(e) {{
                drawing = true;
                const pos = setPosition(e);
                startX = pos.x; startY = pos.y;
                lastX = pos.x; lastY = pos.y;

                if (currentTool === 'line') {{
                    savedImageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
                }}
            }}

            function draw(e) {{
                if (!drawing) return;
                e.preventDefault(); 
                const pos = setPosition(e);

                ctx.lineCap = 'round';
                ctx.lineJoin = 'round';

                if (currentTool === 'eraser') {{
                    ctx.globalCompositeOperation = 'destination-out';
                    ctx.lineWidth = 50; 
                    ctx.beginPath();
                    ctx.moveTo(lastX, lastY);
                    ctx.lineTo(pos.x, pos.y);
                    ctx.stroke();
                    lastX = pos.x; lastY = pos.y;
                    
                }} else if (currentTool === 'pen') {{
                    ctx.globalCompositeOperation = 'source-over';
                    ctx.strokeStyle = 'rgba(239, 68, 68, 0.8)'; 
                    ctx.lineWidth = 12;
                    ctx.beginPath();
                    ctx.moveTo(lastX, lastY);
                    ctx.lineTo(pos.x, pos.y);
                    ctx.stroke();
                    lastX = pos.x; lastY = pos.y;
                    
                }} else if (currentTool === 'line') {{
                    ctx.globalCompositeOperation = 'source-over';
                    ctx.strokeStyle = '#2563eb'; 
                    ctx.lineWidth = 15;
                    
                    ctx.putImageData(savedImageData, 0, 0); 
                    ctx.beginPath();
                    ctx.moveTo(startX, startY);
                    ctx.lineTo(pos.x, pos.y);
                    ctx.stroke();
                }}
            }}

            function stopDraw() {{ drawing = false; }}
            function clearCanvas() {{ ctx.clearRect(0, 0, canvas.width, canvas.height); }}

            canvas.addEventListener('mousedown', startDraw);
            canvas.addEventListener('mousemove', draw);
            canvas.addEventListener('mouseup', stopDraw);
            canvas.addEventListener('mouseout', stopDraw);
            
            canvas.addEventListener('touchstart', startDraw, {{passive: false}});
            canvas.addEventListener('touchmove', draw, {{passive: false}});
            canvas.addEventListener('touchend', stopDraw);
            canvas.addEventListener('touchcancel', stopDraw);
        </script>
    </body>
    </html>
'''

components.html(HTML, height=650, scrolling=True)