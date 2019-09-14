#!/usr/bin/python3
"""
Практическая работа
1) Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из файлов
 info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:

2) Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание
данных. В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить в
соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list,
os_type_list. В этой же функции создать главный список для хранения данных отчета — например, main_data — и поместить
в него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);

3) Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение данных
через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;

4) Проверить работу программы через вызов функции write_to_csv().

5) Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах. Написать
скрипт, автоматизирующий его заполнение данными. Для этого:

6) Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity),
цена (price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря в файл
orders.json. При записи данных указать величину отступа в 4 пробельных символа;

7) Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.

8) Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных в файле
YAML-формата. Для этого:

9) Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом, отсутствующим в
кодировке ASCII (например, €);

10) Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. При этом обеспечить стилизацию
файла с помощью параметра default_flow_style, а также установить возможность работы с юникодом: allow_unicode = True;

11) Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.

Необходимые и достаточные условия:
-- Реализовать скрипт для чтения/записи данных в формате csv;
-- Реализовать скрипт для чтения/записи данных в формате json;
-- Реализовать скрипт для чтения/записи данных в формате yaml;
-- Реализовать скрипт для преобразования данных в формате csv в формат json;
-- Реализовать скрипт для преобразования данных в формате csv в формат yaml;
-- Реализовать скрипт для преобразования данных в формате json в формат yaml.

"""
import chardet
import os
import csv
import json
import yaml
from pprint import pprint
import re
from datetime import datetime
from collections import OrderedDict


def check_file_encoding(filepath):
    if os.path.isfile(filepath):
        with open(filepath, "rb") as file:
            return chardet.detect(file.read())["encoding"]
    else:
        print(f"{filepath} is not a file")
        exit()


def read_yaml(filepath):
    with open(filepath) as file:
        return yaml.safe_load(file)


def read_textfile(filepath):
    with open(filepath, encoding=check_file_encoding(filepath)) as file:
        return file.read()


def read_json(filepath):
    with open(filepath) as file:
        return json.load(file)


def get_data():
    pathlist = [os.path.join("data", f"info_{i}.txt") for i in range(1, 4)]
    # Изготовитель системы, Название ОС, Код продукта, Тип системы
    os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []
    main_data = ["Изготовитель системы", "Название ОС", "Код продукта", "Тип системы"]

    for filepath in pathlist:
        file_text = read_textfile(filepath)
        os_prod_list.append(" ".join(re.findall(f"{main_data[0]}.*", file_text)[0].split()[2:]))
        os_name_list.append(" ".join(re.findall(f"{main_data[1]}.*", file_text)[0].split()[2:]))
        os_code_list.append(" ".join(re.findall(f"{main_data[2]}.*", file_text)[0].split()[2:]))
        os_type_list.append(" ".join(re.findall(f"{main_data[3]}.*", file_text)[0].split()[2:]))
        with open(filepath + "_main_data", "w", encoding="utf-8") as file:
            file.write(",".join([os_prod_list[-1], os_name_list[-1], os_code_list[-1], os_type_list[-1]]))

    with open(os.path.join("data", "main_data"), "w", encoding="utf-8") as file:
        file.write(",".join(main_data))

    return [main_data, os_prod_list, os_name_list, os_code_list, os_type_list]


def write_to_csv(output_filepath):
    with open(output_filepath, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        data = get_data()
        writer.writerow(data[0])
        for rownum in range(len(data[1])):
            writer.writerow([data[colnum][rownum] for colnum in range(1, len(data))])


def write_order_to_json(item, quantity, price, buyer, date):
    json_path = os.path.join("data", "orders.json")
    old_orders = read_json(json_path)
    old_orders["orders"].append({"item": item, "quantity": quantity, "price": price, "buyer": buyer, "date": date})
    with open(json_path, "w") as file:
        json.dump(old_orders, file)


if __name__ == "__main__":
    write_to_csv(os.path.join("data", "main_data.csv"))
    write_order_to_json("some new item", 158, 100500, "Ivan Doolin", str(datetime.now()))

    dict_for_yaml = OrderedDict()
    dict_for_yaml["firstkey"] = ["some", "list", "with", "garbage", "text"]
    dict_for_yaml["secondkey"] = 100500
    dict_for_yaml["thirdkey"] = {"€": 72.33, "¥": 9.9697}

    with open(os.path.join("data", "task.yml"), "w", encoding="utf-8") as file:
        # dumper = yaml.Dumper(stream=file, default_flow_style=True, allow_unicode=True)
        yaml.dump(data=dict_for_yaml, stream=file, default_flow_style=True, allow_unicode=True)

    with open(os.path.join("data", "task.yml"), encoding="utf-8") as file:
        from_yaml = yaml.load(file, Loader=yaml.Loader)
        print(type(from_yaml))
        pprint(from_yaml)
