import io

import streamlit as st
from PIL import Image, ImageFilter, ImageOps

st.set_page_config(page_title="Image Filter", page_icon="✨", layout="wide")


def apply_sepia(image):
    img = image.convert("RGB")
    pixels = img.load()
    width, height = img.size
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            tr = min(255, int(r * 0.393 + g * 0.769 + b * 0.189))
            tg = min(255, int(r * 0.349 + g * 0.686 + b * 0.168))
            tb = min(255, int(r * 0.272 + g * 0.534 + b * 0.131))
            pixels[x, y] = (tr, tg, tb)
    return img


def apply_filter(image, filter_name, intensity):
    if filter_name == "Original":
        return image.copy()
    if filter_name == "Black & White":
        return ImageOps.grayscale(image)
    if filter_name == "Sepia":
        return apply_sepia(image)
    if filter_name == "Blur":
        return image.filter(ImageFilter.GaussianBlur(radius=intensity))
    if filter_name == "Sharpen":
        return image.filter(ImageFilter.SHARPEN).filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
    if filter_name == "Contrast":
        return image.filter(ImageFilter.DETAIL).filter(ImageFilter.UnsharpMask(radius=1, percent=intensity * 30, threshold=3))
    return image.copy()


st.title("✨ Image Filter Studio")
st.caption("이미지에 필터를 적용하고 결과를 바로 다운로드해보세요.")

uploaded_file = st.file_uploader("이미지 업로드", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file is not None:
    original = Image.open(uploaded_file).convert("RGB")
    filter_options = ["Original", "Black & White", "Sepia", "Blur", "Sharpen", "Contrast"]
    filter_name = st.selectbox("필터 선택", filter_options)
    intensity = st.slider("필터 강도", min_value=1, max_value=10, value=3)

    processed = apply_filter(original, filter_name, intensity)

    left, right = st.columns(2)
    with left:
        st.subheader("Original")
        st.image(original, use_container_width=True)
    with right:
        st.subheader("Result")
        st.image(processed, use_container_width=True)

    output = io.BytesIO()
    processed.save(output, format="PNG")
    output.seek(0)

    st.download_button(
        label="결과 이미지 다운로드",
        data=output.getvalue(),
        file_name=f"filtered_{filter_name.lower().replace(' ', '_')}.png",
        mime="image/png",
    )
else:
    st.info("이미지를 업로드하면 필터를 적용할 수 있습니다.")
