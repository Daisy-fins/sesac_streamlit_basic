import time
import pandas as pd
import streamlit as st

# =========================
# 1) PDF 1페이지 구성
# =========================
st.title("나만의 작고 소중한 대시보드")
st.header("실습 예제 작성중!")

st.write("이 대시보드는 Streamlit을 활용하여 만들어졌습니다.")

# (조건 1) '여기' 하이퍼링크: PDF에 있는 링크 주소 그대로
st.markdown("이곳에서는 다양한 *Streamlit* 함수를 활용할 수 있습니다. [여기](https://docs.streamlit.io/)를 클릭하여 더 알아보세요.")

st.markdown("---")

# 예시 데이터프레임
df = pd.DataFrame(
    {
        "상품": ["A", "B", "C", "D"],
        "판매량": [100, 150, 200, 50],
        "작년대비 증감비": ["+10%", "+5%", "+7%", "-15%"],
    }
)

# 표 출력
st.table(df)

# (조건 2) 최대 판매량 metric: DF 값이 바뀌어도 동작하도록(계산 기반)
max_row = df.loc[df["판매량"].idxmax()]
max_sales = int(max_row["판매량"])
max_delta = str(max_row["작년대비 증감비"])

st.metric("최대 판매량", max_sales, max_delta)

# (조건 3) selectbox 선택값에 따라 아래 문구 동적 변경
st.write("어떤 상품의 정보를 보시겠습니까?")
selected = st.selectbox(" ", df["상품"].tolist(), index=0, label_visibility="collapsed")
selected_sales = int(df.loc[df["상품"] == selected, "판매량"].iloc[0])
st.write(f"{selected}의 판매량은 {selected_sales}입니다.")

st.markdown("---")
st.latex(r"l = 2\pi r")

# =========================
# 2) PDF 2페이지 구성
# =========================
st.markdown("---")
st.header("냥이!")

# (조건 4) 이미지: 원하는 이미지, width=200, caption
# - 파일이 없을 수 있으니 URL로 처리(원하면 로컬 경로로 바꿔도 됨)
img_url = "https://images.unsplash.com/photo-1592194996308-7b43878e84a6?auto=format&fit=crop&w=600&q=60"
st.image(img_url, width=200, caption="냥이 이미지")

""
st.markdown("---")
# 코드 출력
st.code("print('Hello, Streamlit!')", language="python")

# 경고 문구
st.warning("이 텍스트는 경고용 메세지 입니다.")

""
st.markdown("---")
# (조건 5) 성공 버튼: 풍선 + 성공메시지
if st.button("성공 버튼"):
    st.balloons()
    st.success("성공!")

""
st.markdown("---")
# (조건 6) 이름 입력 → 출력문구 변경
name = st.text_input("이름을 입력하세요:")
st.write(f"안녕하세요, {name}님!")

""
st.markdown("---")
# (조건 7) 컬러 선택 → HEX 출력
color = st.color_picker("색상을 선택하세요", value="#000000")
st.write(f"선택한 색상은 {color}입니다.")

# =========================
# 3) PDF 3페이지 구성
# =========================
st.markdown("---")

# (조건 8) 진행 버튼: 0→100%를 1초에 10%씩, 하나의 progress bar 업데이트
if st.button("진행 버튼"):
    progress_bar = st.progress(0)
    for p in range(0, 101, 10):     # 0,10,20,...,100
        progress_bar.progress(p)
        if p < 100:
            time.sleep(1)
