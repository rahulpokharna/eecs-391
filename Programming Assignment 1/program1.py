import sys

board = [[0 for x in range(3)] for y in range(3)] #array for representing the board
maxNodes = 100000 #max nodes allowed during search, stop when limit is reached

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
    printState()


'''
Prints out the board in a 3 by 3 table format, like looking at the puzzle itself
'''
def printState():
    for x in range(3):
        for y in range(3):
            print(board[x][y], end="")
        print() 
    print()

'''
Moves the blank spot in the inputted direction and says invalid if move is not valid
'''
def move(dir):
    return {
        'up': #do stuff in whitespace
        'down':
        'left':
        'right':
    }
    print("That is not a valid move. Please submit either up, down, left, or right.")
    printState()

while True:
    inp = input('Here is a list of functions. Type what function you would like to run!\nsetState\trandomizeState\n')
    if(inp == 'setState'):
        setState(input("Input Board State: \n>>"))

    if(inp == 'printState'):
        printState()
