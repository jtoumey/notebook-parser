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

    yearly_record = {}
    monthly_record = {}

    daily_entry_matrix = list()

    def __init__(self, cwd_):
        self.cwd = cwd_

    def convertMarkdownEntries(self):

        for year in self.yearly_record:
            print year

            for month in self.yearly_record[year]:
                print '+++++++++++++'
                for day in self.yearly_record[year][month]:
                            
                    filepath = self.cwd + '/' + year + '/' + month + '/' + day
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

        for year in self.yearly_record:

            main_nb.write('\\section*{%s}\n\n' % year)

            for month in self.yearly_record[year]:

                month_header = self.month_header_dict[month]

                main_nb.write('\\addcontentsline{toc}{section}{%s}\n' % (month_header))
                main_nb.write('\\subsection*{%s}\n\n' % month_header)

                for day in self.yearly_record[year][month]:

                    # The day list only contains markdown files, but assuming that they've all been converted to TeX, swap the file extensions
                    (base, ext) = os.path.splitext(day)
                    day = base + '.tex'

                    # if '.tex' in day:
                    filepath = year + '/' + month + '/' + day
                    month_letter = self.month_dict[month]
                    date_string = day[6:8] +'-' + month_letter

                    # main_nb.write('\\addcontentsline{toc}{section}{%s}\n' % (date_string))
                    main_nb.write('\\subsubsection*{%s}\n\\input{%s}\n' % (date_string, filepath))
                    main_nb.write('\n\\noindent\\rule{\\textwidth}{0.4mm}\n\n')


        main_nb.write('\n\\end{document}\n')
        main_nb.close()


    def generateNotebook(self):

        # Dictionaries which contain a list of our notebook entries

        # Assume the CWD is our notebook directory. The subdirs (excluding .git/) are year folders
        years = next(os.walk(self.cwd))[1]
        years.remove('.git') 

        for year in years:
            months = next(os.walk(self.cwd + '/' + year))[1]

            for month in months:
                days = next(os.walk(self.cwd + '/' + year + '/' + month))[2]

                filtered_days = []

                for day in days:
                    (base, ext) = os.path.splitext(day)
                    if ext in ('.md'):

                        filtered_days.append(day)

                filtered_days.sort()

                self.monthly_record[month] = filtered_days

            self.yearly_record[year] = self.monthly_record

        print self.yearly_record


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
