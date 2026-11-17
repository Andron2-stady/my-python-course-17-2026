import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService

@pytest.fixture
def driver():
    service = FirefoxService(GeckoDriverManager().install())
    _driver = webdriver.Firefox(service=service)
    _driver.maximize_window()
    yield _driver
    _driver.quit()

def test_shop_purchase(driver):
    driver.get("https://www.saucedemo.com")
    wait = WebDriverWait(driver, 10)

    # Авторизация
    wait.until(EC.visibility_of_element_located(
        (By.ID, "user-name"))).send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # Добавляем товары в корзину по названию
    items_to_add = [
        "Sauce Labs Backpack",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Onesie"
    ]

    for item_name in items_to_add:
        # Находим кнопку Add to cart для конкретного товара
        add_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, f"//div[text()='{
                item_name}']/following-sibling::div/button"
        )))
        add_button.click()

    # Переходим в корзину
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    # Проверяем, что в корзине именно наши товары (опционально)
    cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(cart_items) == 3, "В корзине должно быть 3 товара"

    # Оформление заказа
    driver.find_element(By.ID, "checkout").click()

    # Заполняем форму (можно использовать свои данные)
    driver.find_element(By.ID, "first-name").send_keys("Иван")
    driver.find_element(By.ID, "last-name").send_keys("Петров")
    driver.find_element(By.ID, "postal-code").send_keys("101000")

    driver.find_element(By.ID, "continue").click()

    # Получаем итоговую сумму
    total_text = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "summary_total_label"))).text
    # Текст на странице выглядит как "Total: $58.29"
    total_value = total_text.split("$")[-1]

    assert total_value == "58.29", f"Ожидалась сумма $58.29, но получено ${
        total_value}"
