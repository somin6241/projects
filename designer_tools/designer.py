import streamlit as st

st.set_page_config(page_title="Designer Tools", page_icon="🎨", layout="wide")

st.title("🎨 Designer Tools")
st.subheader("디자이너를 위한 색상과 이미지 작업 도구")
st.caption("RGB 색상 선택, 이미지 기반 팔레트 생성, 필터 적용까지 한 번에 진행해보세요.")

features = [
    {
        "title": "Color Picker",
        "icon": "🎯",
        "description": "RGB 슬라이더로 색상을 선택하고, 기본색·보조색·배경색 테마를 자동으로 생성합니다.",
        "page": "pages/01_color_picker.py",
    },
    {
        "title": "Image Color",
        "icon": "🖼️",
        "description": "이미지에서 주요 색상 5개를 추출해 브랜드에 맞는 컬러 테마를 뽑아냅니다.",
        "page": "pages/02_image_color.py",
    },
    {
        "title": "Image Filter",
        "icon": "✨",
        "description": "이미지에 흑백, 세피아, 블러 등 다양한 필터를 적용하고 결과를 다운로드합니다.",
        "page": "pages/03_image_filter.py",
    },
]

cols = st.columns(3)
for col, feature in zip(cols, features):
    with col:
        st.markdown(
            f"""
            <div style="
                padding: 1.4rem;
                border: 1px solid #e3e8ef;
                border-radius: 18px;
                background: linear-gradient(135deg, rgba(122,92,255,0.10), rgba(78,201,255,0.08));
                min-height: 260px;
                margin-bottom: 1rem;
            ">
                <div style="font-size: 2.2rem; margin-bottom: 0.6rem;">{feature['icon']}</div>
                <h3 style="margin-top: 0; margin-bottom: 0.6rem;">{feature['title']}</h3>
                <p style="color: #4b5563; line-height: 1.6; min-height: 90px;">{feature['description']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(f"{feature['title']} 열기", key=f"open_{feature['title']}", use_container_width=True):
            st.switch_page(feature["page"])

st.markdown("---")
st.subheader("사용 가이드")

with st.container(border=True):
    st.write("1. Color Picker: RGB 값을 조절해 원하는 색상을 선택합니다.")
    st.write("2. Image Color: 이미지를 업로드하면 대표 컬러를 추출해 테마를 만듭니다.")
    st.write("3. Image Filter: 필터를 적용해 결과 이미지를 저장하고 바로 활용합니다.")
