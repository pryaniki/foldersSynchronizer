import os
import sys

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


def chekingAccessToDirectory(fName):
    """
    The function checks has current user
    rights to read / write the directory
    
    If the directory does not exist,
    then the function will create it

    :return: True if there is access and False if not
    """

    if not os.access(fName, os.F_OK):
        print("directory ", fName, " does not exist")
        if not os.path.isdir(fName):
            try:
                os.mkdir(fName)
            except PermissionError:
                # PermissionError
                return False
   # else:
   #     print("directory ", fName, " exists")
    return os.access(fName, os.R_OK) and os.access(fName, os.W_OK)


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
        if (not chekingAccessToDirectory(list1[i])):
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

def deletingFiles(directory):
    """
    Функция удоляет все файлы в указанной директории
    1.Директория пустая
    2.В ней есть папки
    3.В ней есть файлы
    4.В ней есть и папки и файлы
    """
    folderPaths, filePaths = GetListDirAndFiles(directory)
    if filePaths:
        for path in filePaths:
            os.remove(path)
    if folderPaths:
        for path in reversed(folderPaths):
            print(path)
            os.rmdir(path)


def copyFiles(list1, directory):
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
    mainDirectory = list1.pop(0)
    for line in list1:
        deletingFiles(line)

    copyFiles(list1)

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
    Sync(list1)
   


def main():
    
    checkingProgPerformance(checkOS())  # Check operating system

    NameOfConfig = "config"
    progWorks, list1 = readConfig(NameOfConfig)  # progWorks = False if program broke

    checkingProgPerformance(progWorks)
    startSync(list1)

if __name__ == "__main__":
    main()
