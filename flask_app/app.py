from flask import Flask, render_template, request
import pytesseract
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        if 'captcha_image' not in request.files or 'not_robot' not in request.form:
            result = "[ERROR] 이미지와 체크박스를 모두 확인해주세요."
        else:
            file = request.files['captcha_image']
            if file.filename != '':
                filepath = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(filepath)
                text = pytesseract.image_to_string(Image.open(filepath)).strip()
                result = text if text else "[EMPTY]"
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
