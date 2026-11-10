import datetime
from zoneinfo import ZoneInfo

import streamlit as st


st.title("간단한 인사 앱")

name = st.text_input("이름을 입력하세요")

if name:
    st.write(f"안녕하세요, {name}님! 만나서 반가워요.")
else:
    st.info("이름을 입력하면 인사말이 표시됩니다.")

if st.button("현재 시간 보기"):
    now = datetime.datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S")
    st.write(f"현재 시간: {now}")
