# Local Directory Content Synchronization Service
import os
from functionsForDebugging import printList

from completedFunctions import checkingProgPerformance, checkOS, readConfig, getListDirAndFiles, getInodeAndDevID, \
    isOnList


def getListDirIgnoreDel(listDir):
    """
    Функция возвращает список папок(содержимое которых нельзя удолять) содержимое которых нельзя удолять
    К ним относятся:
    - первая папка из списка listDir
    - все подпапки первой папки(mainFolder) из listDir (но не папки,
      которые являются подпапками папок из списка listDir)
    """
    # нужные директории
    necessaryDirectory = [listDir[0]] # список директорий, которые нельзя удолять

    # printList("config", listDir)

    mainFolder = listDir[0]

    # неподходящие папки
    unsuitableDirectory = listDir[1:]  # список содержит в себе все подпапки папок из конфига за ислючением тех,которые не находятся над 1-й папкой из конфига

    # предки для mainFolder
    ancestorsOfMainFolder = ['/']  # попадают пути, которые находятся выше 1 папки из listDir

    childrenOfMainFolder = mainFolder.split('/')

    tempStr = ""
    for element in childrenOfMainFolder[1:-1]:
        tempStr = tempStr + '/' + element
        ancestorsOfMainFolder.append(tempStr)
    #printList("ancestorsOfMainFolder (неподходящие папки) : ", ancestorsOfMainFolder)

    #print("ищу подпапки в: ")
    for dir in listDir[1:]:
        if not isOnList(ancestorsOfMainFolder, dir):
            # print(dir)
            folderPaths, _ = getListDirAndFiles(dir)
            unsuitableDirectory = unsuitableDirectory + folderPaths
            
    #printList("unsuitableDirectory(неподходящие папки)", unsuitableDirectory)

    childrenOfMainFolder, _ = getListDirAndFiles(mainFolder)
    # print("Нужные папки: ")
    for path in childrenOfMainFolder:
        if not isOnList(unsuitableDirectory, path):
            necessaryDirectory.append(path)
            # print(path)

    return necessaryDirectory


def deletingFilesAndFolders(config):
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
    delitedFilesAndDirectories = []
    dirIgnore = getListDirIgnoreDel(config)
    for directory in config:
        folderPaths, filePaths = getListDirAndFiles(directory)
        if filePaths:
            print("Файлы, которые удалены:")
            for path in filePaths:
                if not isOnList(dirIgnore, os.path.split(path)[0]):
                    delitedFilesAndDirectories.append(path)
                    print(path)
                    # os.remove(path)
        if folderPaths:
            print("Папки, которые удалены:")
            for path in reversed(folderPaths):
                if not (isOnList(dirIgnore, path) and not isOnList(config, path)):
                    delitedFilesAndDirectories.append(path)
                    print(path)
                    # os.rmdir(path)
    return delitedFilesAndDirectories


def copyFilesAndFolders(list1, directory):
    """
    Копирует все файлы из директории
    """
    pass


def prepSync(list1):
    """
    Функция prepSync (preparatory Sync - подготовительная синхронизация)
    1. удоляет все файлы и папок, которые находятся в
    в директориях(указанных в конфиг файле) начиная
    со 2-й строчки списка list1
    2. копирует все содержимое из первой директории списка
    во все папки из списка list1
    """
    deletingFilesAndFolders(list1)

    # copyFiles(list1)


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
    Sync(list1)  # в разработке

def startTesting():
    from tests import runTestsForGetListDirIgnoreDel, runTestsForDeletingFilesAndFolders
    templateTestName = "config"
    templateResultName = "res"
    numbersOfFiles = 5
    pathToResults = "tests/forGetListDirIgnoreDel/"
    runTestsForGetListDirIgnoreDel(templateTestName, templateResultName, pathToResults, numbersOfFiles)

    pathToResults = "tests/forDeletingFilesAndFolders/"
    #runTestsForDeletingFilesAndFolders(templateTestName, templateResultName, pathToResults, numbersOfTests)


def main():
    checkingProgPerformance(checkOS())  # Check operating system
    testing = 1
    if testing:
        startTesting()
    else:
        nameOfConfig = "config1"
        progWorks, list1 = readConfig(nameOfConfig)  # progWorks = False if program broke

        ### test

        ###
        checkingProgPerformance(progWorks)
        startSync(list1)


if __name__ == "__main__":
    main()
