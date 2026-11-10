import os

import pandas as pd
import streamlit as st


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
INPUT_PATH = os.path.join(DATA_DIR, "pension_raw.csv")
OUTPUT_PATH = os.path.join(DATA_DIR, "cleaned_pension.csv")

SOURCE_STATUS = "사업장가입상태코드 1 등록 2 탈퇴"
SOURCE_TYPE = "사업장형태구분코드 1 법인 2 개인"


@st.cache_data
def load_data(file_path: str) -> pd.DataFrame:
    try:
        data = pd.read_csv(file_path, encoding="cp949")
    except UnicodeDecodeError:
        data = pd.read_csv(file_path, encoding="utf-8-sig")

    data.columns = data.columns.str.strip()
    return data


def show_stage(title: str, message: str, data: pd.DataFrame) -> None:
    with st.expander(title):
        st.success(message)
        st.dataframe(data.head(10), width="stretch")


st.set_page_config(page_title="국민연금 사업장 데이터 전처리", layout="wide")
st.title("📋 국민연금 사업장 데이터 전처리")
metrics_placeholder = st.empty()

try:
    raw_df = load_data(INPUT_PATH)
except Exception as error:
    st.error(f"CSV 파일을 읽지 못했습니다: {error}")
    st.stop()

show_stage("1단계. CSV 읽기", f"원본 데이터를 읽었습니다. 전체 {len(raw_df):,}행입니다.", raw_df)

required_columns = [
    "자료생성년월",
    "사업장명",
    SOURCE_STATUS,
    "사업장도로명상세주소",
    "법정동주소광역시도코드",
    "사업장업종코드명",
    "가입자수",
    "당월고지금액",
    SOURCE_TYPE,
    "신규취득자수",
    "상실가입자수",
]
missing_columns = [column for column in required_columns if column not in raw_df.columns]
if missing_columns:
    st.error(f"원본 CSV에 필요한 컬럼이 없습니다: {', '.join(missing_columns)}")
    st.stop()

working_df = raw_df.loc[:, required_columns].copy()
show_stage("2단계. 필요한 컬럼 선택", "전처리에 필요한 컬럼만 선택했습니다.", working_df)

working_df = working_df.rename(
    columns={
        "사업장명": "company_name",
        SOURCE_STATUS: "status_code",
        "사업장도로명상세주소": "address",
        "법정동주소광역시도코드": "sido_code",
        "사업장업종코드명": "industry",
        "가입자수": "member_count",
        "당월고지금액": "charge_amount",
        SOURCE_TYPE: "type_code",
        "신규취득자수": "new_members",
        "상실가입자수": "lost_members",
    }
)
show_stage("3단계. 컬럼명 영문으로 변경", "컬럼명을 영문으로 변경했습니다.", working_df)

working_df["status"] = pd.to_numeric(working_df["status_code"], errors="coerce").map(
    {1: "등록", 2: "탈퇴"}
)
working_df["company_type"] = pd.to_numeric(working_df["type_code"], errors="coerce").map(
    {1: "법인", 2: "개인"}
)
working_df = working_df.drop(columns=["status_code", "type_code"])
show_stage("4단계. 코드값을 텍스트로 변환", "가입 상태와 사업장 형태 코드를 텍스트로 변환했습니다.", working_df)

working_df["sido"] = working_df["address"].fillna("").astype(str).str.split().str[0]
working_df = working_df.drop(columns=["address", "sido_code"])
show_stage("5단계. 시도명 추출", "도로명 주소에서 시도명을 추출하고 주소 및 시도 코드를 제거했습니다.", working_df)

numeric_columns = ["member_count", "charge_amount", "new_members", "lost_members"]
for column in numeric_columns:
    working_df[column] = pd.to_numeric(working_df[column], errors="coerce").fillna(0)
show_stage("6단계. 숫자 컬럼 타입 변환", "숫자 컬럼을 변환하고 변환 실패 값은 0으로 처리했습니다.", working_df)

working_df["estimated_salary_total"] = working_df["charge_amount"] / 0.095
working_df["estimated_salary_per"] = working_df["estimated_salary_total"].div(
    working_df["member_count"].where(working_df["member_count"] != 0, 1)
)
working_df.loc[working_df["member_count"] == 0, "estimated_salary_per"] = 0
working_df["net_change"] = working_df["new_members"] - working_df["lost_members"]
show_stage("7단계. 파생 컬럼 생성", "추정 급여와 가입자 순증감 컬럼을 계산했습니다.", working_df)

cleaned_df = working_df.loc[
    (working_df["status"] == "등록")
    & (working_df["member_count"] != 0)
    & (working_df["charge_amount"] != 0)
].copy()
show_stage("8단계. 이상값 처리", "등록 상태이며 가입자 수와 고지 금액이 0이 아닌 행만 유지했습니다.", cleaned_df)

try:
    os.makedirs(DATA_DIR, exist_ok=True)
    cleaned_df.to_csv(OUTPUT_PATH, encoding="utf-8", index=False)
except OSError as error:
    st.error(f"전처리 결과를 저장하지 못했습니다: {error}")
    st.stop()

show_stage("9단계. 전처리 결과 저장", "전처리된 데이터를 data/cleaned_pension.csv에 저장했습니다.", cleaned_df)
st.success(f"저장 완료: {OUTPUT_PATH}")

with metrics_placeholder.container():
    before_metric, after_metric = st.columns(2)
    before_metric.metric("전처리 전 행 수", f"{len(raw_df):,}")
    after_metric.metric("전처리 후 행 수", f"{len(cleaned_df):,}")

total_members = cleaned_df["member_count"].sum()
average_salary_per_member = cleaned_df["estimated_salary_per"].mean()
stat_one, stat_two, stat_three, stat_four = st.columns(4)
stat_one.metric("총 사업장 수", f"{len(cleaned_df):,}")
stat_two.metric("시도 수", f"{cleaned_df['sido'].nunique():,}")
stat_three.metric("총 가입자 수", f"{total_members:,.0f}")
stat_four.metric("1인당 추정 평균 월급여", f"{average_salary_per_member:,.0f}원" if pd.notna(average_salary_per_member) else "0원")