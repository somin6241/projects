from collections import Counter

import streamlit as st
from PIL import Image

st.set_page_config(page_title="Image Color", page_icon="🖼️", layout="wide")


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb).upper()


def shift_color(rgb, offset):
    r, g, b = rgb
    return tuple(max(0, min(255, channel + offset)) for channel in (r, g, b))


def create_theme(base_rgb):
    secondary = shift_color(base_rgb, 45)
    background = tuple(max(235, min(255, channel + 120)) for channel in base_rgb)
    return {
        "Primary": base_rgb,
        "Secondary": secondary,
        "Background": background,
    }


def quantize_color(rgb, step=32):
    return tuple(channel // step * step for channel in rgb)


def extract_prominent_colors(image, max_colors=5):
    resized = image.resize((180, 180))
    pixels = list(resized.getdata())
    counter = Counter()
    for pixel in pixels:
        quantized = quantize_color(pixel, step=32)
        counter[quantized] += 1
    return [color for color, _ in counter.most_common(max_colors)]


st.title("🖼️ Image Color Extractor")
st.caption("이미지를 업로드하면 주요 색상을 추출해 컬러 테마를 생성합니다.")

uploaded_file = st.file_uploader("이미지 업로드", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="업로드된 이미지", use_container_width=True)

    colors = extract_prominent_colors(image, max_colors=5)
    theme = create_theme(colors[0])

    st.markdown("---")
    st.subheader("주요 색상 5개")
    palette_cols = st.columns(len(colors))
    for col, color in zip(palette_cols, colors):
        with col:
            st.markdown(
                f"""
                <div style="
                    background: {rgb_to_hex(color)};
                    border-radius: 14px;
                    height: 120px;
                    border: 1px solid rgba(15,23,42,0.12);
                    margin-bottom: 0.7rem;
                "></div>
                """,
                unsafe_allow_html=True,
            )
            st.write(f"RGB: {color}")
            st.write(f"HEX: {rgb_to_hex(color)}")

    st.markdown("---")
    st.subheader("Extracted color theme")
    theme_cols = st.columns(3)
    for col, (name, rgb) in zip(theme_cols, theme.items()):
        with col:
            st.markdown(
                f"""
                <div style="
                    background: {rgb_to_hex(rgb)};
                    border-radius: 14px;
                    height: 110px;
                    border: 1px solid rgba(15,23,42,0.12);
                    margin-bottom: 0.7rem;
                "></div>
                """,
                unsafe_allow_html=True,
            )
            st.write(f"**{name}**")
            st.code(f"RGB: {rgb}")
            st.code(f"HEX: {rgb_to_hex(rgb)}")
else:
    st.info("이미지를 업로드하면 주요 색상을 추출해 테마를 구성합니다.")
