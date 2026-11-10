import json
import os
import calendar
from datetime import date

import pandas as pd
import streamlit as st


DIARY_FILE = "diary.csv"
SETTINGS_FILE = "settings.json"
DIARY_COLUMNS = ["날짜", "작성자", "제목", "내용", "날씨", "오늘의 기분", "먹은 음식"]
THEMES = ["파랑", "초록", "보라", "주황", "빨강"]
THEME_COLORS = {
	"파랑": "#2563EB",
	"초록": "#15803D",
	"보라": "#7E22CE",
	"주황": "#C2410C",
	"빨강": "#B91C1C",
}


def load_settings():
	default_settings = {
		"author_name": "",
		"theme": "파랑",
		"last_viewed_date": "",
	}
	if not os.path.exists(SETTINGS_FILE):
		return default_settings

	try:
		with open(SETTINGS_FILE, encoding="utf-8") as settings_file:
			settings = json.load(settings_file)
	except (OSError, json.JSONDecodeError):
		return default_settings

	if not isinstance(settings, dict):
		return default_settings
	return {**default_settings, **settings}


def save_settings(settings):
	with open(SETTINGS_FILE, "w", encoding="utf-8") as settings_file:
		json.dump(settings, settings_file, ensure_ascii=False, indent=2)


def save_selected_theme():
	settings = load_settings()
	settings["theme"] = st.session_state["theme"]
	save_settings(settings)


settings = load_settings()
today = date.today().isoformat()
if "first_visit" not in st.session_state:
	st.session_state["first_visit"] = not bool(settings["last_viewed_date"])
	settings["last_viewed_date"] = today
	save_settings(settings)

author_name = st.sidebar.text_input("작성자 이름", value=settings["author_name"])
if st.sidebar.button("이름 저장", key="save_author"):
	settings["author_name"] = author_name
	save_settings(settings)
	st.sidebar.success("작성자 이름을 저장했어요.")

saved_theme = settings["theme"] if settings["theme"] in THEMES else THEMES[0]
theme = st.sidebar.selectbox(
	"테마 색상",
	THEMES,
	index=THEMES.index(saved_theme),
	key="theme",
	on_change=save_selected_theme,
)

st.markdown(
	f"<div style='background-color: {THEME_COLORS[theme]}; height: 12px; "
	"border-radius: 4px; margin-bottom: 12px;'></div>",
	unsafe_allow_html=True,
)

st.title("📔 나의 일기장")

title = st.text_input("제목")
content = st.text_area("내용", height=150)
today_mood = st.text_input("오늘의 기분")
food = st.text_input("오늘 먹은 음식")
weather = st.selectbox(
	"오늘의 날씨",
	["☀️ 맑음", "☁️ 흐림", "🌧️ 비", "❄️ 눈", "💨 바람"],
)

if st.button("저장"):
	new_diary = pd.DataFrame(
		[
			[
				date.today().isoformat(),
				author_name,
				title,
				content,
				weather,
				today_mood,
				food,
			]
		],
		columns=DIARY_COLUMNS,
	)

	if os.path.exists(DIARY_FILE):
		saved_diaries = pd.read_csv(DIARY_FILE, encoding="utf-8-sig")
		for column in DIARY_COLUMNS:
			if column not in saved_diaries.columns:
				saved_diaries[column] = ""
		saved_diaries = saved_diaries.reindex(columns=DIARY_COLUMNS)
		saved_diaries = pd.concat([saved_diaries, new_diary], ignore_index=True)
	else:
		saved_diaries = new_diary

	saved_diaries.to_csv(DIARY_FILE, index=False, encoding="utf-8-sig")
	st.success("일기가 저장되었습니다!")

if os.path.exists(DIARY_FILE):
	diaries = pd.read_csv(DIARY_FILE, encoding="utf-8-sig")

else:
	diaries = pd.DataFrame(columns=DIARY_COLUMNS)

for column in DIARY_COLUMNS:
	if column not in diaries.columns:
		diaries[column] = ""
diaries = diaries.reindex(columns=DIARY_COLUMNS)
diaries["_row_id"] = diaries.index
displayed_diaries = diaries.sort_values("날짜", ascending=False)

if displayed_diaries.empty:
	st.write("아직 작성된 일기가 없어요.")
else:
	weather_labels = [
		("맑은 날", ["☀️ 맑음", "맑음"]),
		("흐린 날", ["☁️ 흐림", "흐림"]),
		("비 온 날", ["🌧️ 비", "비"]),
		("눈 온 날", ["❄️ 눈", "눈"]),
		("바람 부는 날", ["💨 바람", "바람"]),
	]
	metrics = [("총 일기 수", f"{len(displayed_diaries)}개")]
	metrics.extend(
		(
			label,
			f"{displayed_diaries['날씨'].isin(values).sum()}번",
		)
	for label, values in weather_labels
)

	for start in range(0, len(metrics), 3):
		columns = st.columns(3)
		for column, (label, value) in zip(columns, metrics[start : start + 3]):
			column.metric(label, value)

	st.dataframe(displayed_diaries.drop(columns="_row_id"), hide_index=True)
	delete_options = [int(row_id) for row_id in displayed_diaries["_row_id"]]
	delete_labels = {
		int(row["_row_id"]): (
			f"{row['날짜']} · {str(row['제목']).strip() or '제목 없음'}"
		)
		for _, row in displayed_diaries.iterrows()
	}
	delete_column, button_column = st.columns([5, 1])
	with delete_column:
		selected_diary = st.selectbox(
			"삭제할 일기",
			options=delete_options,
			format_func=lambda row_id: delete_labels[row_id],
			key="delete_diary_target",
		)
	with button_column:
		if st.button(
			"삭제",
			icon=":material/delete:",
			help="선택한 일기 삭제",
			key="delete_diary_button",
		):
			diaries = diaries.drop(index=selected_diary).reset_index(drop=True)
			diaries = diaries.drop(columns="_row_id")
			diaries.to_csv(DIARY_FILE, index=False, encoding="utf-8-sig")
			st.session_state.pop("delete_diary_target", None)
			st.rerun()

st.subheader("일기 달력")
calendar_date = st.date_input("달력 날짜", value=date.today(), key="calendar_date")
st.markdown(f"**{calendar_date.year}년 {calendar_date.month}월**")
weekday_columns = st.columns(7)
for column, weekday in zip(weekday_columns, ["월", "화", "수", "목", "금", "토", "일"]):
	column.caption(weekday)

daily_counts = diaries["날짜"].value_counts().to_dict()
for week in calendar.monthcalendar(calendar_date.year, calendar_date.month):
	day_columns = st.columns(7)
	for column, day in zip(day_columns, week):
		if day:
			day_key = date(calendar_date.year, calendar_date.month, day).isoformat()
			column.markdown(f"**{day}**")
			column.caption(f"{daily_counts.get(day_key, 0)}건")
		else:
			column.write(" ")

if st.session_state["first_visit"]:
	st.write("처음 방문이에요! 일기를 써봐요 🌱")
else:
	st.write(f"마지막으로 일기를 확인한 날: {settings['last_viewed_date']}")
