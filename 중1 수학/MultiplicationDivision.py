import streamlit as st
import streamlit.components.v1 as components

html_code='''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>정수와 유리수의 곱셈과 나눗셈</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Jua&display=swap" rel="stylesheet">
    
    <style>
        /* 배경 및 기본 설정 (완전 흰색, 스크롤 방지) */
        body {
            font-family: 'Jua', sans-serif;
            background-color: #ffffff;
            touch-action: manipulation;
            margin: 0;
            padding: 0;
            width: 100vw;
            height: 100vh;
            overflow: hidden;
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

        .frac-line { border-bottom: 2px solid #1f2937; }
    </style>
</head>
<body class="flex items-center justify-center">

    <div class="w-full h-full bg-white flex flex-col md:flex-row relative">
        
        <!--[왼쪽 영역] 게임 화면 -->
        <div class="flex-1 flex flex-col relative bg-white min-h-0">
            
            <!-- 헤더 -->
            <div class="bg-blue-500 text-white p-3 sm:p-4 z-10">
                <div class="flex justify-between items-end mb-2">
                    <div class="flex flex-col gap-1 sm:gap-2">
                        <div>
                            <span id="level-badge" class="bg-yellow-400 text-yellow-900 px-2 py-1 sm:px-3 sm:py-1 rounded-full text-xs sm:text-sm font-bold shadow-sm">
                                Lv.1 정수 곱셈
                            </span>
                        </div>
                        <div class="text-xs sm:text-sm font-bold tracking-widest text-red-200" id="lives-display">❤️❤️❤️❤️❤️</div>
                    </div>
                    <div class="text-right flex flex-col justify-end">
                        <div class="flex justify-between items-center mb-1">
                            <div id="combo-display" class="text-yellow-300 font-bold text-base sm:text-lg"></div>
                            <div class="text-base sm:text-lg text-blue-100 font-bold">평균: <span id="avg-time">0.0초</span></div>
                        </div>
                        <div class="flex justify-between items-center mt-1 gap-4">
                            <div id="max-combo-display" class="text-yellow-300 font-bold text-lg sm:text-xl"></div>
                            <div class="text-lg sm:text-xl leading-none">점수: <span id="score">0</span></div>
                        </div>
                    </div>
                </div>
                <div class="w-full bg-blue-300 rounded-full h-1.5 sm:h-2 mt-1 sm:mt-2">
                    <div id="progress-bar" class="bg-yellow-400 h-1.5 sm:h-2 rounded-full transition-all duration-300" style="width: 0%"></div>
                </div>
            </div>

            <!-- 수식 및 피드백 표시 -->
            <div class="flex-1 flex flex-col items-center justify-center p-2 sm:p-4 relative overflow-y-auto">
                
                <div id="levelup-overlay" class="absolute inset-0 bg-white/95 flex items-center justify-center hidden z-20">
                    <div class="text-center pop">
                        <div class="text-5xl sm:text-6xl mb-2">🎉</div>
                        <h2 class="text-2xl sm:text-3xl font-bold text-blue-600">레벨 업!</h2>
                        <p id="levelup-msg" class="text-sm sm:text-base text-gray-600 mt-2">새로운 개념이 등장합니다!</p>
                    </div>
                </div>

                <div id="gameover-overlay" class="absolute inset-0 bg-black/80 flex items-center justify-center hidden z-30">
                    <div class="text-center pop bg-white p-6 sm:p-8 rounded-2xl shadow-xl mx-4 w-11/12 max-w-sm">
                        <div class="text-5xl sm:text-6xl mb-4">😭</div>
                        <h2 class="text-2xl sm:text-3xl font-bold text-red-500 mb-2">게임 종료!</h2>
                        <p class="text-sm sm:text-base text-gray-600 mb-6">하트를 모두 소진했습니다.</p>
                        <div class="bg-gray-100 rounded-xl p-3 sm:p-4 mb-6">
                            <p class="text-base sm:text-lg text-gray-700">최종 점수: <span id="final-score" class="font-bold text-blue-600 text-xl sm:text-2xl">0</span>점</p>
                            <p class="text-base sm:text-lg text-gray-700">평균 풀이: <span id="final-avg-time" class="font-bold text-green-500 text-lg sm:text-xl">0.0초</span></p>
                            <p class="text-base sm:text-lg text-gray-700">최고 콤보: <span id="final-max-combo" class="font-bold text-purple-500 text-lg sm:text-xl">0</span></p>
                        </div>
                        <button onclick="restartGame()" class="bg-blue-500 hover:bg-blue-600 text-white font-bold text-lg sm:text-xl py-3 px-8 w-full rounded-full transition-transform active:scale-95">
                            다시 도전하기
                        </button>
                    </div>
                </div>

                <div id="feedback-msg" class="text-lg sm:text-xl font-bold text-green-500 h-8 transition-all opacity-0">정답입니다!</div>

                <!-- 수식 컨테이너 -->
                <div id="question-box" class="flex flex-wrap items-center justify-center gap-x-1 gap-y-2 text-3xl sm:text-4xl md:text-5xl font-bold text-gray-800 my-4 sm:my-8 text-center min-h-[60px] sm:min-h-[80px] w-full px-2">
                </div>

                <!-- 입력 칸 -->
                <div id="input-box" class="w-full max-w-[180px] sm:max-w-[220px] text-center border-b-4 border-blue-400 text-3xl sm:text-4xl text-blue-600 font-bold py-2 h-14 sm:h-16 bg-gray-50 rounded-t-lg flex items-center justify-center tracking-widest overflow-hidden">
                </div>
                
                <p id="hint-msg" class="text-gray-400 text-xs sm:text-sm mt-3 sm:mt-4 h-4 text-center transition-opacity">※ 분수는 1/2 형식의 기약분수로 입력하세요.</p>
            </div>
        </div>

        <!-- [오른쪽 영역 / 모바일 하단] 키패드 -->
        <div class="w-full md:w-[300px] lg:w-[350px] bg-white p-2 sm:p-4 flex flex-col justify-center border-t md:border-t-0 md:border-l border-gray-200 z-10 shrink-0">
            <div class="grid grid-cols-4 gap-1.5 sm:gap-2 w-full h-full md:h-auto max-w-sm mx-auto">
                <button class="key-btn bg-gray-50 shadow-sm border border-gray-100 rounded-lg sm:rounded-xl text-xl sm:text-2xl font-bold py-3 sm:py-4 md:py-5 text-gray-700" onclick="inputKey('1')">1</button>
                <button class="key-btn bg-gray-50 shadow-sm border border-gray-100 rounded-lg sm:rounded-xl text-xl sm:text-2xl font-bold py-3 sm:py-4 md:py-5 text-gray-700" onclick="inputKey('2')">2</button>
                <button class="key-btn bg-gray-50 shadow-sm border border-gray-100 rounded-lg sm:rounded-xl text-xl sm:text-2xl font-bold py-3 sm:py-4 md:py-5 text-gray-700" onclick="inputKey('3')">3</button>
                <button class="key-btn bg-red-50 shadow-sm border border-red-100 rounded-lg sm:rounded-xl text-base sm:text-xl font-bold py-3 sm:py-4 md:py-5 text-red-500" onclick="inputKey('DEL')">지움</button>
                
                <button class="key-btn bg-gray-50 shadow-sm border border-gray-100 rounded-lg sm:rounded-xl text-xl sm:text-2xl font-bold py-3 sm:py-4 md:py-5 text-gray-700" onclick="inputKey('4')">4</button>
                <button class="key-btn bg-gray-50 shadow-sm border border-gray-100 rounded-lg sm:rounded-xl text-xl sm:text-2xl font-bold py-3 sm:py-4 md:py-5 text-gray-700" onclick="inputKey('5')">5</button>
                <button class="key-btn bg-gray-50 shadow-sm border border-gray-100 rounded-lg sm:rounded-xl text-xl sm:text-2xl font-bold py-3 sm:py-4 md:py-5 text-gray-700" onclick="inputKey('6')">6</button>
                <button class="key-btn bg-blue-50 shadow-sm border border-blue-100 rounded-lg sm:rounded-xl text-2xl sm:text-3xl font-bold py-3 sm:py-4 md:py-5 text-blue-600" onclick="inputKey('-')">-</button>
                
                <button class="key-btn bg-gray-50 shadow-sm border border-gray-100 rounded-lg sm:rounded-xl text-xl sm:text-2xl font-bold py-3 sm:py-4 md:py-5 text-gray-700" onclick="inputKey('7')">7</button>
                <button class="key-btn bg-gray-50 shadow-sm border border-gray-100 rounded-lg sm:rounded-xl text-xl sm:text-2xl font-bold py-3 sm:py-4 md:py-5 text-gray-700" onclick="inputKey('8')">8</button>
                <button class="key-btn bg-gray-50 shadow-sm border border-gray-100 rounded-lg sm:rounded-xl text-xl sm:text-2xl font-bold py-3 sm:py-4 md:py-5 text-gray-700" onclick="inputKey('9')">9</button>
                <button class="key-btn bg-blue-50 shadow-sm border border-blue-100 rounded-lg sm:rounded-xl text-xl sm:text-2xl font-bold py-3 sm:py-4 md:py-5 text-blue-600" onclick="inputKey('/')">/</button>
                
                <button class="key-btn bg-gray-200 shadow-sm border border-gray-300 rounded-lg sm:rounded-xl text-sm sm:text-lg font-bold py-3 sm:py-4 md:py-5 text-gray-700" onclick="inputKey('CLEAR')">초기화</button>
                <button class="key-btn bg-gray-50 shadow-sm border border-gray-100 rounded-lg sm:rounded-xl text-xl sm:text-2xl font-bold py-3 sm:py-4 md:py-5 text-gray-700" onclick="inputKey('0')">0</button>
                <button class="key-btn bg-blue-500 shadow-sm rounded-lg sm:rounded-xl text-base sm:text-xl font-bold py-3 sm:py-4 md:py-5 text-white col-span-2 hover:bg-blue-600" onclick="checkAnswer()">입력 (Enter)</button>
            </div>
        </div>
    </div>

    <script>
        let score = 0;
        let combo = 0;
        let maxCombo = 0;
        let level = 1;
        let lives = 5;
        let expectedAnswer = "";
        let currentInput = "";
        
        let totalTimeMs = 0;
        let solvedCount = 0;
        let questionStartTime = 0;
        let isChecking = false;

        // 6단계 레벨로 세분화 (정수곱 -> 유리수곱 -> 거듭제곱 -> 나눗셈 -> 혼합 -> 덧셈의 귀환)
        const LEVEL_THRESHOLDS =[0, 10, 20, 30, 40, 50]; 
        const LEVEL_TITLES =["Lv.1 정수 곱셈", "Lv.2 유리수 곱셈", "Lv.3 거듭제곱", "Lv.4 나눗셈", "Lv.5 혼합 계산", "Lv.6 덧셈의 귀환"];
        const PRAISES =["완벽해요! 🔥", "최고예요! ⭐", "천재인가요? 🚀", "잘하고 있어요! 👏", "정답입니다! 💯"];

        const scoreEl = document.getElementById('score');
        const comboEl = document.getElementById('combo-display');
        const maxComboEl = document.getElementById('max-combo-display');
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
            score = 0; combo = 0; maxCombo = 0; level = 1; lives = 5;
            totalTimeMs = 0; solvedCount = 0;
            gameOverOverlay.classList.add('hidden');
            init();
        }

        function inputKey(key) {
            if (lives <= 0) return; 
            if (key === 'DEL') currentInput = currentInput.slice(0, -1);
            else if (key === 'CLEAR') currentInput = "";
            else if (key === '-') { if (currentInput === "") currentInput = "-"; }
            else if (key === '/') { if (!currentInput.includes('/') && currentInput !== "" && currentInput !== "-") currentInput += "/"; }
            else { if (currentInput.length < 8) currentInput += key; }
            inputBox.innerText = currentInput;
        }

        // 최대공약수
        function gcd(a, b) {
            a = Math.abs(a); b = Math.abs(b);
            while (b) { let t = b; b = a % b; a = t; }
            return a;
        }

        // 분수 기약분수화 및 문자열 반환 헬퍼
        function simplify(n, d) {
            if (n === 0) return "0";
            let g = gcd(n, d);
            n /= g; d /= g;
            if (d < 0) { n = -n; d = -d; }
            return d === 1 ? `${n}` : `${n}/${d}`;
        }

        function getRandomInt(min, max) { return Math.floor(Math.random() * (max - min + 1)) + min; }

        // 유리수(분수)를 HTML로 이쁘게 변환해주는 헬퍼
        function createFractionHTML(n, d, isFirst) {
            let isPositive = (n * d) > 0;
            let absN = Math.abs(n);
            let absD = Math.abs(d);
            
            let fracCore = `
                <div class="flex flex-col items-center text-[0.65em] leading-none mx-0.5 sm:mx-1 relative top-[-2px]">
                    <span class="frac-line w-full text-center pb-0.5 sm:pb-1">${absN}</span>
                    <span class="pt-0.5 sm:pt-1">${absD}</span>
                </div>`;
            
            if (isFirst) {
                let sign = isPositive ? '' : '-';
                return `<span class="flex items-center mx-0.5 sm:mx-1"><span>${sign}</span>${fracCore}</span>`;
            } else {
                if (isPositive) {
                    return `<span class="flex items-center mx-0.5 sm:mx-1">${fracCore}</span>`;
                } else {
                    return `<span class="flex items-center mx-0.5 sm:mx-1"><span>(</span><span class="ml-0.5">-</span>${fracCore}<span>)</span></span>`;
                }
            }
        }

        function generateQuestion() {
            currentInput = ""; inputBox.innerText = ""; inputBox.classList.remove('shake');
            
            let newLevel = 1;
            if (score >= LEVEL_THRESHOLDS[5]) newLevel = 6;
            else if (score >= LEVEL_THRESHOLDS[4]) newLevel = 5;
            else if (score >= LEVEL_THRESHOLDS[3]) newLevel = 4;
            else if (score >= LEVEL_THRESHOLDS[2]) newLevel = 3;
            else if (score >= LEVEL_THRESHOLDS[1]) newLevel = 2;

            let isLevelUp = false;
            if (newLevel > level) { level = newLevel; isLevelUp = true; }
            updateUI();

            // 이전 난이도 혼합 (40% 확률)
            let problemType = level;
            if (level > 1 && Math.random() < 0.4) {
                problemType = getRandomInt(1, level - 1);
            }

            let qHtml = "";
            let ansStr = "";

            if (problemType === 1) {
                // Lv.1 정수의 곱셈
                let a = getRandomInt(-10, 10);
                let b = getRandomInt(-10, 10);
                if (a === 0) a = 3; if (b === 0) b = -2; // 0 제거
                
                let signA = `${a}`;
                let signB = b > 0 ? `${b}` : `(${b})`; // 양수는 괄호 생략
                
                qHtml = `<span>${signA}</span> <span class="mx-1 text-blue-500">×</span> <span>${signB}</span>`;
                ansStr = (a * b).toString();
                hintMsg.style.opacity = 0;
            } 
            else if (problemType === 2) {
                // Lv.2 유리수(분수)의 곱셈
                let d1 = getRandomInt(2, 6);
                let d2 = getRandomInt(2, 6);
                let n1 = getRandomInt(1, d1 - 1) * (Math.random() < 0.5 ? 1 : -1);
                let n2 = getRandomInt(1, d2 - 1) * (Math.random() < 0.5 ? 1 : -1);

                qHtml = `${createFractionHTML(n1, d1, true)} <span class="mx-1 text-blue-500">×</span> ${createFractionHTML(n2, d2, false)}`;
                ansStr = simplify(n1 * n2, d1 * d2);
                hintMsg.style.opacity = 1;
            }
            else if (problemType === 3) {
                // Lv.3 거듭제곱 (정수 및 분수)
                let type = Math.random() < 0.5 ? 'int' : 'frac';
                if (type === 'int') {
                    let base = getRandomInt(2, 5);
                    let exp = getRandomInt(2, base === 2 ? 4 : 3); // 2^4=16, 3^3=27
                    let isParens = Math.random() < 0.5; // (-3)^2 와 -3^2 구분
                    
                    let baseStr = isParens ? `(-${base})` : `-${base}`;
                    
                    // [수정됨] 지수를 위쪽으로 깔끔하게 올림 (-mt 적용)
                    qHtml = `<span class="flex items-start">
                                <span class="flex items-center">${baseStr}</span>
                                <span class="text-[0.65em] font-bold ml-0.5 -mt-1 sm:-mt-2">${exp}</span>
                             </span>`;
                    
                    let val = Math.pow(base, exp);
                    ansStr = (isParens && exp % 2 === 0) ? val.toString() : (-val).toString();
                } else {
                    let d = getRandomInt(2, 4);
                    let n = getRandomInt(1, d - 1);
                    let exp = getRandomInt(2, 3);
                    let isNeg = Math.random() < 0.5;
                    let sign = isNeg ? '-' : '';
                    
                    let fracHTML = `
                        <div class="flex flex-col items-center text-[0.65em] leading-none mx-0.5 relative top-[-2px]">
                            <span class="frac-line w-full text-center pb-0.5 sm:pb-1">${n}</span>
                            <span class="pt-0.5 sm:pt-1">${d}</span>
                        </div>`;
                        
                    // [수정됨] 분수 거듭제곱도 지수를 위쪽으로 끌어올림
                    qHtml = `<span class="flex items-start">
                                <span class="flex items-center"><span>(</span><span>${sign}</span>${fracHTML}<span>)</span></span>
                                <span class="text-[0.65em] font-bold ml-0.5 -mt-1 sm:-mt-2">${exp}</span>
                             </span>`;
                             
                    let top = Math.pow(n, exp);
                    let bot = Math.pow(d, exp);
                    if (isNeg && exp % 2 !== 0) top = -top;
                    ansStr = simplify(top, bot);
                }
                hintMsg.style.opacity = 1;
            } 
            else if (problemType === 4) {
                // Lv.4 정수 및 분수의 나눗셈
                let type = Math.random() < 0.5 ? 'int' : 'frac';
                if (type === 'int') {
                    let a = getRandomInt(-20, 20);
                    let b = getRandomInt(-10, 10);
                    if (a === 0) a = 8; if (b === 0) b = -4;
                    
                    let signA = `${a}`;
                    let signB = b > 0 ? `${b}` : `(${b})`;
                    
                    qHtml = `<span>${signA}</span> <span class="mx-1 text-blue-500">÷</span> <span>${signB}</span>`;
                    ansStr = simplify(a, b);
                } else {
                    let d1 = getRandomInt(2, 6);
                    let d2 = getRandomInt(2, 6);
                    let n1 = getRandomInt(1, d1 - 1) * (Math.random() < 0.5 ? 1 : -1);
                    let n2 = getRandomInt(1, d2 - 1) * (Math.random() < 0.5 ? 1 : -1);

                    qHtml = `${createFractionHTML(n1, d1, true)} <span class="mx-1 text-blue-500">÷</span> ${createFractionHTML(n2, d2, false)}`;
                    ansStr = simplify(n1 * d2, d1 * n2);
                }
                hintMsg.style.opacity = 1;
            } 
            else if (problemType === 5) {
                // Lv.5 유리수의 혼합 (곱셈/나눗셈 랜덤 섞임)
                hintMsg.style.opacity = 1;
                
                let d1 = getRandomInt(2, 6);
                let d2 = getRandomInt(2, 6);
                let n1 = getRandomInt(1, d1 - 1) * (Math.random() < 0.5 ? 1 : -1);
                let n2 = getRandomInt(1, d2 - 1) * (Math.random() < 0.5 ? 1 : -1);
                let isMul = Math.random() < 0.5;

                qHtml = `${createFractionHTML(n1, d1, true)} <span class="mx-1 text-blue-500">${isMul ? '×' : '÷'}</span> ${createFractionHTML(n2, d2, false)}`;

                if (isMul) {
                    ansStr = simplify(n1 * n2, d1 * d2);
                } else {
                    ansStr = simplify(n1 * d2, d1 * n2);
                }
            }
            else if (problemType === 6) {
                // Lv.6 덧셈의 귀환 (정수/음수와 유리수 덧셈·뺄셈 복습)
                let mode = Math.random();
                if (mode < 0.4) {
                    let a = getRandomInt(-10, 10);
                    let b = getRandomInt(1, 10);
                    let isAdd = Math.random() < 0.5;
                    qHtml = `<span>${a}</span> <span class="mx-1 text-blue-500">${isAdd ? '+' : '-'}</span> <span>${b}</span>`;
                    ansStr = isAdd ? (a + b).toString() : (a - b).toString();
                    hintMsg.style.opacity = 0;
                } else if (mode < 0.75) {
                    let a = getRandomInt(-10, 10);
                    let b = getRandomInt(-10, 10);
                    if (a === 0) a = 2; if (b === 0) b = -3;
                    let isAdd = Math.random() < 0.5;
                    let signA = `${a}`;
                    let signB = b > 0 ? `${b}` : `(${b})`;
                    qHtml = `<span>${signA}</span> <span class="mx-1 text-blue-500">${isAdd ? '+' : '-'}</span> <span>${signB}</span>`;
                    ansStr = isAdd ? (a + b).toString() : (a - b).toString();
                    hintMsg.style.opacity = 0;
                } else {
                    hintMsg.style.opacity = 1;
                    let d1 = getRandomInt(2, 6);
                    let d2 = getRandomInt(2, 6);
                    let n1 = getRandomInt(1, d1 - 1) * (Math.random() < 0.5 ? 1 : -1);
                    let n2 = getRandomInt(1, d2 - 1) * (Math.random() < 0.5 ? 1 : -1);
                    let isAdd = Math.random() < 0.5;
                    qHtml = `${createFractionHTML(n1, d1, true)} <span class="mx-1 text-blue-500">${isAdd ? '+' : '-'}</span> ${createFractionHTML(n2, d2, false)}`;
                    let top = isAdd ? (n1 * d2 + n2 * d1) : (n1 * d2 - n2 * d1);
                    let bottom = d1 * d2;
                    ansStr = simplify(top, bottom);
                }
            }

            qHtml += `<span class="ml-1 sm:ml-2 text-gray-400">= ?</span>`;
            questionBox.innerHTML = qHtml;
            expectedAnswer = ansStr;

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
                questionStartTime = Date.now(); 
            }, 2000);
        }

        function showGameOver() {
            gameOverOverlay.classList.remove('hidden');
            document.getElementById('final-score').innerText = score;
            let finalAvg = solvedCount === 0 ? "0.0" : ((totalTimeMs / solvedCount) / 1000).toFixed(1);
            document.getElementById('final-avg-time').innerText = finalAvg + "초";
            document.getElementById('final-max-combo').innerText = maxCombo;
        }

        function checkAnswer() {
            if (currentInput === "" || lives <= 0 || isChecking) return;
            isChecking = true;

            if (currentInput === expectedAnswer) {
                let timeTaken = Date.now() - questionStartTime;
                totalTimeMs += timeTaken;
                solvedCount++;
                score += 1;
                combo += 1;
                if (combo > maxCombo) maxCombo = combo;
                
                feedbackMsg.innerText = PRAISES[Math.floor(Math.random() * PRAISES.length)];
                feedbackMsg.classList.remove('opacity-0', 'text-red-500');
                feedbackMsg.classList.add('opacity-100', 'text-green-500', 'pop');
                updateUI();
                
                setTimeout(() => {
                    feedbackMsg.classList.remove('pop', 'opacity-100');
                    feedbackMsg.classList.add('opacity-0');
                    generateQuestion();
                    isChecking = false;
                }, 800);
            } else {
                combo = 0;
                lives--;
                updateUI();

                if (lives <= 0) {
                    showGameOver();
                    isChecking = false;
                    return;
                }

                inputBox.classList.remove('shake');
                void inputBox.offsetWidth; 
                inputBox.classList.add('shake');
                currentInput = ""; inputBox.innerText = "";
                
                feedbackMsg.innerText = "앗, 다시 계산해볼까요? 😅";
                feedbackMsg.classList.remove('opacity-0', 'text-green-500');
                feedbackMsg.classList.add('opacity-100', 'text-red-500');
                
                setTimeout(() => {
                    feedbackMsg.classList.remove('opacity-100');
                    feedbackMsg.classList.add('opacity-0');
                    isChecking = false;
                }, 1500);
            }
        }

        function updateUI() {
            scoreEl.innerText = score;
            levelBadgeEl.innerText = LEVEL_TITLES[level-1];
            livesDisplay.innerText = '❤️'.repeat(lives) + '🖤'.repeat(5 - lives); 
            
            let avgSec = solvedCount === 0 ? "0.0" : ((totalTimeMs / solvedCount) / 1000).toFixed(1);
            avgTimeDisplay.innerText = avgSec + "초";
            
            if (combo >= 2) comboEl.innerText = `${combo} 콤보! 🔥`;
            else comboEl.innerText = "";
            
            maxComboEl.innerText = `최고 콤보: ${maxCombo}`;

            let maxScore = LEVEL_THRESHOLDS[level] !== undefined ? LEVEL_THRESHOLDS[level] : LEVEL_THRESHOLDS[LEVEL_THRESHOLDS.length - 1] + 10;
            let minScore = LEVEL_THRESHOLDS[level-1];
            let percent = ((score - minScore) / (maxScore - minScore)) * 100;
            if (percent > 100) percent = 100;
            if (level >= LEVEL_THRESHOLDS.length) percent = 100; 
            
            progressBarEl.style.width = `${percent}%`;
        }

        document.addEventListener('keydown', (e) => {
            const key = e.key;
            if (key >= '0' && key <= '9') inputKey(key);
            else if (key === '-' || key === '/') inputKey(key);
            else if (key === 'Backspace') inputKey('DEL');
            else if (key === 'Enter') checkAnswer();
        });

        init();

    </script>
</body>
</html>
'''

# 4. 스트림릿 컴포넌트로 렌더링
components.html(html_code, height=560)
