import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="OCR 분석 대시보드", layout="centered")

# CSV 불러오기
csv_path = "ocr_analysis_with_similarity.csv"

if not os.path.exists(csv_path):
    st.error(f"CSV 파일이 존재하지 않습니다: {csv_path}")
    st.stop()

df = pd.read_csv(csv_path)

st.title("🧠 OCR 자동화 테스트 분석 대시보드")

# 기본 통계
total = len(df)
success_count = df["Success"].sum()
partial_count = df["Partial Match"].sum()

accuracy = round(success_count / total * 100, 2)
partial_rate = round(partial_count / total * 100, 2)

st.subheader("📊 요약 통계")
st.markdown(f"- 총 테스트 수: **{total}**")
st.markdown(f"- 정확히 일치: **{success_count}개**")
st.markdown(f"- 부분 일치 (유사도 ≥ 90%): **{partial_count}개**")
st.markdown(f"- 🎯 정확도: **{accuracy}%**")
st.markdown(f"- 🟡 부분 일치율: **{partial_rate}%**")

# 필터
st.subheader("🔎 결과 필터링")
filter_option = st.radio("결과 보기 옵션", ("전체", "성공만", "실패만"))

if filter_option == "성공만":
    filtered = df[df["Success"] == True]
elif filter_option == "실패만":
    filtered = df[df["Success"] == False]
else:
    filtered = df

st.dataframe(filtered, use_container_width=True)

# 정확도 vs 부분 일치율 시각화
st.subheader("📈 정확도 / 부분 일치율 그래프")
chart_data = pd.DataFrame({
    '비율': [accuracy, partial_rate]
}, index=['정확도', '부분 일치율'])

st.bar_chart(chart_data)

# Footer
st.markdown("---")
st.caption("Made with 💻 by YOU")
