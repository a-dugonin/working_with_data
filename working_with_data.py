import json
import re
from typing import Any
from bs4 import BeautifulSoup
from requests import Response, get

# task_1 (lorem_ipsum)

text: str = """ Lorem ipsum dolor sit amet, consectetuer adipiscing elit. 
Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes,
nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. 
Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate 
"""

template: str = r"\b\w{4}\b"

lorem_ipsum_result: list = re.findall(template, text)

# task_2 (Registration plates)

scroll: str = "А578ВЕ777 ОР233787 К901МН666 СТ46599 СНИ2929П777 666АМР666"
cars_template: str = r"[АВЕКМНОРСТУХ]\d{3}[АВЕКМНОРСТУХ]{2}\d{2,3}"
taxi_template: str = r"[АВЕКМНОРСТУХ]{2}\d{5,6}"
cars: list = re.findall(cars_template, scroll)
taxi: list = re.findall(taxi_template, scroll)
registration_plates_result: str = (
    f"Список номеров частных автомобилей: {cars}\nСписок номеров такси: {taxi}"
)

# task_3 (May the force be with you)

request_ship: Response = get("https://www.swapi.tech/api/starships/12")
data_ship: dict = json.loads(request_ship.text)
ship: dict = {
    "max_atmosphering_speed": data_ship["result"]["properties"]["max_atmosphering_speed"],
    "name": data_ship["result"]["properties"]["name"],
    "starship_class": data_ship["result"]["properties"]["starship_class"],
    "pilots": [],
}

for pilot in data_ship["result"]["properties"]["pilots"]:
    pilot_data: dict = json.loads(get(pilot).text)
    planet_data: dict = json.loads(
        get(pilot_data["result"]["properties"]["homeworld"]).text
    )

    pilot_info: dict = {
        "name": pilot_data["result"]["properties"]["name"],
        "height": pilot_data["result"]["properties"]["height"],
        "mass": pilot_data["result"]["properties"]["mass"],
        "homeworld": pilot_data["result"]["properties"]["homeworld"],
        "planet": planet_data["result"]["properties"]["name"],
    }

    ship["pilots"].append(pilot_info)

starship: json = json.dumps(ship, indent=4)

with open("starship.json", "w") as json_file:
    json.dump(ship, json_file, indent=4)


# task_4 (Phone numbers)


def number_to_words(num):
    """ Функция для перевода числового значения в его строковое представление """
    list1: list = [
        "первый",
        "второй",
        "третий",
        "четвертый",
        "пятый",
        "шестой",
        "седьмой",
        "восьмой",
        "девятый",
        "десятый",
    ]
    list2: list = [
        "одиннадцатый",
        "двенадцатый",
        "тринадцатый",
        "четырнадцатый",
        "пятнадцатый",
        "шестнадцатый",
        "семнадцатый",
        "восемнадцатый",
        "девятнадцатый",
    ]
    list3: list = [
        "двадцать",
        "тридцать",
        "сорок",
        "пятьдесят",
        "шестьдесят",
        "семьдесят",
        "восемьдесят",
        "девяносто",
    ]
    if num <= 10:
        return list1[num - 1]
    elif 10 < num < 20:
        return list2[num - 10 - 1]
    elif 20 <= num < 100:
        k = num % 10
        n = num // 10
        if k == 0:
            return list3[n - 2]
        else:
            return list3[n - 2] + " " + list1[k - 1]


def check_numbers():
    """ Функция для проверки номера телефона на валидность """
    phone_numbers: list = ["9999999999", "999999-999", "99999x9999"]
    template_number: str = r"[89]\d{9}"
    for index in range(len(phone_numbers)):
        if bool(re.match(template_number, phone_numbers[index])):
            print(f"{number_to_words(index + 1)} номер: всё в порядке")
        else:
            print(f"{number_to_words(index + 1)} номер: не подходит")


# task_5 (Web scraping)


url: str = "https://htmlbook.ru/html/h3"
response: Response = get(url)
soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
h3_list: list = [h3.get_text() for h3 in soup.find_all("h3")]

# task_6 (Finding the difference between two JSON files)


def deserialization(file_name):
    """ Функция для десериализации json файла в словарь """
    with open(file_name) as file_json:
        data: dict = json.load(file_json)
        return data


old_json: dict = deserialization("json_old.json")
new_json: dict = deserialization("json_new.json")

diff_list: list = ["services", "staff", "datetime"]
result_diff_json: dict = {}

for key in diff_list:
    if old_json["data"][key] != new_json["data"][key]:
        result_diff_json[key]: Any = new_json["data"][key]

with open("result.json", "w") as file:
    json.dump(result_diff_json, file, indent=4)
