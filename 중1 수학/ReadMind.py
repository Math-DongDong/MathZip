import streamlit as st
import random

# ---------------------------------------
# 스트림릿 기본 설정
# ---------------------------------------
st.set_page_config(
    page_title="카프리카 상수 동물 마술",
    page_icon="🐾",
    layout="centered"
)

st.title("🐾 카프리카 상수 동물 마술")
st.write("어떤 숫자를 골라도 같은 동물이 나올까요?")

st.divider()

# ---------------------------------------
# 9로 나눈 나머지 → 동물 이모지 매핑
# ---------------------------------------
emoji_map = {
    0: "🐶",  # 강아지
    1: "🐱",  # 고양이
    2: "🐭",  # 생쥐
    3: "🐰",  # 토끼
    4: "🦊",  # 여우
    5: "🐻",  # 곰
    6: "🐼",  # 판다
    7: "🐯",  # 호랑이
    8: "🦁",  # 사자
}

# ---------------------------------------
# 세션 상태 초기화
# ---------------------------------------
if "number" not in st.session_state:
    st.session_state.number = random.randint(1, 99)
    st.session_state.show_answer = False

# ---------------------------------------
# 버튼 UI
# ---------------------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 새로하기"):
        st.session_state.number = random.randint(1, 99)
        st.session_state.show_answer = False

with col2:
    if st.button("✅ 정답은?"):
        st.session_state.show_answer = True

st.divider()

# ---------------------------------------
# 계산 로직
# ---------------------------------------
num = st.session_state.number

# 각 자리수 분리
digits = [int(d) for d in str(num)]

# 자리수의 합
digit_sum = sum(digits)

# 차이 계산
difference = num - digit_sum

# 9로 나눈 나머지
remainder = difference % 9

# ---------------------------------------
# 화면 출력
# ---------------------------------------
st.subheader("📌 결과")

if not st.session_state.show_answer:
    st.write("숫자는 비밀이에요 🤫")
    st.write("하지만 동물은 항상 같아요!")
else:
    st.write(f"✅ 처음 고른 숫자: **{num}**")
    st.write(f"✅ 자리수의 합: **{' + '.join(map(str, digits))} = {digit_sum}**")
    st.write(f"✅ 차이: **{num} − {digit_sum} = {difference}**")
    st.write(f"✅ 9로 나눈 나머지: **{remainder}**")

    st.markdown("---")
    st.markdown(
        f"<h1 style='text-align: center;'>{emoji_map[remainder]}</h1>",
        unsafe_allow_html=True
    )

    st.write("🎉 어떤 숫자를 골라도 이 동물이 나와요!")