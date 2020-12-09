# Local Directory Content Synchronization Service
import os
import sys
from os import DirEntry as de

def checkingProgPerformance(value):
    """
    Проверка работоспособности программы
    Function terminates the program if value = False
    :param value: boolean
    """
    if not value:
        print("PermissionError")
        sys.exit(0)


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
        print(directory, "директория")
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
    try:
        fp = open(fName)
    except PermissionError:
        return False, []
    else:
        with fp:
            list1 = fp.readlines()
    finally:
        fp.close()

    list1 = [line.rstrip() for line in list1]  # remove "\n" at the ends of lines

    home = os.path.expanduser("~")

    for i, line in enumerate(list1):
        if line[0] == "~":
            list1[i] = home + line[1:len(line)]
        # Checking access rights (read / write) to a directory
        if not chekingAccessToDirectory(list1[i]):
            return False, list1

    return True, list1


def GetListDirAndFiles(directory):
    '''
    Функция рекурсивно обходить дигекторию directory и
    возвращает 2 списка:
    1. список путей к папкам, ноходящимся в directory
    2. список путей к файлам, находящимся в directory
    '''
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
    Проверяет находится ли path в списке list(
    планирую использовать для проверки находится ли папка внутри конфига
    """
    for line in list1:
        if line == path:
            return True

    return False


def someFun():
    pass


def getListDirIgnoreDel(paths):
    """
    Функция возвращает список папок, которые нельзя удолять
    К ним относятся:
    - все папки из списка paths
    - все подпапки первой папки(mainFolder) из path (если они не
    кофликтуют со списком paths)
    то есть если mainFolder содержит в себе папку "f1" из конфига,
    то папки из папки "f1" не должны попасть в listDir
    :param paths: список директорий
    """
    listDir = paths  # список директорий, которые нельзя удолять
    print("config:")
    #for path in paths:
        #print(path)
    print()
    mainFolder = paths[0]
    # поиск папок в mainFolder
    folderPaths, _ = GetListDirAndFiles(mainFolder)
    for path in folderPaths:
        if isOnList(paths, path):
            print()
        else:
            ### проверка вложенности директорий
            someFun()
            pass
    return listDir


def deletingFilesAndFolders(directory, dirIgnore):
    """
    Функция удоляет все файлы и папки в указанной директории
    за исключением тех, которые находятся в dirIgnore
    1.Директория пустая
    2.В ней есть папки
    3.В ней есть файлы и ссылки(мягкие и жесткии)
    4.В ней есть и папки и файлы и ссылки
    dirIgnore список директорий, которые не будут удалены
    """
    folderPaths, filePaths = GetListDirAndFiles(directory)
    if filePaths:
        print("Файлы, которые удалены:")
        for path in filePaths:
            if not isOnList(dirIgnore, path):
                print(path)
                #os.remove(path)
    if folderPaths:
        print("Папки, которые удалены:")
        for path in reversed(folderPaths):
            if not isOnList(dirIgnore, path):
                print(path)
                #os.rmdir(path)


def copyFilesAndFolders(list1, directory):
    """
    Копирует все файлы из директории
    """
    key = 'r'
    #for path in list1:
    #    command =  "cp" + '-' + key + directory
    #os.popen()


def prepSync(list1):
    """
    Функция prepSync (preparatory Sync - подготовительная синхронизация)
    1. удоляет все файлы и папок, которые находятся в
    в директориях(указанных в конфиг файле) начиная
    со 2-й строчки списка list1
    2. копирует все содержимое из первой директории списка
    во все папки из списка list1
    """
 #   mainDirectory = list1.pop(0)
    for line in list1:
        deletingFilesAndFolders(line, list1)

    #copyFiles(list1)

def Sync(list1):
    """
    Функция синхронизирует между собой все папки из списка
    """

    pass


def startSync(list1):
    """
    Функция выполняют синхронизацию файлов из списка
    """
    prepSync(list1)
    Sync(list1) # в разработке


def main():
    
    checkingProgPerformance(checkOS())  # Check operating system

    NameOfConfig = "config"
    progWorks, list1 = readConfig(NameOfConfig)  # progWorks = False if program broke

    ### test
    getListDirIgnoreDel(list1)
    ###
    #checkingProgPerformance(progWorks)
    #startSync(list1)




if __name__ == "__main__":
    main()
