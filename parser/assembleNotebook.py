# !/usr/bin/python

import os
import fnmatch

class Notebook:

    directory_list = list()
    filtered_years = list()
    filtered_months = list()
    filtered_days = list()

    def __init__(self, cwd_):
        self.cwd = cwd_

    def generateNotebook(self):

        # for (root, dirs, files) in os.walk('/Users/jtoumey/CodeRepositories/active/labNotebook-uconn', topdown=True):
        for root, subdirs, files in os.walk('/Users/jtoumey/CodeRepositories/active/labNotebook-uconn'):
            for sub_directory in subdirs:
                if '.git' in sub_directory or '.git' in root:
                    # TODO: This condition forces out the .git folder. Note that it only considers the current directory and the
                    # directory one level above. If such a condition is no longer met, this may fail. 
                    continue

                elif '20' in sub_directory:
                    # Here, we find a year folder (assuming I will not be maintaining this into the 2100s :O) and save 
                    # to our list
                    self.filtered_years.append(sub_directory)

                # TODO: I don't think that two asterisks is the correct way for this wildcard. Look at the documentation to find out
                # how to find a two-character wildcard
                elif fnmatch.filter(sub_directory, '**'):

                    # Find month folders based on a two-character wildcard. This fails when the walk() command reaches into
                    # the .git folder, where there are many two-character folders
                    self.filtered_months.append(sub_directory)

            for daily_file in files:
                (base, ext) = os.path.splitext(daily_file)

                # Not solid, but we can assume the filename includes the month, which we may obtain from the root folder
                expected_filename = sub_directory

                if ext in ('.tex', '.md') and expected_filename in daily_file:
                    # DEBUG full_name = os.path.join(root, daily_file) 

                    self.filtered_days.append(daily_file)

        # DEBUG
        print(self.filtered_years)
        print(self.filtered_months)
        print(self.filtered_days)


def main():
    #cwd = os.getcwd()
    cwd = 'Users/jtoumey/CodeRepositories/active/labNotebook-uconn/'
    mainNotebook = Notebook(cwd)

    mainNotebook.generateNotebook()
    #mainNotebook.writeNotebook()


if __name__ == '__main__':
    main()
