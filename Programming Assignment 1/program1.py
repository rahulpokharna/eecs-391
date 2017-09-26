import random

board = [[0 for x in range(3)] for y in range(3)] #array for representing the board
mnodes = 100000 #max nodes allowed during search, stop when limit is reached

'''
Sets the current state to be whatever is input. Assumes proper format. 
'''
def setState(state):
    i = 0
    j = 0
    for c in state:
        if(c == ' '):
            i += 1
            j = 0
        else:
            board[i][j] = c
            j += 1


'''
Prints out the board in a 3 by 3 table format, like looking at the puzzle itself
'''
def printState():
    print('Current Board State:')
    for x in range(3):
        for y in range(3):
            print(board[x][y], end="")
        print() 
    print()

'''
Moves the blank spot in the inputted direction and says invalid if move is not valid. Remove prints in method
'''
def move(dire):
    print(dire)
    i = -1
    j = -1
    #This finds the index of the current blank space
    for x in range(3):
        for y in range(3):
            if(board[x][y] == 'b'):
                i = x
                j = y
    if(dire == 'up'): 
        i = i - 1
        if(i >= 0):
            temp = board[i][j]
            board[i][j] = 'b'
            board[i + 1][j] = temp
            printState()
            return True
        else:
            print("That is not a valid move. Please Check the board again.")
            printState()
            return False

    elif(dire == 'down'): 
        i = i + 1
        if(i <= 2):
            temp = board[i][j]
            board[i][j] = 'b'
            board[i - 1][j] = temp
            printState()
            return True
        else:
            print("That is not a valid move. Please Check the board again.")
            printState()
            return False

    elif(dire == 'left'): 
        j = j - 1
        if(j >= 0):
            temp = board[i][j]
            board[i][j] = 'b'
            board[i][j+1] = temp
            printState()
            return True
        else:
            print("That is not a valid move. Please Check the board again.")
            printState()
            return False

    elif(dire == 'right'): 
        j = j + 1
        if(j <= 2):
            temp = board[i][j]
            board[i][j] = 'b'
            board[i][j - 1] = temp
            printState()
            return True
        else:
            print("That is not a valid move. Please Check the board again.")
            printState()
            return False
    else:
        print("That is not a valid move. Please submit either up, down, left, or right.")
        return False
    
def randomizeState(n):
    setState('b12 345 678')
    for x in range(n):
        #randomly choose 1 to 4, each being a direction
        valid = False
        while(valid == False):
            d = random.randint(1,4)
            if(d == 1):
                valid = move('up')
            elif(d == 2):
                valid = move('down')
            elif(d == 3):
                valid = move('left')
            elif(d == 4):
                valid = move('right')

def maxNodes(n):
    mnodes = n

def solveAstar(heuristic):
    if (heuristic == 'h1'):
        x = 0
    else:
        x = 1

#Replacement for main method since I forget how to make one in python
while True:
    inp = input('Here is a list of functions. Type what function you would like to run!\nsetState\tprintState\trandomizeState\tmove\tmaxNodes\n->')
    print()
    if(inp == 'setState'):
        setState(input("Input Board State: \n>>"))

    if(inp == 'printState'):
        printState()
    
    if(inp == 'move'):
        move(input('What direction do you want to move? (up, down, left, right): '))
    
    if(inp == 'randomizeState'):
        randomizeState(int(input('How many steps should we randomize?: ')))
    
    if(inp = 'maxNodes'):
        max(int(input('What is the maximum number of nodes allowed to be used during search: ')))