import streamlit
# app.py
# Streamlit 기초 실습용 예제 사이트 (초급자 대상)
# - 텍스트 출력 / 데이터 출력 / 시각화 / 미디어 / 코드 출력 / 위젯 / 레이아웃(with)
# 실행: streamlit run app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="Streamlit 기초 실습 사이트",
    page_icon="🧪",
    layout="wide",
)

# -----------------------------
# 유틸: 샘플 데이터 생성
# -----------------------------
def make_sample_df(n: int = 200, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "age": rng.integers(18, 60, size=n),
        "score": np.clip(rng.normal(70, 12, size=n), 0, 100).round(1),
        "group": rng.choice(["A", "B", "C"], size=n, p=[0.4, 0.35, 0.25]),
    })
    return df

# -----------------------------
# 사이드바: 네비게이션
# -----------------------------
with st.sidebar:
    st.title("🧭 메뉴")
    page = st.radio(
        "실습 주제 선택",
        [
            "🏠 홈",
            "📝 텍스트 & 마크다운",
            "📊 데이터 출력 & EDA",
            "🖼️ 미디어(이미지)",
            "🧩 위젯 놀이터",
            "💻 코드 출력",
        ],
        index=0,
    )
    st.divider()
    st.caption("Tip) 위젯을 만져보면서 화면이 어떻게 바뀌는지 확인해보세요!")

# -----------------------------
# 페이지 1: 홈
# -----------------------------
if page == "🏠 홈":
    st.title("🧪 Streamlit 기초 실습 사이트")
    st.write(
        """
이 사이트는 **Streamlit 처음 배우는 학생**이 실습하기 좋은 예제 모음입니다.

- `st.title / st.header / st.subheader / st.write / st.markdown`
- `st.dataframe / st.table / st.json / st.metric`
- `st.image`
- `st.code / st.echo`
- `st.button / st.text_input / st.selectbox / st.slider ...`
- `with st.container() / with st.sidebar / columns / expander`

왼쪽 메뉴에서 이동해보세요.
"""
    )

    st.subheader("오늘의 실습 미션 ✅")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("1) 텍스트/마크다운으로 강조 표현해보기")
    with col2:
        st.info("2) 데이터프레임을 필터링해서 통계/그래프 보기")
    with col3:
        st.info("3) 위젯 값에 따라 화면이 바뀌게 만들기")

# -----------------------------
# 페이지 2: 텍스트 & 마크다운
# -----------------------------
elif page == "📝 텍스트 & 마크다운":
    st.title("📝 텍스트 출력 & 마크다운")
    st.caption("01_basic.ipynb의 01_text 예제를 확장한 페이지")

    st.header("1) 기본 텍스트 출력")
    st.subheader("st.title / st.header / st.subheader / st.write")
    st.write("st.write는 문자열뿐 아니라 숫자, 리스트, 데이터프레임 등 다양한 객체를 출력할 수 있어요.")

    st.header("2) 마크다운 출력")
    st.markdown("**굵게(bold)** / *기울임(italic)* / `코드(code)`")
    st.markdown("- 리스트 1\n- 리스트 2\n- 리스트 3")
    st.markdown("> 인용문도 가능해요")
    st.markdown("~~취소선(strikethrough)~~ 도 됩니다.")

    st.header("3) 간단 퀴즈(위젯 연동)")
    answer = st.text_input("Q) Streamlit에서 가장 많이 쓰는 출력 함수는?")
    if answer:
        st.success(f"입력값: {answer}")
        st.info("예: st.write(), st.markdown(), st.dataframe() 등")

# -----------------------------
# 페이지 3: 데이터 출력 & EDA
# -----------------------------
elif page == "📊 데이터 출력 & EDA":
    st.title("📊 데이터 출력 & 간단 EDA")
    st.caption("01_basic.ipynb의 02_data + 시각화를 묶어서 실습")

    # 데이터 준비: 업로드 or 샘플
    with st.expander("데이터 준비(업로드/샘플 선택)", expanded=True):
        use_sample = st.checkbox("샘플 데이터 사용", value=True)
        uploaded = st.file_uploader("CSV 업로드(선택)", type=["csv"])

        if use_sample:
            df = make_sample_df()
            st.info("샘플 데이터로 진행합니다. (age, score, group)")
        elif uploaded is not None:
            df = pd.read_csv(uploaded)
            st.info("업로드한 CSV로 진행합니다.")
        else:
            st.warning("샘플 데이터 체크 또는 CSV 업로드를 해주세요.")
            st.stop()

    st.subheader("1) 데이터 미리보기")
    st.dataframe(df.head(20), use_container_width=True)

    st.subheader("2) 요약 통계")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("행 개수", f"{len(df):,}")
    with c2:
        st.metric("열 개수", f"{df.shape[1]:,}")
    with c3:
        # score 컬럼이 없을 수도 있어 방어
        if "score" in df.columns and pd.api.types.is_numeric_dtype(df["score"]):
            st.metric("score 평균", f"{df['score'].mean():.2f}")
        else:
            st.metric("score 평균", "N/A")
    with c4:
        st.metric("결측치 수", f"{int(df.isna().sum().sum()):,}")

    st.subheader("3) 필터링 실습")
    # group이 있으면 그룹 필터 제공
    if "group" in df.columns:
        groups = ["전체"] + sorted(df["group"].dropna().astype(str).unique().tolist())
        selected_group = st.selectbox("group 선택", groups)
        if selected_group != "전체":
            df_view = df[df["group"].astype(str) == selected_group].copy()
        else:
            df_view = df.copy()
    else:
        df_view = df.copy()

    # 수치형 컬럼 선택
    numeric_cols = [c for c in df_view.columns if pd.api.types.is_numeric_dtype(df_view[c])]
    if not numeric_cols:
        st.warning("수치형 컬럼이 없어 그래프 실습을 진행할 수 없습니다.")
        st.stop()

    target_col = st.selectbox("그래프를 그릴 수치형 컬럼 선택", numeric_cols)

    st.write("필터 적용된 데이터 미리보기:")
    st.dataframe(df_view.head(10), use_container_width=True)

    st.subheader("4) 히스토그램(기초 시각화)")
    bins = st.slider("bins(막대 개수)", min_value=5, max_value=50, value=15, step=1)

    fig, ax = plt.subplots()
    ax.hist(df_view[target_col].dropna(), bins=bins)
    ax.set_xlabel(target_col)
    ax.set_ylabel("count")
    ax.set_title(f"Histogram of {target_col}")
    st.pyplot(fig)

    st.subheader("5) JSON / table 출력도 가능")
    st.json({"selected_group": selected_group if "group" in df.columns else None, "target_col": target_col, "bins": bins})
    st.table(df_view.describe(include="all").head())

