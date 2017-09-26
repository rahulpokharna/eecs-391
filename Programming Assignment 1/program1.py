import sys

board = [[0 for x in range(3)] for y in range(3)]

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

while True:
    inp = input('Here is a list of functions. Type what function you would like to run!\nsetState\trandomizeState\n')
    if(inp == 'setState'):
        setState(input("Input Board State: \n>>"))

    if(inp == 'printState'):
        printState()
