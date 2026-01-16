# app.py
# Streamlit 기초 실습 예제 사이트 (01_basic.ipynb에서 쓴 기능만 사용)

import time
import numpy as np
import pandas as pd
import streamlit as st

# -------------------------
# 샘플 데이터 만들기
# -------------------------
def make_df(n=30, seed=0):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "name": [f"user_{i+1}" for i in range(n)],
        "age": rng.integers(18, 60, size=n),
        "score": np.clip(rng.normal(70, 12, size=n), 0, 100).round(1),
        "group": rng.choice(["A", "B", "C"], size=n, p=[0.4, 0.35, 0.25])
    })
    return df

# -------------------------
# 메인 제목
# -------------------------
st.title("🧪 Streamlit 기초 실습 사이트")
st.caption("※ 이 사이트는 01_basic.ipynb에서 사용한 Streamlit 기능만으로 구성됨")

# -------------------------
# 페이지 이동(네비게이션) - sidebar/columns/container 미사용
# -------------------------
page = st.radio(
    "실습 페이지 선택",
    [
        "1) 텍스트 출력",
        "2) 위젯 실습",
        "3) 데이터 출력 & 간단 EDA",
        "4) 미디어(이미지/오디오/비디오/카메라)",
        "5) 코드/수식/진행상태"
    ]
)

# =========================================================
# 1) 텍스트 출력
# =========================================================
if page == "1) 텍스트 출력":
    st.header("1) 텍스트 출력")
    st.subheader("기본 출력 함수")
    st.text("st.text는 '텍스트만' 간단히 출력")
    st.write("st.write는 문자열/숫자/리스트/데이터프레임 등 다양한 객체 출력 가능")
    st.markdown("**마크다운**도 가능: `코드` / *기울임* / ~~취소선~~")
    st.latex(r"\text{mean} = \frac{1}{n}\sum_{i=1}^{n}x_i")

    st.subheader("상태 메시지 예시")
    st.info("info: 안내 메시지")
    st.success("success: 성공 메시지")
    st.warning("warning: 경고 메시지")
    st.error("error: 에러 메시지")

# =========================================================
# 2) 위젯 실습
# =========================================================
elif page == "2) 위젯 실습":
    st.header("2) 위젯 실습")
    st.subheader("입력 위젯")

    name = st.text_input("이름 입력", value="Daisy")
    age = st.number_input("나이 입력", min_value=0, max_value=120, value=25, step=1)
    level = st.slider("만족도(0~10)", 0, 10, 7)
    color = st.color_picker("좋아하는 색 선택", value="#00A6FF")

    st.write(f"입력 결과 → 이름: {name}, 나이: {age}, 만족도: {level}, 색상: {color}")

    st.subheader("선택 위젯")
    fruit = st.selectbox("좋아하는 과일 하나 선택", ["사과", "바나나", "수박", "딸기"])
    hobbies = st.multiselect("취미 여러 개 선택", ["독서", "운동", "게임", "음악", "여행"], default=["독서"])
    page_mode = st.radio("학습 모드 선택", ["기본", "응용", "퀴즈"])

    st.write("선택 결과:", fruit, hobbies, page_mode)

    st.subheader("체크박스 & 버튼")
    show_tip = st.checkbox("팁 보기")
    if show_tip:
        st.info("팁: 위젯 값이 바뀌면 Streamlit은 위에서부터 코드를 다시 실행해요(재실행).")

    if st.button("랜덤 점수 생성"):
        score = int(np.random.randint(0, 101))
        st.success(f"생성된 점수: {score}")

    st.subheader("날짜/시간 입력")
    d = st.date_input("날짜 선택")
    t = st.time_input("시간 선택")
    st.write("선택한 날짜/시간:", d, t)

# =========================================================
# 3) 데이터 출력 & 간단 EDA
# =========================================================
elif page == "3) 데이터 출력 & 간단 EDA":
    st.header("3) 데이터 출력 & 간단 EDA")
    st.subheader("샘플 데이터 생성")

    n = st.slider("데이터 개수(n)", 10, 200, 30)
    seed = st.number_input("seed", min_value=0, max_value=9999, value=0, step=1)
    df = make_df(n=n, seed=seed)

    st.subheader("데이터 보기 (st.table)")
    st.table(df.head(10))

    st.subheader("간단 통계")
    st.metric("행 개수", f"{len(df):,}")
    st.metric("score 평균", f"{df['score'].mean():.2f}")

    st.subheader("그룹별 개수")
    group_counts = df["group"].value_counts().to_frame(name="count")
    st.table(group_counts)

    st.subheader("조건 필터링 실습")
    min_age = st.slider("최소 나이", 18, 60, 25)
    filtered = df[df["age"] >= min_age].copy()
    st.write(f"필터 결과: age >= {min_age} 인 데이터 {len(filtered)}개")
    st.table(filtered.head(10))

    st.subheader("JSON 출력(st.json)")
    summary = {
        "n": int(n),
        "seed": int(seed),
        "min_age": int(min_age),
        "mean_score": float(df["score"].mean()),
        "groups": df["group"].value_counts().to_dict()
    }
    st.json(summary)

# =========================================================
# 4) 미디어
# =========================================================
elif page == "4) 미디어(이미지/오디오/비디오/카메라)":
    st.header("4) 미디어 실습")
    st.subheader("이미지")
    img_url = st.text_input(
        "이미지 URL",
        value="https://images.unsplash.com/photo-1543852786-1cf6624b9987?auto=format&fit=crop&w=900&q=60"
    )
    st.image(img_url, caption="URL 이미지 예시")

    st.subheader("오디오/비디오")
    st.write("오디오/비디오는 URL 또는 로컬 파일 경로로도 가능해요.")
    audio_url = st.text_input("오디오 URL(없으면 비워도 됨)", value="")
    video_url = st.text_input("비디오 URL(없으면 비워도 됨)", value="")

    if audio_url.strip():
        st.audio(audio_url)
    else:
        st.info("오디오 URL을 입력하면 재생기가 나타납니다.")

    if video_url.strip():
        st.video(video_url)
    else:
        st.info("비디오 URL을 입력하면 재생기가 나타납니다.")

    st.subheader("카메라 입력")
    st.write("아래 버튼을 눌러 카메라로 촬영(권한 필요).")
    cam = st.camera_input("사진 촬영")
    if cam is not None:
        st.success("촬영 완료! 아래에 이미지로 표시합니다.")
        st.image(cam)

# =========================================================
# 5) 코드/수식/진행상태
# =========================================================
elif page == "5) 코드/수식/진행상태":
    st.header("5) 코드/수식/진행상태")

    st.subheader("st.code: 코드 표시")
    st.code(
        "import streamlit as st\n"
        "st.title('Hello Streamlit')\n"
        "st.write('code 출력 예시')\n",
        language="python"
    )

    st.subheader("st.echo: 작성 코드 보여주면서 실행")
    with st.echo():
        a = 10
        b = 20
        st.write("a + b =", a + b)

    st.subheader("수식 표시(st.latex)")
    st.latex(r"s^2 = \frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})^2")

    st.subheader("진행 상태(st.progress) + 로딩(spinner)")
    if st.button("진행바 시작"):
        prog = st.progress(0)
        with st.spinner("처리 중..."):
            for i in range(101):
                time.sleep(0.01)
                prog.progress(i)
        st.success("완료!")
