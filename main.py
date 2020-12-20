# Local Directory Content Synchronization Service
import os
from functionsForDebugging import printList

from completedFunctions import checkingProgPerformance, checkOS, readConfig, \
    isOnList, removeDuplicatesFromList, deletingFilesAndFolders


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

    pathToResults = templatePathToTests + "forGetListDirIgnoreForRemovingAndCleaning/"
    #runTestsForGetListDirIgnoreDel(templatePathToTests, templateTestName, templateResultName, pathToResults, numbersOfFiles)

    pathToResults = templatePathToTests + "forDeletingFilesAndFolders/"
    runTestsForDeletingFilesAndFolders(templatePathToTests, templateTestName, templateResultName, pathToResults, numbersOfFiles)
def test():
    pass

def main():
    checkingProgPerformance(checkOS())  # Check operating system
    testing = 0 # 0 - обычная работа программы / 1 запустить тестирование
    if testing:
        startTesting()
    else:
        # templatePathToTests = "testsForProgram/"
        templatePathToTests = ""
        nameOfConfig = templatePathToTests + "config"
        progWorks, list1 = readConfig(nameOfConfig)  # progWorks = False if program broke
        checkingProgPerformance(progWorks)
        startSync(list1)


if __name__ == "__main__":
    main()
