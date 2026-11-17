import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

@pytest.fixture
def driver():
    service = ChromeService(ChromeDriverManager().install())
    _driver = webdriver.Chrome(service=service)
    _driver.maximize_window()
    yield _driver
    _driver.quit()

def test_slow_calculator(driver):
    driver.get(
     "https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")
    wait = WebDriverWait(driver, 70)  # Ждем до 70 секунд

    # Устанавливаем задержку
    delay_input = driver.find_element(By.ID, "delay")
    delay_input.clear()
    delay_input.send_keys("45")

    # Нажимаем кнопки
    driver.find_element(By.XPATH, "//button[text()='7']").click()
    driver.find_element(By.XPATH, "//button[text()='+']").click()
    driver.find_element(By.XPATH, "//button[text()='8']").click()
    driver.find_element(By.XPATH, "//button[text()='=']").click()

    # Ждем появления результата. Результат появляется в теге <output>
    result = wait.until(
        EC.visibility_of_element_located((By.TAG_NAME, "output")))

    assert result.text == "15", f"Ожидался результат 15, но - >{result.text}"
