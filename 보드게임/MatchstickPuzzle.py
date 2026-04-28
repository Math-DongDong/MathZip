import streamlit as st
import streamlit.components.v1 as components
import random
from pathlib import Path

# -----------------------------------------------------------------------------
# 1. 페이지 기본 설정 및 헤더
# -----------------------------------------------------------------------------
st.markdown("<h1 style='text-align: center; color: #d97706;'>🧩 성냥개비 퍼즐</h1>", unsafe_allow_html=True)

# 경로 설정
BASE_DIR = Path(__file__).resolve().parents[1]
IMAGE_DIR = BASE_DIR / "기타" / "성냥개비퍼즐(54문제)"

# -----------------------------------------------------------------------------
# 2. 그림판 HTML/CSS/JS (세로 길이 560px 고정)
# -----------------------------------------------------------------------------
DRAWING_HTML = '''
<style>
    /* 스크롤바가 생기지 않도록 overflow: hidden 적용 */
    body { font-family: 'Segoe UI', sans-serif; margin: 0; background: transparent; overflow: hidden; }
    .canvas-wrapper { 
        display: flex; flex-direction: column; align-items: center; justify-content: center; 
        padding: 10px; width: 100%; box-sizing: border-box; 
    }
    
    /* ⬅️[세로 길이 고정] aspect-ratio를 지우고 height를 560px로 고정했습니다! */
    #drawCanvas { 
        width: 100%; 
        height: 560px; /* 세로 길이 고정 */
        border: 2px solid #cbd5e1; 
        border-radius: 16px; 
        touch-action: none; 
        background: #ffffff; 
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1); 
    }
    
    /* 제목과 버튼을 양끝으로 배치하는 컨테이너 */
    .canvas-header { 
        display: flex; justify-content: space-between; align-items: center; 
        width: 100%; margin-bottom: 10px; 
    }
    
    .clear-btn { 
        background: #ef4444; color: white; border: none; border-radius: 8px; 
        padding: 8px 20px; font-size: 1rem; font-weight: bold; cursor: pointer; 
        transition: background 0.2s, transform 0.1s; box-shadow: 0 2px 4px rgba(0,0,0,0.1); 
    }
    .clear-btn:hover { background: #dc2626; transform: translateY(-1px); }
    .clear-btn:active { transform: translateY(1px); }
    
    /* margin-bottom 제거 (header에서 관리) */
    .canvas-title { font-size: 1.2rem; font-weight: bold; color: #334155; margin: 0; display: flex; align-items: center; gap: 8px; }
</style>

<div class="canvas-wrapper">
    <!-- 버튼을 캔버스 아래에서 위로 끌어올려 나란히 배치했습니다 -->
    <div class="canvas-header">
        <div class="canvas-title">✍️ 나만의 풀이장</div>
        <button class="clear-btn" onclick="clearCanvas()">🗑️ 모두 지우기</button>
    </div>
    <canvas id="drawCanvas" width="1600" height="1200"></canvas> <!-- 내부 해상도 -->
</div>

<script>
    const canvas = document.getElementById('drawCanvas');
    const ctx = canvas.getContext('2d');
    let drawing = false;
    let lastX = 0;
    let lastY = 0;

    ctx.lineWidth = 10;
    ctx.lineCap = 'round';
    ctx.strokeStyle = '#111';

    // 캔버스의 화면상 크기와 실제 내부 픽셀간의 비율을 계산하여 마우스/터치 위치 보정
    function setPosition(e) {
        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        
        let clientX = e.clientX;
        let clientY = e.clientY;

        if (e.touches && e.touches.length > 0) {
            clientX = e.touches[0].clientX;
            clientY = e.touches[0].clientY;
        }

        return { 
            x: (clientX - rect.left) * scaleX, 
            y: (clientY - rect.top) * scaleY 
        };
    }

    function startDraw(e) {
        drawing = true;
        const pos = setPosition(e);
        lastX = pos.x; lastY = pos.y;
    }

    function draw(e) {
        if (!drawing) return;
        e.preventDefault();
        const pos = setPosition(e);
        ctx.beginPath();
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(pos.x, pos.y);
        ctx.stroke();
        lastX = pos.x; lastY = pos.y;
    }

    function stopDraw() { drawing = false; }
    function clearCanvas() { ctx.clearRect(0, 0, canvas.width, canvas.height); }

    canvas.addEventListener('mousedown', startDraw);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDraw);
    canvas.addEventListener('mouseout', stopDraw);
    canvas.addEventListener('touchstart', startDraw, {passive: false});
    canvas.addEventListener('touchmove', draw, {passive: false});
    canvas.addEventListener('touchend', stopDraw);
    canvas.addEventListener('touchcancel', stopDraw);
</script>
'''

