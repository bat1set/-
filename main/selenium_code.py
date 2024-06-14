from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Укажите путь к вашему Edge WebDriver
driver_path = 'main\edge\msedgedriver.exe'

# Создайте экземпляр сервиса для Edge WebDriver
service = Service(executable_path=driver_path)

# Создайте экземпляр веб-драйвера, используя сервис
driver = webdriver.Edge(service=service)

def enter_text_slowly(element, text, delay=1):
    """Ввод текста по буквам с заданной задержкой"""
    element.clear()
    for char in text:
        element.send_keys(char)
        time.sleep(delay)

def save_page_source(filename):
    """Сохранение HTML-кода страницы в файл"""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(driver.page_source)
        print(f"HTML-код страницы сохранен в {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении HTML-кода страницы: {e}")

def attempt_login(surname, code):
    try:
        # Откройте нужную страницу
        driver.get('https://result9.coko38.ru/')

        # Ожидание загрузки элемента 'fio'
        fio_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'fio'))
        )

        # Ввод текста в поле 'fio'
        fio_input.send_keys(surname)

        # Заполните поле 'registrationCode'
        reg_code_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'registrationCode'))
        )

        # Ввод текста в поле 'registrationCode'
        reg_code_input.send_keys(code)

        # Установите чекбокс 'termsOfService'
        terms_checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'termsOfService'))
        )
        terms_checkbox.click()

        # Ожидание загрузки и прохождения reCAPTCHA
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'g-recaptcha-response'))
        )

        # Нажмите кнопку отправки формы
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
        )
        submit_button.click()

        # Ожидание загрузки новой страницы
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )

        # Сохранение HTML-кода новой страницы
        save_page_source('output.html')

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        retry_login(surname, code)

def retry_login(surname, code):
    try:
        fio_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'fio'))
        )
        enter_text_slowly(fio_input, surname)

        reg_code_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'registrationCode'))
        )
        enter_text_slowly(reg_code_input, code)

        terms_checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'termsOfService'))
        )
        terms_checkbox.click()

        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
        )
        submit_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )

        # Сохранение HTML-кода новой страницы
        save_page_source('output.html')

    except Exception as e:
        print(f"Повторная попытка завершилась ошибкой: {e}")

def try_(surname, code):
    try:
        attempt_login(surname, code)
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
    finally:
        driver.quit()
