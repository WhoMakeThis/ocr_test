import pytesseract
from PIL import Image
import os

# Tesseract 경로 설정
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# OCR 평가용 데이터
dataset_path = "dataset/"
test_data = [
    ("captcha_sample1.png", "M7J68")
]

correct = 0
total = len(test_data)

# Tesseract 설정
custom_config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

for file_name, correct_text in test_data:
    image_path = os.path.join(dataset_path, file_name)

    if not os.path.exists(image_path):
        print(f"[ERROR] 파일을 찾을 수 없습니다: {image_path}")
        continue

    image = Image.open(image_path)
    predicted_text = pytesseract.image_to_string(image, config=custom_config).strip()

    print(f"[OCR 결과] {file_name}: '{predicted_text}' (정답: '{correct_text}')")

    if predicted_text == correct_text:
        correct += 1

accuracy = (correct / total) * 100 if total > 0 else 0
print(f"OCR 정확도: {accuracy:.2f}%")
