#!/usr/bin/python

import subprocess, sys

# class lineRecord:

#     def __init__(self):


class inputNotebookEntry:

    def __init__(self, source_file_):
        
        self.source_file = source_file_

    def parseNotebookEntry(self):
        print("Parsing input notebook entry...\n")

        inputEntry = open(self.source_file, 'r')
        inputEntryLines = inputEntry.readlines()

        outputEntry = open('output1.tex','w')

        lineNumber = 0

        for lineNumber in range(0, len(inputEntryLines)):

            print('Line number: %i' % lineNumber)
            line = inputEntryLines[lineNumber]
            # Convert the top-level heading to a 'paragraph' LaTeX heading
            # This conversion is specific to these notebook files and not canonical
            if '# ' in line: 
                timeEntryLine = '\paragraph{' + line[2:].rstrip() +'}\n'

                outputEntry.write(timeEntryLine)

            # Detect lines that may be italicized or bullet points 
            elif '*' in line:

                numAsterisks = line.count('*')

                # Maybe the line is an italics line
                if numAsterisks == 2:

                    endPosition = line[1:].find('*')

                    projectEntryLine = '\\textit{' + line[1:(endPosition+1)] + '}\n'
                    outputEntry.write(projectEntryLine)

                # Perhaps we found the start of a bulleted list
                elif numAsterisks == 1:

                    projectEntry = '\\begin{itemize}\n' + '    \item ' + line[2:].rstrip() + '\n'
                    outputEntry.write(projectEntry)

                    # Continue looping over the file, seeing if the list continues
                    for line in inputEntryLines[(lineNumber+1):]:
                        if '* ' in line:
                            projectEntry = '    \item ' + line[2:].rstrip() + '\n'
                            outputEntry.write(projectEntry)

                            lineNumber = lineNumber + 1

                    projectEntry = '\end{itemize}\n\n'
                    outputEntry.write(projectEntry)


            else:
                outputEntry.write(line.rstrip() + '\n')

            lineNumber = lineNumber + 1



        outputEntry.close()

def main():

    source_file = sys.argv[1]


    markdownNotebookEntry = inputNotebookEntry(source_file)
    markdownNotebookEntry.parseNotebookEntry()

    



if __name__ == '__main__':
    main()

