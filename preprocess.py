import cv2
import pytesseract
import os
import csv
import numpy as np

def preprocess_image(image_path, grayscale=True, blur=True, threshold=True):
    image = cv2.imread(image_path)
    if image is None:
        print(f"[ERROR] 이미지 로드 실패: {image_path}")
        return None

    if grayscale:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if blur:
        image = cv2.GaussianBlur(image, (3, 3), 0)
    if threshold:
        _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    return image

def run_ocr(image):
    text = pytesseract.image_to_string(image, config="--psm 6").strip().lower()
    return text if text else "[EMPTY]"

def overlay_text(image, text):
    if len(image.shape) == 2:  # grayscale
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    overlay = image.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(overlay, f"OCR: {text}", (10, 30), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
    return overlay

def save_image(output_dir, filename, image):
    os.makedirs(output_dir, exist_ok=True)
    save_path = os.path.join(output_dir, filename)
    cv2.imwrite(save_path, image)

def save_log(csv_path, rows):
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Image", "OCR Result", "Ground Truth", "Success", "grayscale", "blur", "threshold"])
        writer.writerows(rows)

if __name__ == "__main__":
    dataset_dir = "./dataset"
    output_csv = "ocr_test_results.csv"
    processed_dir = "./processed"
    fail_dir = "./failures"
    success_dir = "./success"

    results = []
    image_files = [f for f in os.listdir(dataset_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not image_files:
        print("[INFO] 처리할 이미지가 없습니다.")
        exit()

    for image_file in image_files:
        image_path = os.path.join(dataset_dir, image_file)

        if '_' in image_file:
            ground_truth = image_file.split('_')[0].lower()
        else:
            print(f"[WARNING] 정답 추출 실패: {image_file}")
            ground_truth = "[UNKNOWN]"

        for grayscale in [True, False]:
            for blur in [True, False]:
                for threshold in [True, False]:
                    processed = preprocess_image(image_path, grayscale, blur, threshold)
                    if processed is None:
                        continue

                    ocr_result = run_ocr(processed)
                    success = (ocr_result == ground_truth)

                    print(f"[{image_file}] OCR: {ocr_result} | GT: {ground_truth} | {'✅' if success else '❌'}")

                    # OCR 결과 시각화
                    visualized = overlay_text(processed, ocr_result)

                    tag = f"{'gray' if grayscale else 'noGray'}_" \
                          f"{'blur' if blur else 'noBlur'}_" \
                          f"{'thresh' if threshold else 'noThresh'}"

                    filename_tagged = f"{os.path.splitext(image_file)[0]}_{tag}.png"

                    # 모든 전처리 이미지 저장
                    save_image(processed_dir, filename_tagged, visualized)

                    if success:
                        save_image(success_dir, f"success_{filename_tagged}", visualized)
                    else:
                        save_image(fail_dir, f"fail_{filename_tagged}", visualized)

                    # 로그에 저장
                    results.append([
                        image_file,
                        ocr_result,
                        ground_truth,
                        success,
                        grayscale,
                        blur,
                        threshold
                    ])

    save_log(output_csv, results)
    print(f"\n✅ 테스트 완료!")
    print(f"📄 결과: {output_csv}")
    print(f"🖼️ 전처리 이미지: {processed_dir}/")
    print(f"✅ 성공 이미지: {success_dir}/")
    print(f"❌ 실패 이미지: {fail_dir}/")