# -----------------------------
# 페이지 4: 미디어(이미지)
# -----------------------------
elif page == "🖼️ 미디어(이미지)":
    st.title("🖼️ 이미지 출력 실습")
    st.caption("01_basic.ipynb의 03_image 예제를 안전하게(파일/URL) 실습")

    st.write("이미지는 **로컬 파일 경로** 또는 **URL**로 표시할 수 있어요.")

    tab1, tab2 = st.tabs(["로컬 이미지", "URL 이미지"])
    with tab1:
        st.subheader("1) 로컬 이미지")
        st.write("프로젝트 폴더에 이미지가 있으면 경로로 불러올 수 있어요.")
        local_path = st.text_input("로컬 이미지 경로 입력(예: data/hamster.jpg)", value="data/hamster.jpg")

        try:
            st.image(local_path, caption="로컬 이미지 미리보기", width=450)
            st.success("로컬 이미지 로드 성공!")
        except Exception as e:
            st.warning("해당 경로에 이미지가 없거나 읽을 수 없습니다. 아래 URL 탭을 사용해보세요.")
            st.code(str(e))

    with tab2:
        st.subheader("2) URL 이미지")
        img_url = st.text_input(
            "이미지 URL 입력",
            value="https://images.unsplash.com/photo-1543852786-1cf6624b9987?auto=format&fit=crop&w=900&q=60",
        )
        st.image(img_url, caption="URL 이미지 미리보기", width=450)

# -----------------------------
# 페이지 5: 위젯 놀이터
# -----------------------------
elif page == "🧩 위젯 놀이터":
    st.title("🧩 위젯 놀이터")
    st.caption("01_basic.ipynb의 05_widget 예제를 한 화면에서 실습")

    with st.container():
        st.subheader("1) 입력 위젯")
        name = st.text_input("이름 입력", value="Daisy")
        age = st.slider("나이 선택", 1, 100, 25)
        mood = st.selectbox("오늘 기분", ["😀 좋음", "🙂 보통", "😅 피곤", "😴 졸림"])

        st.write(f"안녕하세요, **{name}** 님! 나이는 **{age}** 세, 기분은 **{mood}** 이군요.")

    st.divider()

    with st.container():
        st.subheader("2) 버튼(동작) 실습")
        # 버튼은 누르는 순간 True를 반환(해당 실행 시점)
        if st.button("랜덤 점수 생성"):
            score = np.random.randint(0, 101)
            st.success(f"생성된 점수: {score}")

        st.caption("버튼은 클릭 이벤트를 트리거하는 용도로 자주 씁니다.")

    st.divider()

    with st.container():
        st.subheader("3) 체크박스 / 멀티셀렉트")
        show_df = st.checkbox("샘플 데이터 보기", value=False)
        cols = st.multiselect("보고 싶은 컬럼 선택", ["age", "score", "group"], default=["age", "score"])

        if show_df:
            df = make_sample_df()
            st.dataframe(df[cols], use_container_width=True)

# -----------------------------
# 페이지 6: 코드 출력
# -----------------------------
elif page == "💻 코드 출력":
    st.title("💻 코드 출력 실습")
    st.caption("01_basic.ipynb의 04_code 예제를 기반으로 실습")

    st.subheader("1) st.code() - 코드만 보여주기")
    example_code = """
import streamlit as st

st.title("Hello Streamlit")
st.write("This is code display example")
"""
    st.code(example_code, language="python")

    st.subheader("2) st.echo() - 작성한 코드를 그대로 보여주고 실행도")
    with st.echo():
        x = 10
        y = 20
        st.write("x + y =", x + y)

    st.subheader("3) 미션")
    st.info("미션: 아래에 본인이 만든 함수를 st.echo() 안에서 실행해보세요!")
    user_fn = st.text_area("함수 코드를 작성해보기(연습용)", value="def hello(name):\n    return f'Hello, {name}!'\n\nhello('Streamlit')")
    st.code(user_fn, language="python")
