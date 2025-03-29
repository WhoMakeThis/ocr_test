from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import csv

# 로그 저장 함수
def save_log(csv_path, row):
    file_exists = os.path.exists(csv_path)
    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Image", "OCR Result", "Ground Truth", "Success", "Timestamp"])
        writer.writerow(row)

# 단일 테스트 함수
def run_test(driver, image_path, ground_truth, log_path):
    driver.get("http://127.0.0.1:5000/")
    time.sleep(1)

    # 파일 업로드
    file_input = driver.find_element(By.NAME, "captcha_image")
    file_input.send_keys(os.path.abspath(image_path))

    # 체크박스 클릭
    checkbox = driver.find_element(By.ID, "not_robot")
    if not checkbox.is_selected():
        checkbox.click()

    # 제출
    submit_btn = driver.find_element(By.ID, "submit-btn")
    submit_btn.click()
    time.sleep(1)

    # 결과 추출
    result_text = driver.find_element(By.TAG_NAME, "p").text.strip()
    ocr_result = result_text
    success = (ocr_result.lower() == ground_truth.lower())

    print(f"[{os.path.basename(image_path)}] OCR: {ocr_result} | GT: {ground_truth} | {'✅' if success else '❌'}")

    # 실패 시 이미지 저장
    if not success:
        fail_dir = "failures"
        os.makedirs(fail_dir, exist_ok=True)
        from shutil import copyfile
        copyfile(image_path, os.path.join(fail_dir, f"{os.path.splitext(os.path.basename(image_path))[0]}_fail.png"))

    save_log(log_path, [os.path.basename(image_path), ocr_result, ground_truth, success, time.strftime('%Y-%m-%d %H:%M:%S')])

# 메인 실행
if __name__ == "__main__":
    dataset_dir = "./dataset"
    log_file = "selenium_log.csv"
    ground_truth_map = { "captcha_sample1.png": "M7J68" }

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        for filename, ground_truth in ground_truth_map.items():
            image_path = os.path.join(dataset_dir, filename)
            if os.path.exists(image_path):
                run_test(driver, image_path, ground_truth, log_file)
            else:
                print(f"[ERROR] 이미지 없음: {image_path}")
            time.sleep(1)
    finally:
        driver.quit()
        print(f"\n✅ 전체 테스트 완료! 결과는 '{log_file}'에 저장됨.")