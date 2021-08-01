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


def deleting_file(path: str):
    """
    Функция удоляет указанный файл
    """
    os.remove(path)


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
            deleting_file(path)
    if folderPaths:
        for path in reversed(folderPaths):
            if not (isOnList(dirIgnoreForRemoving, path) or isOnList(config, path)):
                os.rmdir(path)
    os.rmdir(current_path)


def creat_folder(path):
    os.mkdir(path)


def copy_folder(path):
    # пооучить список файлов и папок
    # в папке
    folderPaths, filePaths = getListDirAndFiles(path)
    for folder in folderPaths:
        creat_folder(folder)
    for file in filePaths:
        pass  ## yflj ext


def copy_file(path, copy_to):
    shutil.copyfile(path, copy_to)


def creating():
    """
    Функция обрабатывает объекты с флагот "cha" все из списка change
    """
    pass


def change():
    """
    Функция обрабатывает объекты с флагот "mod" все из списка change
    """
    pass


def renaming():
    """

    """
    pass


def moving():
    """

    """
    pass