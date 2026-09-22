import streamlit as st

st.title("자기소개")

with st.form("intro_form"):
    name = st.text_input("이름")
    job = st.text_input("직업")
    hobby = st.text_input("취미")
    submitted = st.form_submit_button("소개 보기")

if submitted:
    if not name or not job or not hobby:
        st.warning("이름, 직업, 취미를 모두 입력해주세요.")
    else:
        st.markdown(
            f"저는 {job}으로 일하는 {name}입니다. 취미는 {hobby}예요."
        )
