import requests
from bs4 import BeautifulSoup
import json

def parse_headhunter_vacancies(search_query, cities, currency=None):
    base_url = "https://hh.ru/search/vacancy"
    params = {
        "text": search_query,
        "area": cities,
        "currency": currency
    }

    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.text, "html.parser")

    vacancies = []

    for vacancy in soup.find_all("div", class_="vacancy-serp-item"):
        vacancy_info = {}

        vacancy_title_elem = vacancy.find("a", class_="bloko-link")
        vacancy_info["title"] = vacancy_title_elem.text.strip()
        vacancy_info["link"] = vacancy_title_elem["href"]

        salary_elem = vacancy.find("div", class_="vacancy-serp-item__compensation")
        if salary_elem:
            vacancy_info["salary"] = salary_elem.text.strip()
        else:
            vacancy_info["salary"] = "З/П не указана"

        company_elem = vacancy.find("a", class_="bloko-link bloko-link_secondary")
        vacancy_info["company"] = company_elem.text.strip()

        city_elem = vacancy.find("span", class_="vacancy-serp-item__meta-info")
        vacancy_info["city"] = city_elem.text.strip()

        # Проверяем наличие ключевых слов в описании вакансии
        description_elem = vacancy.find("div", class_="g-user-content")
        if description_elem and all(keyword.lower() in description_elem.text.lower() for keyword in ["django", "flask"]):
            vacancies.append(vacancy_info)

    return vacancies

search_query = "Python"
cities = [1, 2]  # 1 - Москва, 2 - Санкт-Петербург
currency = "USD"

vacancies = parse_headhunter_vacancies(search_query, cities, currency)

# Сохраняем результаты в JSON файл
with open("vacancies.json", "w", encoding="utf-8") as f:
    json.dump(vacancies, f, ensure_ascii=False, indent=4)

print("Вакансии успешно сохранены в файл vacancies.json")
