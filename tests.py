from completedFunctions import readConfig, getListFromFile
from functionsForDebugging import printList


def comparisonOfResults(namePfTest, obj1, obj2):
    #printList("obj1", obj1)
    #printList("obj2", obj2)
    if obj1 == obj2:
        print(namePfTest, " success")
        # print()
    else:
        print(namePfTest, " failed")
        # print()


def runTestsForGetListDirIgnoreDel(templateTestName, templateResultName, pathToResults, numbersOfTests):
    from main import getListDirIgnoreDel
    for i in range(numbersOfTests):
        testName = templateTestName + str(i + 1)
        progWorks, list1 = readConfig("tests/" + testName)  # progWorks = False if program broke
        myListOfAnswers = getListDirIgnoreDel(list1)

        listOfAnswers = getListFromFile(pathToResults + templateResultName + str(i + 1))

        comparisonOfResults(testName, sorted(myListOfAnswers), sorted(listOfAnswers))


def runTestsForDeletingFilesAndFolders(templateTestName, templateResultName, pathToResults, numbersOfTests):
    from main import deletingFilesAndFolders
    for i in range(numbersOfTests):
        testName = templateTestName + str(i + 1)
        progWorks, list1 = readConfig("tests/" + testName)  # progWorks = False if program broke
        myListOfAnswers = deletingFilesAndFolders(list1)

        listOfAnswers = getListFromFile(pathToResults + templateResultName + str(i + 1))

        comparisonOfResults(testName, sorted(myListOfAnswers), sorted(listOfAnswers))


def runTestsForProgram(configList):
    pass


def runTests(configList):
    pass
    # for config in configList:
    #    progWorks, list1 = readConfig(config)  # progWorks = False if program broke
