import json
import streamlit as st
import streamlit.components.v1 as components

telegram_config = st.secrets.get("Telegram", {})
telegram_token = telegram_config.get("Token", "")
telegram_chat_id = telegram_config.get("chat_id", "")

html_code='''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>다항식 챌린지</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Jua&display=swap" rel="stylesheet">
    
    <style>
        /* 배경 흰색, 스크롤 방지 */
        body {
            font-family: 'Jua', sans-serif;
            background-color: #ffffff;
            touch-action: manipulation;
            margin: 0;
            padding: 0;
            width: 100vw;
            height: 100vh;
            overflow: hidden;
            color: #334155;
        }
        
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            20%, 60% { transform: translateX(-5px); }
            40%, 80% { transform: translateX(5px); }
        }
        .shake { animation: shake 0.4s ease-in-out; }

        @keyframes pop {
            0% { transform: scale(0.5); opacity: 0; }
            50% { transform: scale(1.1); opacity: 1; }
            100% { transform: scale(1); opacity: 1; }
        }
        .pop { animation: pop 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }

        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-5px); }
        }
        .float { animation: float 2s ease-in-out infinite; }

        .key-btn { transition: transform 0.05s, background-color 0.1s; }
        .key-btn:active { transform: scale(0.92); background-color: #e2e8f0; }

        .frac-line { border-bottom: 2px solid currentColor; }
        
        @media (max-width: 768px) {
            #keypad-panel { padding: 0.75rem; }
            .key-btn { padding: 0.75rem 0.65rem !important; font-size: 1.35rem !important; min-height: 1.875rem !important; }
            #game-container { padding-bottom: 0.5rem; }
            #expression-box { min-height: 50px; font-size: 1.95rem; line-height: 1.05; }
            #input-box { font-size: 1.9rem; line-height: 1.1; }
            .text-6xl { font-size: 2.4rem; }
            .text-5xl { font-size: 2rem; }
        }

        ::-webkit-scrollbar { width: 0px; background: transparent; }
    </style>
</head>
<body class="flex items-center justify-center">

    <!-- [시작 화면] 이름 입력 -->
    <div id="intro-screen" class="absolute inset-0 z-50 bg-white flex flex-col justify-center items-center p-6">
        <div class="text-center pop w-full max-w-sm">
            <div class="text-6xl mb-4 float">🏃‍♂️</div>
            <h1 class="text-4xl sm:text-5xl font-bold text-indigo-500 mb-2">다항식 챌린지</h1>
            <p class="text-base text-slate-500 mb-8">항, 계수, 차수를 완벽히 정복하자!</p>
            
            <div class="bg-indigo-50/50 p-6 rounded-3xl w-full">
                <input type="text" id="player-name-input" placeholder="플레이어 이름" class="w-full bg-white text-slate-800 text-xl font-bold p-4 rounded-xl focus:ring-4 focus:ring-indigo-300 focus:outline-none mb-6 text-center placeholder-slate-300 shadow-sm" autocomplete="off">
                <button onclick="startGame()" class="w-full bg-indigo-500 hover:bg-indigo-600 text-white font-bold text-xl py-4 rounded-xl transition-all active:scale-95 shadow-md">
                    챌린지 시작
                </button>
            </div>
        </div>
    </div>

    <!--[게임 오버 화면] ⬅️ 여기로 꺼냈습니다! -->
    <div id="gameover-screen" class="absolute inset-0 z-50 bg-white flex flex-col justify-center items-center p-6 hidden">
        <div class="text-center pop w-full max-w-sm">
            <div class="text-6xl mb-4 float">😭</div>
            <h1 class="text-4xl sm:text-5xl font-bold text-indigo-500 mb-2">게임 종료!</h1>
            <p class="text-base text-slate-500 mb-8">하트를 모두 소진했습니다.</p>
            
            <div class="bg-indigo-50/50 p-6 rounded-3xl w-full border border-indigo-100 mb-6 shadow-sm">
                <p class="text-lg sm:text-xl text-slate-600 mb-3 font-bold">최종 점수: <span id="final-score" class="text-indigo-600 text-2xl sm:text-3xl">0</span></p>
                <p class="text-lg sm:text-xl text-slate-600 mb-3 font-bold">최고 콤보: <span id="final-max-combo" class="text-orange-500 text-xl sm:text-2xl">0</span></p>
                <p class="text-lg sm:text-xl text-slate-600 font-bold">평균 기록: <span id="final-avg-time" class="text-emerald-500 text-xl sm:text-2xl">0.0초</span></p>
            </div>
            <button onclick="location.reload()" class="w-full bg-indigo-500 hover:bg-indigo-600 text-white font-bold text-xl py-4 rounded-xl transition-all active:scale-95 shadow-md">
                다시 도전하기
            </button>
        </div>
    </div>

    <!-- 메인 컨테이너 -->
    <div id="game-container" class="w-full h-full bg-white flex flex-col md:flex-row relative hidden">
        
        <!--[왼쪽 영역] 게임 화면 -->
        <div class="flex-1 flex flex-col relative min-h-0">
            
            <!-- 상단 헤더 상태창 -->
            <div class="bg-indigo-50/70 p-3 sm:p-5 z-10 rounded-b-3xl mx-2 shadow-sm">
                <div class="flex justify-between items-end mb-2">
                    <div class="flex flex-col gap-1 sm:gap-2">
                        <div class="flex items-center gap-2">
                            <span id="player-name-display" class="text-indigo-700 font-bold text-base sm:text-lg">학생</span>
                            <span id="level-badge" class="bg-indigo-200 text-indigo-800 px-3 py-1 rounded-full text-xs sm:text-sm font-bold shadow-sm">
                                Lv.1 시작
                            </span>
                        </div>
                        <div class="text-sm font-bold tracking-widest text-rose-400 mt-1" id="lives-display">❤️❤️❤️❤️❤️</div>
                    </div>
                    
                    <!-- 우측 점수 및 통계 패널 -->
                    <div class="text-right flex flex-col justify-end items-end gap-1 sm:gap-2">
                        <div class="flex items-center text-sm sm:text-base font-bold">
                            <span id="combo-display" class="text-orange-500 mr-3 opacity-0 transition-opacity duration-200">0 콤보! 🔥</span>
                            <span class="text-slate-500">평균: <span id="avg-time" class="text-emerald-500">0.0</span>초</span>
                        </div>
                        <div class="flex items-center text-sm sm:text-base font-bold">
                            <span class="text-orange-500 mr-3">최고 콤보: <span id="max-combo">0</span></span>
                            <span class="text-slate-700">점수: <span id="score" class="text-indigo-600 text-xl sm:text-2xl">0</span></span>
                        </div>
                    </div>
                </div>
                <!-- 경험치 진행률 바 -->
                <div class="w-full bg-indigo-200 rounded-full h-2 sm:h-3 mt-2 overflow-hidden shadow-inner">
                    <div id="progress-bar" class="bg-gradient-to-r from-indigo-400 to-purple-400 h-full rounded-full transition-all duration-300" style="width: 0%"></div>
                </div>
            </div>

            <!-- 게임 진행 화면 -->
            <div id="game-play-area" class="flex flex-col items-center justify-center p-2 sm:p-4 relative overflow-y-auto max-h-[380px] sm:max-h-[450px]">
                
                <!-- 레벨업 알림 -->
                <div id="levelup-overlay" class="absolute inset-0 bg-white/90 flex items-center justify-center hidden z-20 backdrop-blur-sm">
                    <div class="text-center pop">
                        <div class="text-6xl mb-4">🌟</div>
                        <h2 class="text-3xl sm:text-4xl font-bold text-indigo-500">레벨 업!</h2>
                        <p id="levelup-msg" class="text-base sm:text-lg text-slate-500 mt-2 font-bold">새로운 챌린지가 열렸습니다.</p>
                    </div>
                </div>

                <!-- 피드백 메시지 -->
                <div id="feedback-msg" class="text-lg sm:text-xl font-bold text-emerald-500 h-8 transition-all opacity-0 mb-2">Great!</div>

                <!-- 수식 및 질문 컨테이너 -->
                <div class="bg-slate-50/50 rounded-3xl p-0 w-full max-w-md flex flex-col items-center">
                    <div id="expression-box" class="flex flex-wrap items-center justify-center gap-x-1 gap-y-2 text-4xl sm:text-5xl font-bold text-slate-800 mb-[5px] text-center min-h-[60px] w-full">
                        <!-- 다항식 렌더링 -->
                    </div>
                    
                    <!-- 질문 렌더링 -->
                    <div id="question-box" class="text-xl sm:text-2xl text-slate-700 font-bold text-center w-full break-keep px-2">
                        질문이 들어갑니다.
                    </div>
                </div>

                <!-- 텍스트 입력 칸 -->
                <div id="input-box" class="w-full max-w-[260px] text-center border-b-4 border-indigo-400 text-3xl sm:text-4xl text-indigo-600 font-bold py-0 h-16 sm:h-20 bg-indigo-50/30 rounded-t-2xl flex items-center justify-center overflow-hidden tracking-widest">
                </div>
                
                <!-- 예/아니오 선택 버튼 -->
                <div id="choice-panel" class="hidden w-full max-w-[280px] flex gap-4 mt-6">
                    <!-- JS에서 생성됨 -->
                </div>
            </div>
        </div>

        <!--[오른쪽 영역 / 모바일 하단] 다항식 전용 키패드 -->
        <div id="keypad-panel" class="w-full md:w-[300px] lg:w-[340px] bg-slate-50 p-3 sm:p-4 flex flex-col justify-center border-t md:border-t-0 md:border-l border-slate-200 z-10 shrink-0 rounded-t-3xl md:rounded-none">
            <div class="grid grid-cols-4 gap-2 w-full h-full md:h-auto max-w-sm mx-auto">
                <button class="key-btn bg-white shadow-sm border border-slate-200 rounded-2xl text-2xl font-bold py-3 md:py-4 text-slate-700" onclick="inputKey('1')">1</button>
                <button class="key-btn bg-white shadow-sm border border-slate-200 rounded-2xl text-2xl font-bold py-3 md:py-4 text-slate-700" onclick="inputKey('2')">2</button>
                <button class="key-btn bg-white shadow-sm border border-slate-200 rounded-2xl text-2xl font-bold py-3 md:py-4 text-slate-700" onclick="inputKey('3')">3</button>
                <button class="key-btn bg-slate-200 shadow-sm border border-slate-300 rounded-2xl text-base font-bold py-3 md:py-4 text-slate-600" onclick="inputKey('DEL')">지움</button>

                <button class="key-btn bg-white shadow-sm border border-slate-200 rounded-2xl text-2xl font-bold py-3 md:py-4 text-slate-700" onclick="inputKey('4')">4</button>
                <button class="key-btn bg-white shadow-sm border border-slate-200 rounded-2xl text-2xl font-bold py-3 md:py-4 text-slate-700" onclick="inputKey('5')">5</button>
                <button class="key-btn bg-white shadow-sm border border-slate-200 rounded-2xl text-2xl font-bold py-3 md:py-4 text-slate-700" onclick="inputKey('6')">6</button>
                <button class="key-btn bg-indigo-100 shadow-sm border border-indigo-200 rounded-2xl text-xl font-bold py-3 md:py-4 text-indigo-600" onclick="inputKey('²')">²</button>

                <button class="key-btn bg-white shadow-sm border border-slate-200 rounded-2xl text-2xl font-bold py-3 md:py-4 text-slate-700" onclick="inputKey('7')">7</button>
                <button class="key-btn bg-white shadow-sm border border-slate-200 rounded-2xl text-2xl font-bold py-3 md:py-4 text-slate-700" onclick="inputKey('8')">8</button>
                <button class="key-btn bg-white shadow-sm border border-slate-200 rounded-2xl text-2xl font-bold py-3 md:py-4 text-slate-700" onclick="inputKey('9')">9</button>
                <button class="key-btn bg-indigo-100 shadow-sm border border-indigo-200 rounded-2xl text-3xl font-bold py-3 md:py-4 text-indigo-600 pb-6" onclick="inputKey(',')">,</button>

                <button class="key-btn bg-indigo-50 shadow-sm border border-indigo-100 rounded-2xl text-3xl font-bold py-3 md:py-4 text-indigo-500" onclick="inputKey('-')">-</button>
                <button class="key-btn bg-indigo-100 shadow-sm border border-indigo-200 rounded-2xl text-2xl font-bold italic py-3 md:py-4 text-indigo-600" onclick="inputKey('x')">x</button>
                <button class="key-btn bg-indigo-100 shadow-sm border border-indigo-200 rounded-2xl text-2xl font-bold italic py-3 md:py-4 text-indigo-600" onclick="inputKey('y')">y</button>
                <button id="submit-btn" class="key-btn bg-indigo-500 hover:bg-indigo-600 border border-indigo-600 shadow-md rounded-2xl text-xl font-bold py-3 md:py-4 text-white" onclick="checkTextAnswer()">확인</button>
            </div>
        </div>
    </div>

    <script>
        let playerName = "학생";
        let score = 0;
        let combo = 0;
        let maxCombo = 0; 
        let level = 1;
        let lives = 5;
        
        let expectedAnswer =[]; 
        let currentInput = "";
        let currentQType = "text"; 
        let isChecking = false;
        let wrongCount = 0;
        
        let totalTimeMs = 0;
        let solvedCount = 0;
        let questionStartTime = 0;

        const TELEGRAM_TOKEN = TELEGRAM_TOKEN_PLACEHOLDER;
        const TELEGRAM_CHAT_ID = TELEGRAM_CHAT_ID_PLACEHOLDER;

        function sendTelegram(message) {
            if (!TELEGRAM_TOKEN || !TELEGRAM_CHAT_ID || !playerName || playerName === "학생") return;
            fetch(`https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    chat_id: TELEGRAM_CHAT_ID,
                    text: message
                })
            }).catch((error) => console.error("Telegram 전송 실패:", error));
        }

        function notifyLevelUp(levelName) {
            sendTelegram(`${playerName}님이 레벨업했습니다! 🎉\\n현재 단계: ${levelName}`);
        }

        function notifyWrongAnswer(levelNumber) {
            sendTelegram(`${playerName}님이 레벨 ${levelNumber}에서 틀렸습니다. ⚠️`);
        }

        function sendGameOverSummary() {
            const avgSec = solvedCount === 0 ? "0.0" : ((totalTimeMs / solvedCount) / 1000).toFixed(1);
            sendTelegram(`${playerName}님 챌린지 종료 📌\\n최종 점수: ${score}\\n최고 콤보: ${maxCombo}\\n평균 풀이: ${avgSec}초\\n레벨: ${LEVEL_TITLES[level-1]}`);
        }

        const LEVEL_THRESHOLDS =[0, 5, 15, 25, 35]; 
        const LEVEL_TITLES =["Lv.1 항과 상수항", "Lv.2 계수 찾기", "Lv.3 차수 판별", "Lv.4 다항식 분류", "Lv.5 마스터 챌린지"];
        const PRAISES =["정확해요! 👏", "최고예요! ⭐", "완벽합니다! ✨", "나이스! 😊", "정답! 💯"];

        const introScreen = document.getElementById('intro-screen');
        const gameContainer = document.getElementById('game-container');
        // ⬅️ 새로운 게임오버 화면 불러오기
        const gameOverScreen = document.getElementById('gameover-screen'); 
        
        const scoreEl = document.getElementById('score');
        const comboEl = document.getElementById('combo-display');
        const maxComboEl = document.getElementById('max-combo');
        const levelBadgeEl = document.getElementById('level-badge');
        const progressBarEl = document.getElementById('progress-bar');
        const livesDisplay = document.getElementById('lives-display');
        const avgTimeDisplay = document.getElementById('avg-time');
        
        const expressionBox = document.getElementById('expression-box');
        const questionBox = document.getElementById('question-box');
        const inputBox = document.getElementById('input-box');
        const choicePanel = document.getElementById('choice-panel');
        const keypadPanel = document.getElementById('keypad-panel');
        
        const feedbackMsg = document.getElementById('feedback-msg');
        const levelUpOverlay = document.getElementById('levelup-overlay');
        const levelUpMsg = document.getElementById('levelup-msg');

        function startGame() {
            const nameInput = document.getElementById('player-name-input').value.trim();
            if(nameInput !== "") playerName = nameInput;
            document.getElementById('player-name-display').innerText = playerName;
            
            introScreen.classList.add('hidden');
            gameContainer.classList.remove('hidden');
            
            sendTelegram(`${playerName}님이 다항식 챌린지를 시작하였습니다.`);
            init();
        }

        function init() {
            keypadPanel.style.display = '';
            const gamePlayArea = document.getElementById('game-play-area');
            if (window.innerWidth <= 768) {
                gamePlayArea.style.maxHeight = '';
            }
            score = 0; combo = 0; maxCombo = 0; level = 1; lives = 5;
            totalTimeMs = 0; solvedCount = 0;
            updateUI();
            generateQuestion();
        }

        function inputKey(key) {
            if (lives <= 0 || currentQType === 'choice') return; 
            if (key === 'DEL') currentInput = currentInput.slice(0, -1);
            else if (key === 'CLEAR') currentInput = "";
            else { if (currentInput.length < 15) currentInput += key; }
            inputBox.innerText = currentInput;
        }

        function getRandomInt(min, max) { return Math.floor(Math.random() * (max - min + 1)) + min; }

        function generatePolynomial(termCount) {
            const varPool =[
                {v: 'x', exp: 1}, {v: 'x', exp: 2},
                {v: 'y', exp: 1}, {v: 'y', exp: 2}
            ];

            let selectedTerms =[];

            if (termCount === 3) {
                varPool.sort(() => Math.random() - 0.5);
                selectedTerms = varPool.slice(0, 2);
                selectedTerms.push({v: '', exp: 0});
            } else {
                const fullPool = [...varPool, {v: '', exp: 0}];
                fullPool.sort(() => Math.random() - 0.5);
                selectedTerms = fullPool.slice(0, termCount);
            }

            selectedTerms.sort((a, b) => {
                if (a.v === b.v) return b.exp - a.exp; 
                if (a.v === 'x') return -1;
                if (a.v === 'y' && b.v === '') return -1;
                return 1;
            });

            let finalTerms = selectedTerms.map(t => {
                let coef = getRandomInt(1, 9) * (Math.random() < 0.5 ? 1 : -1);
                return { coef, denom: 1, v: t.v, exp: t.exp };
            });

            return finalTerms;
        }

        function formatTerm(coef, denom, v, exp, isFirst) {
            let sign = '';
            if (coef < 0) sign = '-';
            else if (!isFirst) sign = '+';

            let num = Math.abs(coef);
            let coefHtml = '';

            if (num === 1 && denom === 1 && v !== '') coefHtml = ''; 
            else if (denom === 1) coefHtml = `${num}`;
            else {
                coefHtml = `
                <div class="flex flex-col items-center text-[0.65em] leading-none mx-0.5 sm:mx-1 relative top-[-3px]">
                    <span class="frac-line w-full text-center pb-0.5">${num}</span>
                    <span class="pt-0.5">${denom}</span>
                </div>`;
            }

            let varHtml = '';
            if (v) {
                varHtml = `<span class="italic text-indigo-500">${v}</span>`;
                if (exp === 2) varHtml += `<span class="text-[0.6em] -mt-2 ml-0.5 text-slate-500">2</span>`;
            }

            return `<span class="flex items-center mx-1"><span>${sign}</span>${coefHtml}${varHtml}</span>`;
        }

        function getValidTermRepresentations(coef, denom, v, exp) {
            let valids =[];
            let num = Math.abs(coef);
            let sign = coef < 0 ? "-" : "";
            let signPlus = coef > 0 ? "+" : "";

            let varPart = v;
            if(v && exp === 2) varPart += '²';

            if (v === '') { 
                if(denom === 1) {
                    valids.push(`${sign}${num}`);
                    if(coef > 0) valids.push(`${signPlus}${num}`);
                } else {
                    valids.push(`${sign}${num}/${denom}`);
                    if(coef > 0) valids.push(`${signPlus}${num}/${denom}`);
                }
            } else { 
                if (denom === 1) {
                    if (num === 1) {
                        valids.push(`${sign}${varPart}`); 
                        valids.push(`${sign}1${varPart}`); 
                        if (coef > 0) {
                            valids.push(`${signPlus}${varPart}`);
                            valids.push(`${signPlus}1${varPart}`);
                        }
                    } else {
                        valids.push(`${sign}${num}${varPart}`); 
                        if (coef > 0) valids.push(`${signPlus}${num}${varPart}`);
                    }
                } else {
                    valids.push(`${sign}${num}/${denom}${varPart}`); 
                    if (coef > 0) valids.push(`${signPlus}${num}/${denom}${varPart}`);
                    if (num === 1) {
                        valids.push(`${sign}${varPart}/${denom}`); 
                        if (coef > 0) valids.push(`${signPlus}${varPart}/${denom}`);
                    }
                }
            }
            return valids;
        }

        function getValidCoefRepresentations(coef, denom) {
            let valids =[];
            let num = Math.abs(coef);
            let sign = coef < 0 ? "-" : "";
            let signPlus = coef > 0 ? "+" : "";

            if (denom === 1) {
                valids.push(`${sign}${num}`);
                if (coef > 0) valids.push(`${signPlus}${num}`);
            } else {
                valids.push(`${sign}${num}/${denom}`);
                if (coef > 0) valids.push(`${signPlus}${num}/${denom}`);
            }
            return valids;
        }

        function setChoiceOptions(options) {
            choicePanel.innerHTML = '';
            options.forEach(opt => {
                let btn = document.createElement('button');
                btn.className = "flex-1 bg-white hover:bg-slate-50 text-indigo-600 font-bold py-3 sm:py-4 rounded-xl border-2 border-indigo-200 active:scale-95 transition-transform text-lg shadow-sm";
                btn.innerText = opt;
                btn.onclick = () => checkChoiceAnswer(opt);
                choicePanel.appendChild(btn);
            });
        }

        function generateQuestion() {
            currentInput = ""; inputBox.innerText = ""; inputBox.classList.remove('shake');
            
            let newLevel = 1;
            if (score >= LEVEL_THRESHOLDS[4]) newLevel = 5;
            else if (score >= LEVEL_THRESHOLDS[3]) newLevel = 4;
            else if (score >= LEVEL_THRESHOLDS[2]) newLevel = 3;
            else if (score >= LEVEL_THRESHOLDS[1]) newLevel = 2;

            let isLevelUp = false;
            if (newLevel > level) { level = newLevel; isLevelUp = true; }
            updateUI();

            if (isLevelUp) {
                showLevelUp();
                return;
            }

            let problemType = level;
            if (level === 5) {
                problemType = getRandomInt(1, 4); 
            } else if (level > 1 && Math.random() < 0.4) {
                problemType = getRandomInt(1, level - 1);
            }

            let termCount = (problemType === 4 && Math.random() < 0.3) ? 1 : getRandomInt(2, 3); 
            let terms = generatePolynomial(termCount);

            let exprHtml = "";
            let allTermsValids =[]; 
            
            terms.forEach((t, i) => {
                exprHtml += formatTerm(t.coef, t.denom, t.v, t.exp, i === 0);
                allTermsValids.push(getValidTermRepresentations(t.coef, t.denom, t.v, t.exp));
            });
            expressionBox.innerHTML = exprHtml;

            inputBox.classList.remove('hidden');
            choicePanel.classList.add('hidden');
            keypadPanel.style.opacity = "1";
            keypadPanel.style.pointerEvents = "auto";
            currentQType = "text";
            questionStartTime = Date.now();

            if (problemType === 1) {
                let constTermIdx = terms.findIndex(t => t.v === '');
                if(Math.random() < 0.5 && constTermIdx !== -1) {
                    questionBox.innerText = "상수항은 무엇인가요?";
                    expectedAnswer = getValidTermRepresentations(terms[constTermIdx].coef, terms[constTermIdx].denom, '', 0);
                } else {
                    questionBox.innerHTML = "항을 <span class='text-rose-500'>모두</span> 쓰시오. (쉼표로 구분)";
                    currentQType = "terms";
                    expectedAnswer = allTermsValids; 
                }
            } 
            else if (problemType === 2) {
                let varTerms = terms.filter(t => t.v !== '');
                if(varTerms.length === 0) varTerms = terms; 
                let target = varTerms[Math.floor(Math.random() * varTerms.length)];
                let tName = target.v + (target.exp === 2 ? '²' : '');
                
                questionBox.innerHTML = `<span class="italic text-indigo-500">${tName}</span> 의 계수는?`;
                expectedAnswer = getValidCoefRepresentations(target.coef, target.denom);
            }
            else if (problemType === 3) {
                if(Math.random() < 0.5) {
                    let varTerms = terms.filter(t => t.v !== '');
                    if(varTerms.length > 0) {
                        let target = varTerms[Math.floor(Math.random() * varTerms.length)];
                        let repStr = getValidTermRepresentations(target.coef, target.denom, target.v, target.exp)[0]; 
                        questionBox.innerHTML = `항 <span class="bg-indigo-100 text-indigo-600 px-2 rounded">[ ${repStr} ]</span> 의 차수는?`;
                        expectedAnswer =[target.exp.toString()];
                    } else {
                        questionBox.innerText = `다항식의 차수는?`;
                        expectedAnswer = ["0"];
                    }
                } else {
                    questionBox.innerText = `이 다항식의 차수는?`;
                    let maxDegree = Math.max(...terms.map(t => t.exp));
                    expectedAnswer = [maxDegree.toString()];
                }
            }
            else if (problemType === 4) {
                inputBox.classList.add('hidden');
                choicePanel.classList.remove('hidden');
                keypadPanel.style.opacity = "0.4"; 
                keypadPanel.style.pointerEvents = "none";
                currentQType = "choice";
                
                let maxDegree = Math.max(...terms.map(t => t.exp));
                let isMonomial = terms.length === 1;
                let isPolynomial = true; 
                let isLinear = maxDegree === 1;

                let qRand = Math.random();
                setChoiceOptions(['예', '아니오']);

                if (qRand < 0.33) {
                    questionBox.innerText = `이 식은 단항식인가요?`;
                    expectedAnswer = isMonomial ? ["예"] :["아니오"];
                } else if (qRand < 0.66) {
                    questionBox.innerText = `이 식은 다항식인가요?`;
                    expectedAnswer = isPolynomial ?["예"] : ["아니오"];
                } else {
                    questionBox.innerText = `이 식은 일차식인가요?`;
                    expectedAnswer = isLinear ? ["예"] : ["아니오"];
                }
            }

            if (isLevelUp) {
                showLevelUp();
            } else {
                questionStartTime = Date.now();
            }
        }

        function checkTextAnswer() {
            if (currentQType === "choice" || currentInput === "" || lives <= 0 || isChecking) return;
            isChecking = true;

            let isCorrect = false;

            if(currentQType === "terms") {
                let userArr = currentInput.split(',').map(s => s.trim());
                
                if (userArr.length === expectedAnswer.length) {
                    let matched = new Array(expectedAnswer.length).fill(false);
                    let allMatch = true;
                    
                    for (let uTerm of userArr) {
                        let found = false;
                        for (let i = 0; i < expectedAnswer.length; i++) {
                            if (!matched[i] && expectedAnswer[i].includes(uTerm)) {
                                matched[i] = true;
                                found = true;
                                break;
                            }
                        }
                        if (!found) { allMatch = false; break; }
                    }
                    isCorrect = allMatch;
                }
            } else {
                isCorrect = expectedAnswer.includes(currentInput.trim());
            }

            processResult(isCorrect);
        }

        function checkChoiceAnswer(choice) {
            if (currentQType !== "choice" || lives <= 0 || isChecking) return;
            isChecking = true;
            processResult(expectedAnswer.includes(choice));
        }

        function processResult(isCorrect) {
            if (isCorrect) {
                let timeTaken = Date.now() - questionStartTime;
                totalTimeMs += timeTaken;
                solvedCount++;
                
                score += 1; 
                combo += 1;
                maxCombo = Math.max(maxCombo, combo);
                
                feedbackMsg.innerText = PRAISES[Math.floor(Math.random() * PRAISES.length)];
                feedbackMsg.classList.remove('opacity-0', 'text-rose-500');
                feedbackMsg.classList.add('opacity-100', 'text-emerald-500', 'pop');
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
                wrongCount += 1;
                notifyWrongAnswer(level);
                updateUI();

                if (lives <= 0) {
                    showGameOver();
                    return;
                }

                if(currentQType !== 'choice') {
                    inputBox.classList.remove('shake');
                    void inputBox.offsetWidth; 
                    inputBox.classList.add('shake');
                    currentInput = ""; inputBox.innerText = "";
                } else {
                    choicePanel.classList.remove('shake');
                    void choicePanel.offsetWidth;
                    choicePanel.classList.add('shake');
                }
                
                feedbackMsg.innerText = "앗, 다시 확인해볼까요? 🥲";
                feedbackMsg.classList.remove('opacity-0', 'text-emerald-500');
                feedbackMsg.classList.add('opacity-100', 'text-rose-500');
                
                setTimeout(() => {
                    feedbackMsg.classList.remove('opacity-100');
                    feedbackMsg.classList.add('opacity-0');
                    isChecking = false;
                }, 1500);
            }
        }

        // ⬅️ [중요] 게임 오버 처리가 수정된 부분
        function showGameOver() {
            // 게임 컨테이너 자체를 완전히 숨깁니다 (CSS 충돌 원천 차단)
            gameContainer.classList.add('hidden');
            
            // 바깥으로 빼낸 게임오버 스크린을 표시합니다.
            gameOverScreen.classList.remove('hidden');
            
            document.getElementById('final-score').innerText = score;
            document.getElementById('final-max-combo').innerText = maxCombo;
            let finalAvg = solvedCount === 0 ? "0.0" : ((totalTimeMs / solvedCount) / 1000).toFixed(1);
            document.getElementById('final-avg-time').innerText = finalAvg + "초";
            
            sendGameOverSummary();
        }

        function showLevelUp() {
            levelUpMsg.innerText = LEVEL_TITLES[level-1] + " 등장!";
            levelUpOverlay.classList.remove('hidden');
            setTimeout(() => { 
                levelUpOverlay.classList.add('hidden'); 
                questionStartTime = Date.now();
                generateQuestion();
            }, 2000);
        }

        function updateUI() {
            scoreEl.innerText = score;
            document.getElementById('max-combo').innerText = maxCombo;
            levelBadgeEl.innerText = LEVEL_TITLES[level-1];
            livesDisplay.innerText = '❤️'.repeat(lives) + '🖤'.repeat(5 - lives); 
            
            let avgSec = solvedCount === 0 ? "0.0" : ((totalTimeMs / solvedCount) / 1000).toFixed(1);
            avgTimeDisplay.innerText = avgSec;
            
            if (combo >= 2) {
                comboEl.innerText = `${combo} 콤보! 🔥`;
                comboEl.classList.remove('opacity-0');
                comboEl.classList.add('opacity-100');
            } else {
                comboEl.classList.remove('opacity-100');
                comboEl.classList.add('opacity-0');
            }

            let maxScore = LEVEL_THRESHOLDS[level] || LEVEL_THRESHOLDS[4] + 10;
            let minScore = LEVEL_THRESHOLDS[level-1];
            let percent = ((score - minScore) / (maxScore - minScore)) * 100;
            if (percent > 100) percent = 100;
            if (level === 5) percent = 100; 
            
            progressBarEl.style.width = `${percent}%`;
        }

        document.addEventListener('keydown', (e) => {
            const key = e.key;
            if(currentQType === 'text') {
                if (key >= '0' && key <= '9') inputKey(key);
                else if (['-', '/', ',', 'x', 'y'].includes(key)) inputKey(key);
                else if (key === 'Backspace') inputKey('DEL');
                else if (key === 'Enter') checkTextAnswer();
            }
        });

    </script>
</body>
</html>
'''

# 4. 스트림릿 컴포넌트로 렌더링
html_code = html_code.replace("TELEGRAM_TOKEN_PLACEHOLDER", json.dumps(telegram_token))
html_code = html_code.replace("TELEGRAM_CHAT_ID_PLACEHOLDER", json.dumps(telegram_chat_id))
components.html(html_code, height=600)