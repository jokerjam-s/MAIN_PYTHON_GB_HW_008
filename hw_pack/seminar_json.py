"""Погружение в Python. Сериализация"""


import json
from typing import TextIO
from pathlib import Path

__all__ = ['ui', 'add_data', 'write_json', 'create_json', 'txt_to_json', 'read_json', 'two_files_in_one', 'make_base']

def _read_or_begin(fd: TextIO) -> str:
    line = fd.readline()
    if not line:
        fd.seek(0)
        return _read_or_begin(fd)
    return line[:-1]


def two_files_in_one(numbers: Path, words: Path, result: Path) -> None:
    with (open(numbers, 'r', encoding='utf-8') as f_num,
          open(words, 'r', encoding='utf-8') as f_word,
          open(result, 'w', encoding='utf-8') as f_res
          ):
        len_numbers = sum(1 for _ in f_num)
        len_word = sum(1 for _ in f_word)
        for _ in range(max(len_numbers, len_word)):
            num = _read_or_begin(f_num)
            word = _read_or_begin(f_word)
            num_a, num_b = num.split('|')
            mult = int(num_a) * float(num_b)
            if mult < 0:
                f_res.write(f'{word.lower()} {abs(mult)}\n')
            elif mult > 0:
                f_res.write(f'{word.upper()} {round(mult)}\n')


def txt_to_json(file: Path) -> None:
    file_data = {}
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            name, number = line.split(" ")
            file_data[name.capitalize()] = float(number)
    with open(file.stem + '.json', 'w') as f:
        json.dump(file_data, f, indent=2)


def create_json(file: Path) -> None:
    file_data = {}
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            name, number = line.split()
            file_data[name.capitalize()] = float(number)
    with open(file.stem + '.json', 'w', encoding='utf-8') as f_2:
        json.dump(file_data, f_2, ensure_ascii=False, indent=2)


def add_data(name: str, personal_id: int, level: int) -> dict[int, dict[str, int]]:
    return {level: {personal_id: name}}


def write_json(data: dict) -> None:
    file = 'data.json'
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_json():
    with open("data.json", "r", encoding='utf-8') as read_file:
        # data = read_file.read()
        # if data:
        #     return {}
        data_from_file = json.load(read_file)
    return data_from_file


def make_base(data_to_write: dict):
    base_list = []
    read_data = read_json()
    base_list.append(read_data)
    return base_list


def ui():
    base_dict = read_json()
    exit_program = False
    print("Добро пожаловать в программу. Введите данные для создания файла...")
    while not exit_program:
        personal_id = int(input("Введите id: "))
        name = input("Введите имя: ")
        level = int(input("Введите уровень доступа: "))
        continue_program = input("Хотите продолжить? да/нет")
        if continue_program == 'нет':
            exit_program = True
        res_dict = (add_data(name, personal_id, level))
        if level in base_dict:
            base_dict[level].update({personal_id: name})
        else:
            base_dict[level] = {personal_id: name}
    write_json(base_dict)
