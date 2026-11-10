import streamlit as st

st.set_page_config(page_title="Color Picker", page_icon="🎯", layout="wide")


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb).upper()


def shift_color(rgb, offset):
    r, g, b = rgb
    return tuple(max(0, min(255, channel + offset)) for channel in (r, g, b))


def create_theme(base_rgb):
    secondary = shift_color(base_rgb, 45)
    background = tuple(max(230, min(255, channel + 120)) for channel in base_rgb)
    return {
        "Primary": base_rgb,
        "Secondary": secondary,
        "Background": background,
    }


def render_swatches(title, rgb):
    hex_code = rgb_to_hex(rgb)
    st.markdown(
        f"""
        <div style="
            background: {hex_code};
            border-radius: 14px;
            height: 100px;
            border: 1px solid rgba(15,23,42,0.12);
            margin-bottom: 0.7rem;
        "></div>
        """,
        unsafe_allow_html=True,
    )
    st.write(f"**{title}**")
    st.code(f"RGB: {rgb}")
    st.code(f"HEX: {hex_code}")


def classify_color_family(rgb):
    r, g, b = rgb
    max_channel = max(rgb)
    min_channel = min(rgb)
    delta = max_channel - min_channel

    if max_channel <= 20 and min_channel >= 230:
        return "무채색 계열", "회색 계열로 중립적이며 깔끔한 톤을 연상시킵니다."

    if r >= g and r >= b and r > 150 and max_channel - min_channel >= 30:
        if b > 100 and g > 80:
            return "보라 계열", "붉은 기와 파란 기가 섞여 감성적이고 고급스러운 느낌을 줍니다."
        return "빨강 계열", "활기와 열정이 느껴지는 주목성 높은 색상입니다."

    if g >= r and g >= b and g > 150 and max_channel - min_channel >= 30:
        if r > 100 and b > 80:
            return "초록 계열", "자연스럽고 안정감 있는 느낌의 균형 잡힌 색입니다."
        return "초록 계열", "자연과 안정감을 강조하는 편안한 계열입니다."

    if b >= r and b >= g and b > 150 and max_channel - min_channel >= 30:
        if r > 100 and g > 70:
            return "보라 계열", "차분하면서도 프리미엄한 느낌을 주는 색상입니다."
        return "파랑 계열", "신뢰감, 안정감, 차분함을 전달하는 대표적인 색상입니다."

    if r >= 200 and g >= 180 and b <= 120:
        return "노랑 계열", "밝고 친근한 느낌으로 에너지와 희망을 전달합니다."

    if abs(r - g) <= 20 and abs(g - b) <= 20:
        return "무채색 계열", "중립적이고 정돈된 느낌을 주는 색상입니다."

    if r > g and b < g:
        return "노랑 계열", "따뜻하고 밝은 톤으로 친근하고 세련된 분위기를 줍니다."

    if g > b and r < b:
        return "보라 계열", "차분하고 창의적인 분위기를 연상시키는 색입니다."

    return "무채색 계열", "중립적이고 안정적인 무드로 다양한 디자인에 활용하기 좋습니다."


st.title("🎯 RGB Color Picker")
st.caption("슬라이더를 움직이며 원하는 컬러를 선택하고, 테마를 미리 확인해보세요.")

red = st.slider("Red", 0, 255, 120)
green = st.slider("Green", 0, 255, 90)
blue = st.slider("Blue", 0, 255, 200)

base_rgb = (red, green, blue)
hex_code = rgb_to_hex(base_rgb)
theme = create_theme(base_rgb)
family_name, family_desc = classify_color_family(base_rgb)

st.markdown("---")
left, right = st.columns([1.2, 1.8])

with left:
    st.subheader("Selected color")
    st.markdown(
        f"""
        <div style="
            background: {hex_code};
            border-radius: 18px;
            height: 220px;
            border: 1px solid rgba(15,23,42,0.14);
        "></div>
        """,
        unsafe_allow_html=True,
    )
    st.code(f"RGB: {base_rgb}")
    st.code(f"HEX: {hex_code}")
    st.markdown(f"### 🎨 색상 계열: {family_name}")
    st.info(family_desc)

with right:
    st.subheader("Color theme")
    theme_cols = st.columns(3)
    for col, (name, rgb) in zip(theme_cols, theme.items()):
        with col:
            render_swatches(name, rgb)

st.markdown("---")

st.subheader("Suggested usage")
preview_cols = st.columns(3)
for col, label in zip(preview_cols, ["Primary button", "Accent button", "Background card"]):
    with col:
        color = theme["Primary"] if label == "Primary button" else theme["Secondary"] if label == "Accent button" else theme["Background"]
        st.markdown(
            f"""
            <div style="
                background: {rgb_to_hex(color)};
                color: #111827;
                border-radius: 14px;
                padding: 1rem;
                text-align: center;
                font-weight: 700;
                border: 1px solid rgba(15,23,42,0.10);
                margin-bottom: 0.7rem;
            ">{label}</div>
            """,
            unsafe_allow_html=True,
        )
