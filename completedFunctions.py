import sys
import os
from functionsForDebugging import printList


def checkingProgPerformance(value):
    """
    Проверка работоспособности программы
    Function terminates the program if value = False
    :param value: boolean
    """
    if not value:
        print("PermissionError")
        sys.exit(-1)

def checkOS():
    """
    Function return: True if operating system - Linux and False if the other
    """
    if sys.platform == "linux":
        return True
    else:
        print("Your operating system is not suitable")
        return False


def chekingAccessToDirectory(directory):
    """
    The function checks has current user
    rights to read / write the directory

    If the directory does not exist,
    then the function will create it

    :return: True if there is access and False if not
    """
    if os.path.isdir(directory):
        if not os.path.exists(directory):
            try:
                os.mkdir(directory)
            except PermissionError:
                # PermissionError
                return False
    else:
        print(directory, " не является директорией")
        return False

    return os.access(directory, os.R_OK) and os.access(directory, os.W_OK)


def readConfig(fName):
    """
    Function reads config file and add specified path to list.

    Instead of the "~" character, the path to the user's
    home directory is substituted

    :param fName: name of file config
    :return: list
    """
    #try:
    #    fp = open(fName)
    #except PermissionError:
    #    return False, []
    #else:
    #    with fp:
    #        list1 = fp.readlines()
    #finally:
    #    fp.close()
    try:
        with open(fName) as fp:
            list1 = fp.readlines()

        list1 = [line.rstrip() for line in list1]  # remove "\n" at the ends of lines

        home = os.path.expanduser("~")

        for i, line in enumerate(list1):
            if line[0] == "~":
                list1[i] = home + line[1:len(line)]
            # Checking access rights (read / write) to a directory
            if not chekingAccessToDirectory(list1[i]):
                return False, list1

        return True, list1

    except  FileNotFoundError:
        print("Нет файла: ", fName)

def getListDirAndFiles(directory):
    """
    Функция рекурсивно обходить дигекторию directory и
    возвращает 2 списка:
    1. список путей к папкам, ноходящимся в directory
    2. список путей к файлам, находящимся в directory
    """
    folderPaths = []
    filePaths = []

    for dirpath, dirnames, filenames in os.walk(directory):
        # перебрать каталоги
        for dirname in dirnames:
            #print(os.path.join(dirpath, dirname))
            folderPaths.append(os.path.join(dirpath, dirname))
        # перебрать файлы
        for filename in filenames:
            #print(os.path.join(dirpath, filename))
            filePaths.append(os.path.join(dirpath, filename))

    return folderPaths, filePaths


def getInodeAndDevID(path):
    """
    Возвращает inode и id устройства на котором хранится файл или папка
    хранящаяся по пути path
    """
    A = os.path.split(path)
    name = A[1]  # название папки файла для которого получаем inode и deviseID
    path = A[0]
    with os.scandir(path) as itr:
        for entry in itr:
            if name == entry.name:
                return entry.stat().st_ino, entry.stat().st_dev

    return None


def isOnList(list1, path):
    """
    Проверяет находится ли path в списке list1
    """
    for line in list1:
        if line == path:
            return True

    return False

def getListFromFile(fName):
    """
    функция прочитает файл и верет список
    :param fName:
    :return: список
    """
    with open(fName) as f:
        return f.read().splitlines()
