# Local Directory Content Synchronization Service
import os
from functionsForDebugging import printList

from completedFunctions import checkingProgPerformance, checkOS, readConfig, getListDirAndFiles, \
    isOnList, removeDuplicatesFromList


def getListDirIgnoreForCleaning():
    """ dirIgnoreForCleaning список папок, содержимое которых нельзя удолять """
    dirIgnoreForRemoving = []
    return dirIgnoreForRemoving


def deletingFilesAndFolders(config):
    from functionsForDebugging import printList
    from completedFunctions import getListDirIgnoreForRemoving
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
    dirIgnoreForRemoving = getListDirIgnoreForRemoving(config) # список папок, которые нельзя удолять
    #printList("dirIgnoreForRemoving", dirIgnoreForRemoving)
    dirIgnoreForCleaning = []  # список папок, ФАЙЛЫ В которых нельзя удолять
    # printList("dirIgnore",dirIgnore)
    for directory in config:
        folderPaths, filePaths = getListDirAndFiles(directory)
       # printList("folders",folderPaths)
    # printList("files", filePaths)
        if filePaths:
            #print("Файлы, которые удалены:")
            for path in filePaths:
                if not isOnList(dirIgnoreForRemoving, os.path.split(path)[0]):
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
    return removeDuplicatesFromList(delitedFiles), removeDuplicatesFromList(delitedDirectories)


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
    templatePathToTests = "testsForProgram/"
    numbersOfFiles = 6
    pathToResults = templatePathToTests + "forGetListDirIgnoreForRemoving/"
    runTestsForGetListDirIgnoreDel(templatePathToTests, templateTestName, templateResultName, pathToResults, numbersOfFiles)

    pathToResults = templatePathToTests + "forDeletingFilesAndFolders/"
    #runTestsForDeletingFilesAndFolders(templatePathToTests, templateTestName, templateResultName, pathToResults, numbersOfFiles)
def test():
    #txt = "Сумма: {'225'} руб"
    #print(txt.translate(txt.maketrans("{'}", "   ")))
    print(os.getcwd())
    pass

def main():
    checkingProgPerformance(checkOS())  # Check operating system
    testing = 1
    if testing:
        startTesting()
    else:
        templatePathToTests = "testsForProgram/"
        nameOfConfig = templatePathToTests + "config1"
        progWorks, list1 = readConfig(nameOfConfig)  # progWorks = False if program broke

        ### test

        ###
        checkingProgPerformance(progWorks)
        startSync(list1)


if __name__ == "__main__":
    main()
