from completedFunctions import readConfig, getListFromFile, getListDirIgnoreForRemovingAndCleaning
from functionsForDebugging import printList
from main import deletingFilesAndFolders


def comparisonOfResults(namePfTest, obj1, obj2):
    if obj1 == obj2:
        print(namePfTest, " success")
        # print()
    else:
        printList("myAnswer", obj1)
        printList("rightAnswer", obj2)
        print(namePfTest, " failed")
        # print()

def runTestsForGetListDirIgnoreDel(pathToTests, templateTestName, templateResultName, pathToResults, numbersOfTests):
    print("###############")
    print("TestsForgetListDirIgnoreForRemovingAndCleaning")
    print("###############")
    for i in range(numbersOfTests):
        testName = templateTestName + str(i + 1)
        progWorks, list1 = readConfig(pathToTests + testName)  # progWorks = False if program broke
        myListOfAnswers, _ = getListDirIgnoreForRemovingAndCleaning(list1)
        listOfAnswers = getListFromFile(pathToResults + "folders/" + templateResultName + str(i + 1))
        comparisonOfResults(testName, sorted(myListOfAnswers), sorted(listOfAnswers))

    print("###############")
    print("TestsForGetListDirIgnoreForCleaning")
    print("###############")
    for i in range(numbersOfTests):
        testName = templateTestName + str(i + 1)
        progWorks, list1 = readConfig(pathToTests + testName)  # progWorks = False if program broke
        _, myListOfAnswers = getListDirIgnoreForRemovingAndCleaning(list1)
        listOfAnswers = getListFromFile(pathToResults + "files/" + templateResultName + str(i + 1))
        comparisonOfResults(testName, sorted(myListOfAnswers), sorted(listOfAnswers))


def runTestsForDeletingFilesAndFolders(pathToTests, templateTestName, templateResultName, pathToResults, numbersOfTests):
    print("###############")
    print("TestsForDeletingFilesAndFolders")
    print("###############")
    for i in range(numbersOfTests):
        testName = templateTestName + str(i + 1)
        progWorks, list1 = readConfig(pathToTests + testName)  # progWorks = False if program broke
        myListOfAnswers = deletingFilesAndFolders(list1)
        listOfAnswers = getListFromFile(pathToResults + templateResultName + str(i + 1))

        comparisonOfResults(testName, sorted(myListOfAnswers), sorted(listOfAnswers))


def runTestsForProgram(configList):
    pass


def runTests(configList):
    pass
    # for config in configList:
    #    progWorks, list1 = readConfig(config)  # progWorks = False if program broke
