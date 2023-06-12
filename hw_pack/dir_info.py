# Напишите функцию, которая получает на вход директорию и рекурсивно обходит её и все вложенные директории.
# Результаты обхода сохраните в файлы json, csv и pickle.
# - Для дочерних объектов указывайте родительскую директорию.
# - Для каждого объекта укажите файл это или директория.
# - Для файлов сохраните его размер в байтах, а для директорий размер файлов в ней с учётом всех
# вложенных файлов и директорий.
__all__ = ['dir_info', 'save_to_csv', 'save_to_picle', 'save_to_json']

from pathlib import Path
import pickle
import json
import csv

KEY_PARENT = 'parent'
KEY_SIZE = 'size'
KEY_TYPE = 'type'
KEY_NAME = 'name'
KEY_CHILD = 'child'

THIS_FILE = 'file'
THIS_DIR = 'dir'


def save_to_json(info: dict, file_name: str):
    with open(file_name, "w") as f:
        json.dump(info, f, indent=2)


def save_to_csv(info: dict, file_name: str):
    with open(file_name, "w", encoding="UTF-8", newline='') as f:
        csw_writer = csv.DictWriter(f, dialect='excel', quoting=csv.QUOTE_MINIMAL,
                                    fieldnames=[KEY_PARENT, KEY_NAME, KEY_SIZE, KEY_TYPE])
        csw_writer.writeheader()
        dict_info = []
        _dict_info(info, dict_info)

        csw_writer.writerows(dict_info)


def save_to_picle(info: dict, file_name: str):
    with open(file_name, "wb") as f:
        pickle.dump(info, f)


def dir_info(path: str = None) -> dict:
    """Получение информации о каталоге path. Если не указан - обрабатывается текущий каталог."""
    start_path = Path().cwd() if path is None else Path(path)
    return _file_info(start_path)


def _dict_info(info: dict, list_info: list) -> list:
    csv_dict = {
        KEY_PARENT: info.get(KEY_PARENT, ""),
        KEY_NAME: info.get(KEY_NAME, ""),
        KEY_TYPE: info.get(KEY_TYPE, ""),
        KEY_SIZE: info.get(KEY_SIZE, 0)
    }
    list_info.append(csv_dict)
    list_child = info.get(KEY_CHILD, None)
    if list_child is not None:
        for c in list_child:
            _dict_info(c, list_info)
    return list_info


def _file_info(file: Path) -> dict:
    """Формирование словаря информации о файле"""
    info = {KEY_PARENT: file.parent.name, KEY_NAME: file.name}
    if file.is_file():
        info[KEY_SIZE] = file.stat().st_size
        info[KEY_TYPE] = THIS_FILE
    else:
        info[KEY_TYPE] = THIS_DIR
        info[KEY_SIZE] = 0
        list_child = []
        for p in file.iterdir():
            child = _file_info(p)
            info[KEY_SIZE] += child.get(KEY_SIZE, 0)
            list_child.append(child)
        info[KEY_CHILD] = list_child

    return info


if __name__ == '__main__':
    print(dir_info())
