import os
import sys
import json
import shutil

from completedFunctions import getListDirAndFiles, getListDirIgnoreForRemovingAndCleaning, isOnList

# обработка изменений
"""
Модуль позволяет обработать изменения во всех папках из списка config, такие как:
    -Удаление папки и файла;
    -Переименование папки и файла;
    -Перемещение папки и файла;
    -Создание папки и файла;
    -Изменение папки и файла;
"""


def clearing(change, folders_in_config):
    """
    Функция удоляет ненужные изменения в списке
    """
    ### Надо убрать дубли из словаря
    flag_for_del = True
    for id, value in list(change.items()):
        for folder in folders_in_config:
            if id.split()[1][1:].startswith(folder):  # содержится ли файл\папка в папках конфига
                flag_for_del = False
        if flag_for_del:
            del change[id]
        flag_for_del = True


def deleting_link(path: str):
    """
    Функция удоляет символическую ссылку на папку\файл
    """
    #print(f"\nУдоляю ссылку {path}\n")
    os.unlink(path)


def deleting_file(path: str):
    """
    Функция удоляет указанный файл
    """
    if os.path.exists(path):
        os.remove(path)
    else:
        print(f"Файла {path} не существует, его нельзя удалить")


def deleting_directory(current_path: str):
    """
    Функция полностью очищает указанную директорию и удоляет саму папку
    """

    with open(sys.argv[1], 'r') as file:
        config = json.loads(file.read())
    dirIgnoreForRemoving = config[:]
    folderPaths, filePaths = getListDirAndFiles(current_path)
    print("\nfolders", folderPaths)
    print("\nfiles", filePaths)
    if filePaths:
        for path in filePaths:
            if os.path.islink(path):
                deleting_link(path)
            else:
                deleting_file(path)
    if folderPaths:
        for path in reversed(folderPaths):
            if not (isOnList(dirIgnoreForRemoving, path) or isOnList(config, path)):
                if os.path.islink(path):
                    deleting_link(path)
                else:
                    os.rmdir(path)

    if os.path.islink(current_path):
        deleting_link(current_path)
    else:
        os.rmdir(current_path)


def creat_link(path, copy_to):
    """
    Функция создает ссылку на файл \ папку
    """
    #print(f"\nСоздаю ссылку {copy_to}\n")
    os.symlink(path, copy_to)


def creat_folder(path):
    if os.path.exists(path):
        pass  # Обработать
    else:
        os.mkdir(path)


def copy_file(path, copy_to):
    if os.path.islink(path):  # является ли путь символической ссылкой.
        os.symlink(path, copy_to)
    else:
        shutil.copyfile(path, copy_to)


def change_file(path, change_it):
    """
    Функция удоляет файл change_it и перемещает path вместо него
    """
    deleting_file(change_it)
    copy_file(path, change_it)
