import streamlit as st

# 1. 페이지 레이아웃 설정 (가장 먼저 실행되어야 할 명령어!)
# layout="wide"로 설정해야 상단 메뉴바가 제대로 표시됩니다.
st.set_page_config(
    page_title="동동쌤의 수학모음",
    page_icon="./images/동동이.PNG",
    layout="wide"
)

# 2. 상단 페이지들 정의
# 각 페이지의 실제 콘텐츠는 별도의 파일에 존재합니다.
pages = {
    "보드게임": [
        # 그룹의 첫 번째 페이지를 default=True로 설정하면 '보드게임' 클릭 시 이 페이지가 먼저 보입니다.
        st.Page("Streams.py", title="스트림스", default=True),
    ],
    "주사위 모음": [
        st.Page("Dice.py", title="주사위 모음")
    ],
    "인공지능 수학": [
        st.Page("ImageExpression.py", title="이미지 자료의 표현")
    ],
}

# 3. 네비게이션 UI 생성
# position="top"으로 설정하여 상단에 메뉴가 나오도록 합니다.
pg = st.navigation(pages, position="top")

# 4. 사용자가 선택한 페이지 실행
# 이 명령어가 '사용자가 선택한 페이지의 파이썬 코드를 이제부터 실행해라!'고
# 지시하는 핵심적인 역할을 합니다.
pg.run()