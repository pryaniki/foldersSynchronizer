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


def removeDuplicatesFromList(l):
    n = []
    for i in l:
        if i not in n:
            n.append(i)
    return n


def checkToSubstring(config):  # проверка подстроки
    """ проверяет садержатся ли пути из списка config в path

    subfolders # подпапки первой папки из конфига
    """
    mainFolder = config[0]
    subfolders, _ = getListDirAndFiles(mainFolder)  # подпапки 0-й папки из конфиг
    subfolders = sorted(subfolders)
    #printList("все подпапки 0 папки из конфига", subfolders)

    ### разделит папки на 1 лагеря
    # подпапки config[0:]
    unnecessaryPaths = config.copy()[1:]
    for folder in subfolders:
        t = os.path.split(folder)[0]  # путь к папке над folder
        #print("folder ", folder)
        if isOnList(unnecessaryPaths, t):
            #print("folder ", folder, "append unnec")
            unnecessaryPaths.append(folder)


    #printList("unnecessaryPaths", unnecessaryPaths)
    ####
    # подпапки 0 config но не пренадлежащие 1 пункту
    result = config.copy()[1:]
    for folder in subfolders:
        t = os.path.split(folder)[0]  # путь к папке над folder
        #print("folder ", folder)
        if not isOnList(unnecessaryPaths, t):
            #print("folder ", folder, "append result")
            result.append(folder)
    #printList("result", sorted(removeDuplicatesFromList(result)))
    return sorted(removeDuplicatesFromList(result))


def getListDirIgnoreForRemovingAndCleaning(config):
    """
    Функция возвращает:
    1)список папок которые нельзя удолять;
    2)список папок, в которых нельзя удолять файлы
    1 пункт
    К ним относятся:
    -1 первая папка из списка config
    -2 папки, содержащиеся в пути папок из config
    -3 все подпапки первой папки(mainFolder) из config (но не папки,
      которые являются подпапками папок из списка config)
    2 пункт
    К ним относятся:
    -4 получитс список папок, файлы в которых нельзя удолять
    """
    ### -1
    dirIgnoreForRemoving = [config[0]]  # список директорий, которые нельзя удолять

    ### -3
    dirIgnoreForRemoving += checkToSubstring(config)
    # printList("3 dirIgnoreForRemoving", removeDuplicatesFromList(dirIgnoreForRemoving))

    ### -4
    tempList = []
    for path in dirIgnoreForRemoving:
        for element in config[1:]:
            if element == path:
                tempList.append(element)
                break

    dirIgnoreForCleaning = []
    for path in dirIgnoreForRemoving:
        if not isOnList(tempList, path):
            dirIgnoreForCleaning.append(path)
    # printList("4 dirIgnoreForCleaning", removeDuplicatesFromList(dirIgnoreForCleaning))
    ### -2
    prefix = os.path.commonprefix(config)  # общий префикс путей
    lenPrefix = len(prefix.split('/')) - 2
    ancestorsOfFolder = []
    for folder in config:
        # предки для Folder
        folder = folder.split('/')
        folder.pop(0)

        tempStr = os.path.split(prefix)[0]
        for element in folder[lenPrefix:]:
            tempStr += "/" + element
            #printList("добавляю в список", tempStr)
            ancestorsOfFolder.append(tempStr)

    #printList("ancestorsOfFolder", removeDuplicatesFromList(ancestorsOfFolder))
    dirIgnoreForRemoving += ancestorsOfFolder
    #printList("2 dirIgnoreForRemoving", removeDuplicatesFromList(dirIgnoreForRemoving))

    return removeDuplicatesFromList(dirIgnoreForRemoving), removeDuplicatesFromList(dirIgnoreForCleaning)


def deletingFilesAndFolders(config):
    from functionsForDebugging import printList
    from completedFunctions import getListDirIgnoreForRemovingAndCleaning
    """
    Функция удоляет все файлы и папки в указанной директории
    за исключением тех, которые находятся в dirIgnore
    1.Директория пустая
    2.В ней есть папки
    3.В ней есть файлы и ссылки(мягкие и жесткии)
    4.В ней есть и папки и файлы и ссылки
    dirIgnore список и config директорий, которые не будут удалены
    :return: возвращает список удаленных папок и файлов
    """
    delitedDirectories = []
    delitedFiles = []

    # список папок, которые нельзя удолять,| список папок, ФАЙЛЫ В которых нельзя удолять
    dirIgnoreForRemoving, dirIgnoreForCleaning = getListDirIgnoreForRemovingAndCleaning(config)
    #printList("dirIgnoreForRemoving", dirIgnoreForRemoving)
    #printList("dirIgnoreForCleaning ", dirIgnoreForCleaning)
    for directory in config:
        folderPaths, filePaths = getListDirAndFiles(directory)
       # printList("folders",folderPaths)
    # printList("files", filePaths)
        if filePaths:
            #print("Файлы, которые удалены:")
            for path in filePaths:
                if not isOnList(dirIgnoreForCleaning, os.path.split(path)[0]):
                    delitedFiles.append(path)
                    #print(path)
                    # os.remove(path)
        if folderPaths:
            #print("Папки, которые удалены:")
            for path in reversed(folderPaths):
                if not (isOnList(dirIgnoreForRemoving, path) or isOnList(config, path)):
                    delitedDirectories.append(path)
                    #print(path)
                    # os.rmdir(path)
    printList("удаленные директории", delitedDirectories)
    printList("удаленные файлы", delitedFiles)
    return removeDuplicatesFromList(delitedFiles) + removeDuplicatesFromList(delitedDirectories)


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
