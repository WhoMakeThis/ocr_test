from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# WebDriver 탐지 우회 (JavaScript 삽입)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    });
    """
})

driver.get("https://www.google.com/recaptcha/api2/demo")
time.sleep(2)

# iframe 접근 및 체크박스 클릭 (필요 시)
iframe = driver.find_element(By.XPATH, "//iframe[contains(@src, 'recaptcha')]")
driver.switch_to.frame(iframe)
checkbox = driver.find_element(By.CLASS_NAME, "recaptcha-checkbox-border")
checkbox.click()

print("✅ navigator.webdriver 우회 + CAPTCHA 체크박스 클릭")
time.sleep(5)
driver.quit()
