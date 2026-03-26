import streamlit as st
import streamlit.components.v1 as components

st.title("덧셈, 뺄셈")
html_code='''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>정수와 유리수 마스터</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Jua&display=swap" rel="stylesheet">
    
    <style>
        body {
            font-family: 'Jua', sans-serif;
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            touch-action: manipulation;
            margin: 0;
        }
        
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            20%, 60% { transform: translateX(-5px); }
            40%, 80% { transform: translateX(5px); }
        }
        .shake { animation: shake 0.4s ease-in-out; }

        @keyframes pop {
            0% { transform: scale(0.8); opacity: 0; }
            50% { transform: scale(1.1); opacity: 1; }
            100% { transform: scale(1); opacity: 1; }
        }
        .pop { animation: pop 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); }

        .key-btn { transition: transform 0.05s, background-color 0.2s; }
        .key-btn:active { transform: scale(0.92); background-color: #e2e8f0; }

        .frac-line { border-bottom: 3px solid #1f2937; }
    </style>
</head>
<body class="min-h-screen flex items-center justify-center p-0 sm:p-4">

    <!-- 메인 컨테이너 -->
    <div class="w-full h-screen md:h-[650px] md:max-w-4xl bg-white md:rounded-3xl shadow-2xl flex flex-col md:flex-row relative overflow-hidden">
        
        <!-- [왼쪽 영역] 게임 화면 -->
        <div class="flex-1 flex flex-col relative bg-white">
            
            <!-- 헤더 -->
            <div class="bg-blue-500 text-white p-4 md:rounded-tl-3xl shadow-md z-10">
                <div class="flex justify-between items-end mb-2">
                    <div class="flex flex-col gap-2">
                        <div>
                            <span id="level-badge" class="bg-yellow-400 text-yellow-900 px-3 py-1 rounded-full text-sm sm:text-base font-bold shadow">
                                Lv.1 초보자
                            </span>
                        </div>
                        <div class="text-sm font-bold tracking-widest text-red-200" id="lives-display">❤️❤️❤️❤️❤️</div>
                    </div>
                    <div class="text-right flex flex-col justify-end">
                        <div class="text-xs sm:text-sm text-blue-100 font-bold mb-1">평균: <span id="avg-time">0.0초</span></div>
                        <div id="combo-display" class="text-yellow-300 font-bold text-sm sm:text-base h-5 transition-all leading-none"></div>
                        <div class="text-xl sm:text-2xl mt-1 leading-none">점수: <span id="score">0</span></div>
                    </div>
                </div>
                <div class="w-full bg-blue-300 rounded-full h-2 mt-2">
                    <div id="progress-bar" class="bg-yellow-400 h-2 rounded-full transition-all duration-300" style="width: 0%"></div>
                </div>
            </div>

            <!-- 수식 및 피드백 표시 -->
            <div class="flex-1 flex flex-col items-center justify-center p-4 relative overflow-y-auto">
                
                <!-- 레벨업 알림 -->
                <div id="levelup-overlay" class="absolute inset-0 bg-white/90 flex items-center justify-center hidden z-20">
                    <div class="text-center pop">
                        <div class="text-6xl mb-2">🎉</div>
                        <h2 class="text-3xl font-bold text-blue-600">레벨 업!</h2>
                        <p id="levelup-msg" class="text-gray-600 mt-2">난이도가 상승합니다!</p>
                    </div>
                </div>

                <!-- 게임 오버 알림 -->
                <div id="gameover-overlay" class="absolute inset-0 bg-black/80 flex items-center justify-center hidden z-30">
                    <div class="text-center pop bg-white p-8 rounded-3xl shadow-2xl mx-4 w-11/12 max-w-sm">
                        <div class="text-6xl mb-4">😭</div>
                        <h2 class="text-3xl font-bold text-red-500 mb-2">게임 종료!</h2>
                        <p class="text-gray-600 mb-6">하트를 모두 소진했습니다.</p>
                        <div class="bg-gray-100 rounded-xl p-4 mb-6">
                            <p class="text-lg text-gray-700">최종 점수: <span id="final-score" class="font-bold text-blue-600 text-2xl">0</span>점</p>
                            <p class="text-lg text-gray-700">평균 풀이: <span id="final-avg-time" class="font-bold text-green-500 text-xl">0.0초</span></p>
                        </div>
                        <button onclick="restartGame()" class="bg-blue-500 hover:bg-blue-600 text-white font-bold text-xl py-3 px-8 w-full rounded-full shadow-lg transition-transform active:scale-95">
                            다시 도전하기
                        </button>
                    </div>
                </div>

                <div id="feedback-msg" class="text-xl font-bold text-green-500 h-8 transition-all opacity-0">정답입니다!</div>

                <!-- 수식 컨테이너 -->
                <div id="question-box" class="flex flex-wrap items-center justify-center gap-1 sm:gap-2 text-4xl sm:text-5xl font-bold text-gray-800 my-8 text-center tracking-wider min-h-[80px]">
                </div>

                <!-- 입력 칸 -->
                <div id="input-box" class="w-full max-w-[220px] text-center border-b-4 border-blue-400 text-4xl text-blue-600 font-bold py-2 h-16 bg-gray-50 rounded-t-lg flex items-center justify-center tracking-widest overflow-hidden">
                </div>
                
                <p id="hint-msg" class="text-gray-400 text-sm mt-4 h-4 text-center transition-opacity">※ 분수는 1/2 형식의 기약분수로 입력하세요.</p>
            </div>
        </div>

        <!--[오른쪽 영역 / 모바일 하단] 키패드 -->
        <div class="w-full md:w-80 lg:w-96 bg-gray-100 p-3 sm:p-6 flex flex-col justify-center border-t md:border-t-0 md:border-l border-gray-200 z-10">
            <div class="grid grid-cols-4 gap-2 w-full h-full md:h-auto max-w-sm mx-auto">
                <button class="key-btn bg-white shadow rounded-xl text-2xl font-bold py-4 md:py-5 text-gray-700" onclick="inputKey('1')">1</button>
                <button class="key-btn bg-white shadow rounded-xl text-2xl font-bold py-4 md:py-5 text-gray-700" onclick="inputKey('2')">2</button>
                <button class="key-btn bg-white shadow rounded-xl text-2xl font-bold py-4 md:py-5 text-gray-700" onclick="inputKey('3')">3</button>
                <button class="key-btn bg-red-100 shadow rounded-xl text-xl font-bold py-4 md:py-5 text-red-600" onclick="inputKey('DEL')">지우기</button>
                
                <button class="key-btn bg-white shadow rounded-xl text-2xl font-bold py-4 md:py-5 text-gray-700" onclick="inputKey('4')">4</button>
                <button class="key-btn bg-white shadow rounded-xl text-2xl font-bold py-4 md:py-5 text-gray-700" onclick="inputKey('5')">5</button>
                <button class="key-btn bg-white shadow rounded-xl text-2xl font-bold py-4 md:py-5 text-gray-700" onclick="inputKey('6')">6</button>
                <button class="key-btn bg-blue-100 shadow rounded-xl text-3xl font-bold py-4 md:py-5 text-blue-700" onclick="inputKey('-')">-</button>
                
                <button class="key-btn bg-white shadow rounded-xl text-2xl font-bold py-4 md:py-5 text-gray-700" onclick="inputKey('7')">7</button>
                <button class="key-btn bg-white shadow rounded-xl text-2xl font-bold py-4 md:py-5 text-gray-700" onclick="inputKey('8')">8</button>
                <button class="key-btn bg-white shadow rounded-xl text-2xl font-bold py-4 md:py-5 text-gray-700" onclick="inputKey('9')">9</button>
                <button class="key-btn bg-blue-100 shadow rounded-xl text-2xl font-bold py-4 md:py-5 text-blue-700" onclick="inputKey('/')">/</button>
                
                <button class="key-btn bg-gray-200 shadow rounded-xl text-lg font-bold py-4 md:py-5 text-gray-700" onclick="inputKey('CLEAR')">초기화</button>
                <button class="key-btn bg-white shadow rounded-xl text-2xl font-bold py-4 md:py-5 text-gray-700" onclick="inputKey('0')">0</button>
                <button class="key-btn bg-blue-500 shadow rounded-xl text-xl font-bold py-4 md:py-5 text-white col-span-2 hover:bg-blue-600" onclick="checkAnswer()">입력 (Enter)</button>
            </div>
        </div>
    </div>

    <script>
        // 게임 상태 변수
        let score = 0;
        let combo = 0;
        let level = 1;
        let lives = 5;
        let expectedAnswer = "";
        let currentInput = "";
        
        // 통계 (시간) 변수
        let totalTimeMs = 0;
        let solvedCount = 0;
        let questionStartTime = 0;

        const LEVEL_THRESHOLDS =[0, 5, 12, 20]; 
        const LEVEL_TITLES =["Lv.1 덧셈 연습", "Lv.2 덧셈과 뺄셈", "Lv.3 음수의 뺄셈", "Lv.4 유리수 마스터"];
        const PRAISES =["완벽해요! 🔥", "최고예요! ⭐", "천재인가요? 🚀", "잘하고 있어요! 👏", "정답입니다! 💯"];

        const scoreEl = document.getElementById('score');
        const comboEl = document.getElementById('combo-display');
        const levelBadgeEl = document.getElementById('level-badge');
        const progressBarEl = document.getElementById('progress-bar');
        const livesDisplay = document.getElementById('lives-display');
        const avgTimeDisplay = document.getElementById('avg-time');
        
        const questionBox = document.getElementById('question-box');
        const inputBox = document.getElementById('input-box');
        const feedbackMsg = document.getElementById('feedback-msg');
        const levelUpOverlay = document.getElementById('levelup-overlay');
        const levelUpMsg = document.getElementById('levelup-msg');
        const gameOverOverlay = document.getElementById('gameover-overlay');
        const hintMsg = document.getElementById('hint-msg');

        function init() {
            updateUI();
            generateQuestion();
        }

        function restartGame() {
            score = 0;
            combo = 0;
            level = 1;
            lives = 5;
            totalTimeMs = 0;
            solvedCount = 0;
            gameOverOverlay.classList.add('hidden');
            init();
        }

        function inputKey(key) {
            if (lives <= 0) return; // 게임오버 시 입력 금지
            if (key === 'DEL') currentInput = currentInput.slice(0, -1);
            else if (key === 'CLEAR') currentInput = "";
            else if (key === '-') { if (currentInput === "") currentInput = "-"; }
            else if (key === '/') { if (!currentInput.includes('/') && currentInput !== "" && currentInput !== "-") currentInput += "/"; }
            else { if (currentInput.length < 8) currentInput += key; }
            inputBox.innerText = currentInput;
        }

        function gcd(a, b) {
            a = Math.abs(a); b = Math.abs(b);
            while (b) { let t = b; b = a % b; a = t; }
            return a;
        }

        function getRandomInt(min, max) { return Math.floor(Math.random() * (max - min + 1)) + min; }

        // 분수 모양 HTML 생성기
        // isFirst: 첫 번째 항이면 괄호 무조건 생략 (양수면 기호 생략, 음수면 - 표시)
        // !isFirst: 두 번째 항일 때 양수면 괄호 생략, 음수면 괄호 추가
        function createFractionHTML(n, d, isFirst) {
            let isPositive = (n * d) > 0;
            let absN = Math.abs(n);
            let absD = Math.abs(d);
            
            let fracCore = `
                <div class="flex flex-col items-center text-[0.65em] leading-none mx-0.5 relative top-[-2px]">
                    <span class="frac-line w-full text-center pb-1">${absN}</span>
                    <span class="pt-1">${absD}</span>
                </div>`;
            
            if (isFirst) {
                // 첫번째 숫자는 괄호 완전 생략
                let sign = isPositive ? '' : '-';
                return `<span class="flex items-center mx-1"><span>${sign}</span>${fracCore}</span>`;
            } else {
                // 두번째 숫자: 양수면 괄호 생략 (부호도 생략되므로 연산자와 바로 붙음)
                if (isPositive) {
                    return `<span class="flex items-center mx-1">${fracCore}</span>`;
                } else {
                    // 음수면 괄호 치기
                    return `<span class="flex items-center mx-1"><span>(</span><span>-</span>${fracCore}<span>)</span></span>`;
                }
            }
        }

        function generateQuestion() {
            currentInput = "";
            inputBox.innerText = "";
            inputBox.classList.remove('shake');
            
            let newLevel = 1;
            if (score >= LEVEL_THRESHOLDS[3]) newLevel = 4;
            else if (score >= LEVEL_THRESHOLDS[2]) newLevel = 3;
            else if (score >= LEVEL_THRESHOLDS[1]) newLevel = 2;

            let isLevelUp = false;
            if (newLevel > level) {
                level = newLevel;
                isLevelUp = true;
            }
            updateUI();

            // 이전 난이도 40% 섞어 출제
            let problemType = level;
            if (level > 1 && Math.random() < 0.4) {
                problemType = getRandomInt(1, level - 1);
            }

            let qHtml = "";
            let ansStr = "";

            if (problemType === 1) {
                let a = getRandomInt(-10, 10);
                let b = getRandomInt(1, 10); // b는 무조건 양수
                qHtml = `<span>${a}</span> <span class="mx-1">+</span> <span>${b}</span>`;
                ansStr = (a + b).toString();
                hintMsg.style.opacity = 0;
            } 
            else if (problemType === 2) {
                let a = getRandomInt(-10, 10);
                let b = getRandomInt(1, 10); // b는 무조건 양수
                let isAdd = Math.random() < 0.5;
                qHtml = `<span>${a}</span> <span class="mx-1">${isAdd ? '+' : '-'}</span> <span>${b}</span>`;
                ansStr = isAdd ? (a + b).toString() : (a - b).toString();
                hintMsg.style.opacity = 0;
            } 
            else if (problemType === 3) {
                // 음수가 포함되는 덧셈/뺄셈
                let a = getRandomInt(-10, 10);
                let b = getRandomInt(-10, 10);
                if (a === 0) a = 2; if (b === 0) b = -3;
                let isAdd = Math.random() < 0.5;
                
                // 첫번째 숫자: 무조건 괄호 생략 (예: 3, -3)
                let signA = `${a}`;
                
                // 두번째 숫자: 양수면 괄호 생략 (+부호 생략), 음수면 괄호 포함
                let signB = b > 0 ? `${b}` : `(${b})`;
                
                qHtml = `<span>${signA}</span> <span class="mx-1 text-blue-500">${isAdd ? '+' : '-'}</span> <span>${signB}</span>`;
                ansStr = isAdd ? (a + b).toString() : (a - b).toString();
                hintMsg.style.opacity = 0;
            } 
            else if (problemType === 4) {
                hintMsg.style.opacity = 1;
                
                let d1 = getRandomInt(2, 6);
                let d2 = getRandomInt(2, 6);
                let n1 = getRandomInt(1, d1 - 1) * (Math.random() < 0.5 ? 1 : -1);
                let n2 = getRandomInt(1, d2 - 1) * (Math.random() < 0.5 ? 1 : -1);
                let isAdd = Math.random() < 0.5;

                qHtml = `${createFractionHTML(n1, d1, true)} <span class="mx-1 text-blue-500">${isAdd ? '+' : '-'}</span> ${createFractionHTML(n2, d2, false)}`;

                let top = isAdd ? (n1 * d2 + n2 * d1) : (n1 * d2 - n2 * d1);
                let bottom = d1 * d2;

                if (top === 0) {
                    ansStr = "0";
                } else {
                    let g = gcd(top, bottom);
                    top /= g; bottom /= g;
                    if (bottom < 0) { top = -top; bottom = -bottom; }
                    ansStr = bottom === 1 ? `${top}` : `${top}/${bottom}`;
                }
            }

            questionBox.innerHTML = qHtml + `<span class="ml-2 text-gray-400">= ?</span>`;
            expectedAnswer = ansStr;

            // 시간 측정 시작
            if (isLevelUp) {
                showLevelUp();
            } else {
                questionStartTime = Date.now();
            }
        }

        function showLevelUp() {
            levelUpMsg.innerText = LEVEL_TITLES[level-1] + " 등장!";
            levelUpOverlay.classList.remove('hidden');
            setTimeout(() => { 
                levelUpOverlay.classList.add('hidden'); 
                questionStartTime = Date.now(); // 오버레이가 끝난 직후부터 시간 측정 시작!
            }, 2000);
        }

        function showGameOver() {
            gameOverOverlay.classList.remove('hidden');
            document.getElementById('final-score').innerText = score;
            let finalAvg = solvedCount === 0 ? "0.0" : ((totalTimeMs / solvedCount) / 1000).toFixed(1);
            document.getElementById('final-avg-time').innerText = finalAvg + "초";
        }

        function checkAnswer() {
            if (currentInput === "" || lives <= 0) return;

            if (currentInput === expectedAnswer) {
                // 정답
                let timeTaken = Date.now() - questionStartTime;
                totalTimeMs += timeTaken;
                solvedCount++;
                score += 1;
                combo += 1;
                
                feedbackMsg.innerText = PRAISES[Math.floor(Math.random() * PRAISES.length)];
                feedbackMsg.classList.remove('opacity-0', 'text-red-500');
                feedbackMsg.classList.add('opacity-100', 'text-green-500', 'pop');
                updateUI();
                
                setTimeout(() => {
                    feedbackMsg.classList.remove('pop', 'opacity-100');
                    feedbackMsg.classList.add('opacity-0');
                    generateQuestion();
                }, 800);
            } else {
                // 오답
                combo = 0;
                lives--;
                updateUI();

                if (lives <= 0) {
                    showGameOver();
                    return;
                }

                inputBox.classList.remove('shake');
                void inputBox.offsetWidth; 
                inputBox.classList.add('shake');
                currentInput = "";
                inputBox.innerText = "";
                
                feedbackMsg.innerText = "앗, 다시 계산해볼까요? 😅";
                feedbackMsg.classList.remove('opacity-0', 'text-green-500');
                feedbackMsg.classList.add('opacity-100', 'text-red-500');
                
                setTimeout(() => {
                    feedbackMsg.classList.remove('opacity-100');
                    feedbackMsg.classList.add('opacity-0');
                }, 1500);
            }
        }

        function updateUI() {
            scoreEl.innerText = score;
            levelBadgeEl.innerText = LEVEL_TITLES[level-1];
            livesDisplay.innerText = '❤️'.repeat(lives) + '🖤'.repeat(5 - lives); // 잃은 하트를 검은색으로 표시
            
            // 평균 시간 업데이트
            let avgSec = solvedCount === 0 ? "0.0" : ((totalTimeMs / solvedCount) / 1000).toFixed(1);
            avgTimeDisplay.innerText = avgSec + "초";
            
            if (combo >= 2) comboEl.innerText = `${combo} 콤보! 🔥`;
            else comboEl.innerText = "";

            let maxScore = LEVEL_THRESHOLDS[level] || LEVEL_THRESHOLDS[3] + 10;
            let minScore = LEVEL_THRESHOLDS[level-1];
            let percent = ((score - minScore) / (maxScore - minScore)) * 100;
            if (percent > 100) percent = 100;
            if (level === 4) percent = 100; 
            
            progressBarEl.style.width = `${percent}%`;
        }

        // 데스크탑 물리 키보드 대응
        document.addEventListener('keydown', (e) => {
            const key = e.key;
            if (key >= '0' && key <= '9') inputKey(key);
            else if (key === '-' || key === '/') inputKey(key);
            else if (key === 'Backspace') inputKey('DEL');
            else if (key === 'Enter') checkAnswer();
        });

        // 초기 시작
        init();

    </script>
</body>
</html>
'''

# 4. 스트림릿 컴포넌트로 렌더링
components.html(html_code, height=800, scrolling=True)