# -----------------------------------------------------------------------------
# 3. 로직 함수 정의
# -----------------------------------------------------------------------------
def load_problem_files():
    if not IMAGE_DIR.exists():
        return []
    problems =[
        path for path in sorted(IMAGE_DIR.iterdir(), key=lambda p: (p.suffix.lower(), p.name))
        if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
    ]
    problems =[str(path) for path in problems]
    random.shuffle(problems)
    return problems

def initialize_problems():
    problems = load_problem_files()
    st.session_state.problem_pool = problems
    st.session_state.solved_count = 0
    st.session_state.unknown_count = 0
    st.session_state.total_count = len(problems)
    st.session_state.current_problem = st.session_state.problem_pool.pop(0) if st.session_state.problem_pool else None

if "problem_pool" not in st.session_state or "current_problem" not in st.session_state:
    initialize_problems()

# -----------------------------------------------------------------------------
# 4. 화면 레이아웃 구성
# -----------------------------------------------------------------------------

if not st.session_state.current_problem:
    st.balloons()
    st.success("🎉 모든 문제를 완료했습니다! 정말 수고하셨습니다.")
    st.info("성냥개비 퍼즐 폴더에 이미지 파일이 있는지 확인해 주세요.")
    if st.button("🔄 처음부터 다시하기", type="primary", key="restart_empty"):
        initialize_problems()
        st.rerun()
    st.stop()

# ==========================================
# [상단 영역] 대시보드
# ==========================================
remaining = len(st.session_state.problem_pool)
st.markdown(f"""
<div style='background-color: #f8fafc; padding: 15px; border-radius: 10px; border: 1px solid #e2e8f0; display: flex; justify-content: space-around; text-align: center;'>
    <div><span style='font-size: 0.9rem; color: #64748b;'>총 문제</span><br><span style='font-size: 1.2rem; font-weight: bold; color: #0f172a;'>{st.session_state.total_count}</span></div>
    <div><span style='font-size: 0.9rem; color: #64748b;'>해결한 문제</span><br><span style='font-size: 1.2rem; font-weight: bold; color: #16a34a;'>{st.session_state.solved_count}</span></div>
    <div><span style='font-size: 0.9rem; color: #64748b;'>다시 볼 문제</span><br><span style='font-size: 1.2rem; font-weight: bold; color: #ea580c;'>{st.session_state.unknown_count}</span></div>
    <div><span style='font-size: 0.9rem; color: #64748b;'>남은 문제</span><br><span style='font-size: 1.2rem; font-weight: bold; color: #2563eb;'>{remaining + 1}</span></div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# [중단 영역] 조작 버튼 
# ==========================================
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 처음부터 다시", type="secondary", use_container_width=True, key="restart_matchstick"):
        initialize_problems()
        st.rerun()


with col2:
    if st.button("❓ 잘 모르겠어요 (나중에 풀기)", type="secondary", use_container_width=True, key="unknown_matchstick"):
        st.session_state.unknown_count += 1
        st.session_state.problem_pool.append(st.session_state.current_problem)
        random.shuffle(st.session_state.problem_pool)
        if st.session_state.problem_pool:
            st.session_state.current_problem = st.session_state.problem_pool.pop(0)
        else:
            st.session_state.current_problem = None
        st.rerun()

with col3:
    if st.button("✅ 해결했습니다!", type="primary", use_container_width=True, key="solve_matchstick"):
        st.session_state.solved_count += 1
        if st.session_state.problem_pool:
            st.session_state.current_problem = st.session_state.problem_pool.pop(0)
        else:
            st.session_state.current_problem = None
        st.rerun()

st.divider() 

# ==========================================
#[하단 영역] 메인 문제 & 그림판 (1 : 2.5 비율)
# ==========================================
left_col, right_col = st.columns([1, 2.5])

with left_col:
    st.subheader("💡 오늘의 문제")
    st.image(st.session_state.current_problem, width='stretch')
    st.info("📌 **Hint:** 풀이장에 먼저 스케치해 보세요!")

with right_col:
    # 캔버스 560px + 상단 제목 + 하단 버튼이 넉넉히 보이도록 전체 높이를 700으로 설정했습니다.
    components.html(DRAWING_HTML, height=650, scrolling=True)
