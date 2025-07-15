import streamlit as st
import random
import time

pages = {
    "기타": [
        st.Page("Dice.py", title="주사위 모음")
    ],
    "보드게임": [
        st.Page("Streams.py", title="스트림스")
    ],
}

pg = st.navigation(pages, position="top")
pg.run()