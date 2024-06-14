from selenium_code import try_
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

import os
import configparser


# Инициализация colorama
init(autoreset=True)

config = configparser.ConfigParser()
config.read('main\config.ini', encoding='utf-8')

def viewHTML(file_content):
    soup = BeautifulSoup(file_content, "html.parser")
    rows = soup.find_all("tr")

    results = []
    no_results = []

    for row in rows:
        cells = row.find_all("td")
        if cells:
            date = cells[0].text.strip()
            subject = cells[1].text.strip()
            test_score = cells[2].text.strip()
            min_score = cells[3].text.strip()
            mark = cells[4].text.strip()
            status = cells[5].text.strip()

            if row.find("a"):
                results.append((date, subject, test_score, min_score, mark, status))
            else:
                no_results.append((date, subject, "-", "-", "-", "Результатов пока нет"))

    print_results(results, no_results)

def print_results(results, no_results):
    print(Fore.YELLOW + Style.BRIGHT + "Результаты экзаменов:")
    print(Fore.YELLOW + Style.BRIGHT + "{:<15} {:<30} {:<15} {:<15} {:<10} {:<20}".format("Дата экзамена", "Предмет", "Тестовый балл", "Мин. балл", "Отметка", "Статус"))

    for result in results:
        print(Fore.GREEN + "{:<15} {:<30} {:<15} {:<15} {:<10} {:<20}".format(result[0], result[1], result[2], result[3], result[4], result[5]))

    for no_result in no_results:
        print(Fore.RED + "{:<15} {:<30} {:<15} {:<15} {:<10} {:<20}".format(no_result[0], no_result[1], no_result[2], no_result[3], no_result[4], no_result[5]))

def openHTML():
    with open('output.html', 'r', encoding='utf-8') as file:
        return file.read()

def main():
    file_content = openHTML()
    viewHTML(file_content)
    os.remove("output.html")

try:
    if not config["Settings"].get("surname") or not config["Settings"].get("code"):
        if not config["Settings"].get("surname"):
            config["Settings"]["surname"] = input("Фамилия: ")
        if not config["Settings"].get("code"):
            config["Settings"]["code"] = input("Код: ")

        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    else:
        try_(surname=config["Settings"]["surname"], code=config["Settings"]["code"])
        main()
except Exception as e:
    print(f"Произошла ошибка: {e}")
finally:
    pass