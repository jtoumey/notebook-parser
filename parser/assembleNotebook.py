# !/usr/bin/python

import os
import subprocess
import fnmatch

import parser

class Notebook:

    preamble = """\\documentclass{article}
\\usepackage[T1]{fontenc}
\\usepackage{tgpagella}

\\usepackage[margin=1in]{geometry}
\\usepackage{amsmath}
\\usepackage{tabu}

\\usepackage{multicol}
\\usepackage{booktabs}
\\usepackage{graphicx}

\\title{Laboratory Notebook \\\\ Computational Thermal Fluids Lab}
\\author{Julian Toumey\\thanks{julian.toumey@uconn.edu}}
\\date{Maintained: 05 August 2019--Present}

\\begin{document}

\\maketitle

\\tableofcontents

"""
    month_dict = {'01': 'JAN', '02': 'FEB', '03': 'MAR', '04': 'APR', '05': 'MAY', '06': 'JUN', '07': 'JUL', '08': 'AUG', '09': 'SEP', '10': 'OCT', '11': 'NOV', '12': 'DEC'}
    month_header_dict = {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June', '07': 'July', '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'}

    directory_list = list()
    filtered_years = list()
    filtered_months = list()
    filtered_days = list()

    daily_entry_matrix = list()

    def __init__(self, cwd_):
        self.cwd = cwd_

    def convertMarkdownEntries(self):

        for filename in self.filtered_days:
            ext = filename.split('.')[1]

            print ext

            if 'md' in ext: 
                print filename

                filepath = self.cwd + '/' + self.filtered_years[0] + '/' + self.filtered_months[0] + '/' + filename
                print filepath

                parser.parseEntry(filepath)

    def writeMainNotebook(self):

        print('*****************************************************')
        print self.cwd

        main_nb_path = self.cwd + '/mainNb_autoGen.tex'
        print main_nb_path
        main_nb = open(main_nb_path, 'w')

        # main_nb.write('\\documentclass{article} \n \\begin{document} \n')
        main_nb.write(self.preamble)

        for year in self.filtered_years:

            main_nb.write('\\section*{%s}\n\n' % year)

            for month in self.filtered_months:

                month_header = self.month_header_dict[month]

                main_nb.write('\\addcontentsline{toc}{section}{%s}\n' % (month_header))
                main_nb.write('\\subsection*{%s}\n\n' % month_header)

                for day in self.filtered_days:

                    if '.tex' in day:
                        filepath = year + '/' + month + '/' + day
                        month_letter = self.month_dict[month]
                        date_string = day[6:8] +'-' + month_letter

                        # main_nb.write('\\addcontentsline{toc}{section}{%s}\n' % (date_string))
                        main_nb.write('\\subsubsection*{%s}\n\\input{%s}\n' % (date_string, filepath))
                        main_nb.write('\n\\noindent\\rule{\\textwidth}{0.4mm}\n\n')


        main_nb.write('\n\\end{document}\n')
        main_nb.close()


    def generateNotebook(self):

        # for (root, dirs, files) in os.walk('/Users/jtoumey/CodeRepositories/active/labNotebook-uconn', topdown=True):
        for root, subdirs, files in os.walk(self.cwd):
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

        self.filtered_years.sort()
        self.filtered_months.sort()
        self.filtered_days.sort()

        self.convertMarkdownEntries()

        self.writeMainNotebook()

    def compilePdfNotebook(self):
        main_nb_path = self.cwd + '/mainNb_autoGen.tex'

        print(main_nb_path)
        subprocess.call(['pdflatex' + main_nb_path])


def main():
    cwd = os.getcwd()
    #cwd = 'Users/jtoumey/CodeRepositories/active/labNotebook-uconn/'
    mainNotebook = Notebook(cwd)

    mainNotebook.generateNotebook()
    # mainNotebook.compilePdfNotebook()


if __name__ == '__main__':
    main()
