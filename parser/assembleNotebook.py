# !/usr/bin/python

import os
import fnmatch

class Notebook:

    directoryList = list()
    filteredYears = list()

    def __init__(self, cwd_):
        self.cwd = cwd_

    def generateNotebook(self):
        for (root, dirs, files) in os.walk('/Users/jtoumey/CodeRepositories/active/labNotebook-uconn', topdown=True):

            self.filteredYears.append(fnmatch.filter(dirs, '20**'))
            # loop over items in the filtered list, building a year entry for each 
            filteredMonths = fnmatch.filter(dirs, '**')

            filteredDays = fnmatch.filter(files, '20******.md')
            # for name in dirs:
            #     self.directoryList.append(os.path.join(root, name))

        #print self.directoryList
        print self.filteredYears
        print filteredMonths
        print filteredDays

def main():
    #cwd = os.getcwd()
    cwd = 'Users/jtoumey/CodeRepositories/'
    mainNotebook = Notebook(cwd)


    mainNotebook.generateNotebook()
    #mainNotebook.writeNotebook()


if __name__ == '__main__':
    main()
