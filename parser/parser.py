#!/usr/bin/python

import subprocess, sys

class inputNotebookEntry:

    def __init__(self, source_file_):
        
        self.source_file = source_file_

    def parseNotebookEntry(self):
        print("Parsing input notebook entry...\n")

        inputEntry = open(self.source_file, 'r')
        outputEntry = open('output1.tex','w')

        # Convert the top-level heading to a 'paragraph' LaTeX heading
        # This conversion is specific to these notebook files and not canonical
        for line in inputEntry:
            if '# ' in line: 
                print line[2:]
                timeEntryLine = '\paragraph{' + line[2:].rstrip() +'}\n'

                outputEntry.write(timeEntryLine)

            # Detect italicized notes 
            elif '*' in line:
                print line
                endPosition = line[1:].find('*')

                projectEntryLine = '\\textit{' + line[1:(endPosition+1)] + '}\n'

                outputEntry.write(projectEntryLine)


            else:
                outputEntry.write(line.rstrip())



        outputEntry.close()

def main():

    source_file = sys.argv[1]


    markdownNotebookEntry = inputNotebookEntry(source_file)
    markdownNotebookEntry.parseNotebookEntry()

    



if __name__ == '__main__':
    main()

