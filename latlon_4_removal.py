#! /usr/bin/env python
#This program will do the following:
#1: read the text from Marrus_claudanielis.txt
#2: parse the data
#3: repackage the data into a new format and written to an output file.

import re #Load regular expression module, used by decimalat()

# Functions must be defned before they are used
def decimalat (DegString):
    #This function requires that the re module is loaded
    #take a string in the format "34 56.78 N" and return decimal degrees
    SearchStr = '(\d+) ([\d\.]+) (\w)'
    Result = re.search(SearchStr, DegString)

    #Get the captured character groups, as defined by the parentheses
    #in the regular expression, convert the numbers to floats, and
    #assign them to the variables with meaningful names
    Degree = float(Result.group(1))
    Minutes = float(Result.group(2))
    Compass = Result.group(3).upper() #Make sure it is capital too

    #calculate the decimal Degrees
    DecimalDegree = Degree + Minutes/60

    #if the compass direction indicates the coordinates is south or
    #West, make the sign of the coordinate negative

    if Compass == 'S' or Compass == 'W':
        DecimalDegree  = -DecimalDegree
    return DecimalDegree
#End of the function decimalat () definition

#Set the input file name
InFileName = 'Marrus_claudanielis.txt'

#Derive the output file name from the input file names
OutFileName = 'dec_' + InFileName

#give the option to write to a file or just print to screen
WriteOutFile = True

#Open the input file
InFile = open(InFileName, 'r')
#to remove Comments in the output file, i removed the \tcomment here
#i also added \t in front og dive to improve formating
HeaderLine = '\tdive\tdepth\tlatitude\tlongitude\tdate'
print (HeaderLine)

#open the output file, if desired. Do this outside the loop
if WriteOutFile:
    #open the output file
    OutFile = open(OutFileName, 'w')
    OutFile.write(HeaderLine + '\n')

#initialize the counter used to keep track of the line numbers
LineNumber = 0

#Loop over each line in the InFile
for Line in InFile:
    #Check the line number, dont consider if it is first Line
    if LineNumber > 0:
        #Remove the line ending characters
        #print (line) #uncomment for debugging
        Line = Line.strip('\n')

        #split the line into a list of ElementList, using tab as a delimiter
        ElementList = Line.split('\t')

        #Returns a list in the format:
        #['tiburon 596', '19-Jul-03', '36 36.12 N', '122 22.48 W', '1190', 'holotype']
        #uncomment for debugging
        #print ("ElementList: ", ElementList)

        Dive = ElementList[0]
        Date = ElementList[1]
        Depth = ElementList[4]
        Comment = ElementList[5]

        LatDegrees = decimalat(ElementList[2])
        lonDegrees = decimalat(ElementList[3])

        #create string to 5 decimal places, padded to 10 total characters
        #(using line continuation character \)
        #to remove Comments, i removed the comment string and the %9s\t here
        OutString = "%s\t%4s\t%10.5f\t%10.5f\t%s" % \
                            (Dive,Depth,LatDegrees,lonDegrees,Date)
        print (OutString)
        if WriteOutFile:
            OutFile.write(OutString + '\n') #remember the line feed!
    #another way to say LineNumber = LineNumber+1...
    LineNumber += 1 # this is outside the if, but inside the for Loop

#close the files
InFile.close()
if WriteOutFile:
    OutFile.close()
