# ocr_test
* 프로젝트 구조


captcha_project/


├── flask_app/                # Flask 서버 코드


├── dataset/                  # 테스트용 CAPTCHA 이미지들


├── failures/                 # OCR 실패 이미지 저장


├── success/                  # OCR 성공 이미지 저장


├── selenium_log.csv          # 테스트 결과 로그


├── selenium_ocr_runner.py    # Selenium 자동화 봇 코드


├── ocr_dashboard.py          # Streamlit 대시보드


* 설치 및 실행 방법
필수 라이브러리 설치:


pip install -r requirements.txt

Flask 서버 실행:
python flask_app/app.py

Selenium 자동화 실행:
python selenium_ocr_runner.py

Streamlit 대시보드 실행:
streamlit run ocr_dashboard.py
