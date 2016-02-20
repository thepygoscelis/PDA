# Author    : Charlie R. Hicks
# Program   : Push Down Automaton

import os
#Function Name : contains
#Purpose       : Helper Function to check if a list contains a key. Doesn't throw an error like index.
#Parameters    :
# value - key to search for
# set   - list to search
#Return Values
# True  - found the value
# False - failed to find value
def contains(value,set):
    for item in set:
        if(value == item):
            return True
    return False
#Function Name : findTransition
#Purpose       : Determines if a transition can be accomplished from the current state within the PDA.
#Parameters    :
# letter   - used to determine the transition to look at within the current state
# state    - current state of the PDA
# stack1   - one of the two stacks of PDA (needed to see if you can pop the items from the stack)
# stack2   - one of the two stacks of PDA (needed to see if you can pop the items from the stack)
# alphabet - used in conjunction with letter to determine transition to examine.
#Return Values
# Valid transition index or -1 for no transition
def findTransition(letter,state,stack1,stack2,alphabet):
    #No Use in trying if the letter isn't in the alphabet
    if contains(letter,alphabet):
        #Transitions are lined up based on the order of the given alphabet
        index = alphabet.index(letter)
        #Pull the transition from the current state
        transition =  state[index]
        #This can handle multiple items to be popped.
        popFrom1 = transition[1]
        popFrom2 = transition[3]
        #The two loops below both check to see if anything needs to be popped from the stacks and if it is valid.
        for letter in popFrom1:
            if(letter != '!'):
                if(stack1 == []):
                    return -1 
                else:
                    #Top of stack needs to match letter to be valid to pop.
                    if(stack1[-1] == letter):
                        stack1.pop()
                    else:
                        return -1
        for letter in popFrom2:
            if(letter != '!'):
                if(stack2 == []):
                    return -1
                else:            
                    #Top of stack need to match letter to be valid to pop.
                    if(stack2[-1] == letter):
                        stack2.pop()
                    else:
                        return -1
        return index
    else:
        return -1
#Function Name : parseString
#Purpose       : This is used to tell wether a string is accepted or not.
#Parameters    :
# alphabet     - list of single characters
# finalStates  - a list of integers that represent the idencies of final states
# states       - a three dimensional array which holds states that in turn hold the transitions
# parseString  - string to be tested against the PDA
# fastRun      - Won't show state of PDA after each transition [Default=True]
# Return values
# 1  - parseString is valid by the PDA.
# -1 - parseString is invalid by the PDA.
def parseString(alphabet,finalStates,states,parseString,fastRun=True):
    currentState = 0
    stack1 = []
    stack2 = []
    for letter in parseString:
        if not fastRun:
            print("Current State: " + repr(currentState) + "\nStack #1: " + repr(stack1) + "\nStack #2: " + repr(stack2))
            input("Press Enter to Continue")
        transition = findTransition(letter,states[currentState],stack1,stack2,alphabet)
        if(transition == -1):
            print("Failed to find transition")
            return -1
        else:
            #Multiple Character Input
            for symbol in states[currentState][transition][2][::-1]:
                if(symbol != '!'):
                    stack1.append(symbol)
            for symbol in states[currentState][transition][4][::-1]:
                
                if(symbol != '!'):
                    stack2.append(symbol)
            currentState = states[currentState][transition][0]
    if not fastRun:
         print("Current State: " + repr(currentState) + "\nStack #1: " + repr(stack1) + "\nStack #2: " + repr(stack2))
    if(stack1 == [] and stack2 == [] and contains(currentState,finalStates)):
        return 1
    else: 
        return -1
#START OF MAIN PROGRAM
userAnswer = "y"
while (userAnswer != "n" and userAnswer != "N"):
    #The next 4 are used as parts of the PDA
    # alphabet       - a set of single characters
    # numberOfStates - total number of states in the PDA
    # finalStates    - set of int values indicating the indexes of finals states within the states set
    # states         - set of states which contain transitions which contain information on what to do based on each character.
    alphabet = []
    numberOfStates = 0
    finalStates = []
    states = []
    #The next 3 are used for user input:
    #toBeParsed  - user provided string to test against the PDA
    #typeOfRun   - user provide string indicating a fast or step-by-step run
    #keepParsing - user provided string indicating wether to run another string against the PDA
    toBeParsed = ""
    typeOfRun = ""
    keepParsing = ""
    #Used for the success of a parse
    result = 0
    fileName = input("Enter the file you wish to read: ")
    #Make sure the file exists to avoid File I/O errors.
    while not os.path.exists(fileName):
        fileName = input("Enter a file that exists: ")
    dataFile = open(fileName,'r')
    #Get the alphabet
    alphabet = dataFile.readline().split(" ")
    #Remove the newline/whitespace
    alphabet[len(alphabet)-1] = alphabet[len(alphabet)-1].strip()
    #Get the number of States
    numberOfStates = int(dataFile.readline().strip())
    #Read the final state numbers
    finalStates = dataFile.readline().split(" ")
    for i in range(len(finalStates)):
        finalStates[i] = int(finalStates[i])

    #Read the States
    #Here I read the lines 1 at a time and strip the whitespace that Python wants to read.
    #I also have this set up to read an arbitrary number of transitions.
    #I know that the number of letters is fixed, this however is more flexible.
    #You also note that I transform the first element of every transition to an int since it represents the next state.
    for i in range(numberOfStates):
        states.append(dataFile.readline().split(" "))
        for j in range(len(states[i])):
            states[i][j] = states[i][j].strip()
            states[i][j] = states[i][j].split(',')
            #Transform the next state element of the transitions to an int
            states[i][j][0] = int(states[i][j][0])
    while (keepParsing != "n" and keepParsing != "N"):
        #Get parse string
        toBeParsed = input("Enter string to Be Parsed: ")
        #Ask User for Step by Step or Fast Run
        typeOfRun = input("Choose type of run\n1 -> Fast Run\n 2 -> Step-by-Step\n: ")
        while typeOfRun != "1" and typeOfRun != "2":
            typeOfRun = input("You must choose either 1 (Fast Run) or 2(Step-by-Step): ")
        #Fast Run
        if (typeOfRun == "1"):
            result = parseString(alphabet,finalStates,states,toBeParsed)
        #Step By Step Run
        elif (typeOfRun == "2"):
            result = parseString(alphabet,finalStates,states,toBeParsed,False)
        if(result == 1):
            print("Successsfully parsed " + repr(toBeParsed) + "!")
        else:
            print("Failed to accept string " + repr(toBeParsed) + "!")
        #Parse another string with the same PDA
        keepParsing = input("Would you like to parse another string? [Y/n] ")
    #Read another PDA
    userAnswer = input("Do you wish to continue? (Y/n) :")
print("Program Terminated.")
