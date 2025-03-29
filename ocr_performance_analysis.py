import pandas as pd
import difflib
import os

# CSV 경로
log_path = "selenium_log.csv"
output_path = "ocr_analysis_with_similarity.csv"

# CSV 불러오기
if not os.path.exists(log_path):
    print(f"[ERROR] 파일 없음: {log_path}")
    exit()

df = pd.read_csv(log_path)

# 유사도 계산 함수 (difflib 사용)
def get_similarity(s1, s2):
    return round(difflib.SequenceMatcher(None, str(s1).lower(), str(s2).lower()).ratio() * 100, 2)

# 유사도 컬럼 추가
df["Similarity (%)"] = df.apply(lambda row: get_similarity(row["OCR Result"], row["Ground Truth"]), axis=1)

# 부분 일치 여부 판단 (기준: 90%)
df["Partial Match"] = df["Similarity (%)"] >= 90

# 통계 출력
total = len(df)
exact_matches = df["Success"].sum()
partial_matches = df["Partial Match"].sum()
accuracy = round((exact_matches / total) * 100, 2)
partial_rate = round((partial_matches / total) * 100, 2)

print("\n📊 OCR 테스트 분석 결과")
print(f"총 테스트 수: {total}")
print(f"정확히 일치 (Success=True): {exact_matches}")
print(f"부분 일치 (유사도 ≥ 90%): {partial_matches}")
print(f"정확도: {accuracy}%")
print(f"부분 일치율: {partial_rate}%")

# 결과 저장
df.to_csv(output_path, index=False)
print(f"\n✅ 분석 결과 저장 완료 → {output_path}")
