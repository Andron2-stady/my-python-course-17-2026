import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Определяем браузер в зависимости от ОС
import platform
system = platform.system()

@pytest.fixture
def driver():
    if system == "Windows":
        from selenium.webdriver.edge.service import Service as EdgeService
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
        service = EdgeService(EdgeChromiumDriverManager().install())
        _driver = webdriver.Edge(service=service)
    elif system == "Darwin":  # вmacOS
        _driver = webdriver.Safari()
    else:
        pytest.skip("Тесты для формы поддерживают только Windows (Edge) и macOS (Safari)")

    _driver.maximize_window()
    yield _driver
    _driver.quit()

def test_form_submission(driver):
    driver.get(
     "https://bonigarcia.dev/selenium-webdriver-java/data-types.html")
    wait = WebDriverWait(driver, 10)

    # Заполняем форму
    wait.until(EC.visibility_of_element_located(
        (By.NAME, "firstName"))).send_keys("Иван")
    driver.find_element(By.NAME, "lastName").send_keys("Петров")
    driver.find_element(By.NAME, "address").send_keys("Ленина, 55-3")
    driver.find_element(By.NAME, "email").send_keys("test@skypro.com")
    driver.find_element(By.NAME, "phone").send_keys("+7985899998787")
    # Zip code оставляем пустым
    driver.find_element(By.NAME, "city").send_keys("Москва")
    driver.find_element(By.NAME, "country").send_keys("Россия")
    driver.find_element(By.NAME, "job").send_keys("QA")
    driver.find_element(By.NAME, "company").send_keys("SkyPro")

    # Отправляем форму
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Проверка валидации
    zip_code = driver.find_element(By.NAME, "zip")
    assert "is-invalid" 
    in zip_code.get_attribute("class"), "в поле Zip code подсветка красным (invalid)"

    valid_fields = ["firstName", "lastName", "address", "email", "phone", "city", "country", "job", "company"]
    for field_name in valid_fields:
        field = driver.find_element(By.NAME, field_name)
        assert "is-valid" in field.get_attribute("class"), f"в поле {field_name} подсветка зеленым (valid)"
