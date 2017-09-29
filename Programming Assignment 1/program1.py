import random
import math
import fileinput

goalState = 'b12 345 678' #used to check final state
goalBoard = [['b', '1', '2'], ['3', '4', '5'], ['6', '7', '8']] #used to check final board


class Puzzle:

    #onstructor
    def __init__(self):
        self.board = [[0 for x in range(3)] for y in range(3)] #array for representing the board
        self.mnodes = 1000 #max nodes allowed during search, stop when limit is reached
        self.parent = None
        self.parentMove = 'Completed'
        self.depth = 0

    #redefine equivalence function to compare boards between two puzzles
    def __eq__(self, other):
        if(other.__class__ != self.__class__):
            return False
        return self.board == other.board

    #Sets the current state to be whatever is input. Assumes proper format. 
    def setState(self, state):
        self.board = self.convertState(state)

    #Converts an input string into an output array to compare to a final board state
    def convertState(self, state):
        i = 0
        j = 0
        tempState = [[0 for x in range(3)] for y in range(3)] #array for representing the board
        for c in state:
            if(c == ' '):
                i += 1
                j = 0
            else:
                tempState[i][j] = c
                j += 1
        return tempState

    #made to convert board to state string
    def convertBoard(self):
        c = ''
        for x in range(3):
            for y in range(3):
                c = c + str(self.board[x][y])
            c = c + ' '
        return c

    #Prints out the board in a 3 by 3 table format, like looking at the puzzle itself
    def printState(self):
        print('Current Board State:')
        for x in range(3):
            for y in range(3):
                print(self.board[x][y], end="")
            print() 
        print()

    #Moves the blank spot in the inputted direction and says invalid if move is not valid. Remove prints in method
    def move(self, dire):
        i = -1
        j = -1
        #This finds the index of the current blank space
        for x in range(3):
            for y in range(3):
                if(self.board[x][y] == 'b'):
                    i = x
                    j = y
        if(dire == 'up'): 
            i = i - 1
            if(i >= 0):
                temp = self.board[i][j]
                self.board[i][j] = 'b'
                self.board[i + 1][j] = temp
                self.parentMove = 'up'
                #printState()
                return True
            else:
                #print("That is not a valid move. Please Check the board again.")
                #printState()
                return False

        elif(dire == 'down'): 
            i = i + 1
            if(i <= 2):
                temp = self.board[i][j]
                self.board[i][j] = 'b'
                self.board[i - 1][j] = temp
                self.parentMove = 'down'
                #printState()
                return True
            else:
                #print("That is not a valid move. Please Check the board again.")
                #printState()
                return False

        elif(dire == 'left'): 
            j = j - 1
            if(j >= 0):
                temp = self.board[i][j]
                self.board[i][j] = 'b'
                self.board[i][j+1] = temp
                self.parentMove = 'left'
                #printState()
                return True
            else:
                #print("That is not a valid move. Please Check the board again.")
                #printState()
                return False

        elif(dire == 'right'): 
            j = j + 1
            if(j <= 2):
                temp = self.board[i][j]
                self.board[i][j] = 'b'
                self.board[i][j - 1] = temp
                self.parentMove = 'right'
                #printState()
                return True
            else:
                #print("That is not a valid move. Please Check the board again.")
                #printState()
                return False
        else:
            #print("That is not a valid move. Please submit either up, down, left, or right.")
            return False
        
    #randomizes the state after setting it equal to the goal state
    def randomizeState(self, n):
        self.setState(goalState)
        for x in range(n):
            #randomly choose 1 to 4, each being a direction
            d = random.choice(self.validMoves())
            self.move(d)
        print('After randomizing, the ', end='')
        self.printState()

    #Returns a list of all valid directions to move in the current state
    def validMoves(self):
        moves = []
        x, y = self.findBlank()
        if(x >= 1):
            moves.append('up')
        if(x <= 1):
            moves.append('down')
        if(y >= 1):
            moves.append('left')
        if(y <= 1):
            moves.append('right')
        return moves

    #Prints out the final solution using the parentMove and the parent states
    def printSolution(self):
        if(self.parent == None):
            return 'You have solved it! Take the steps from 1 onwards to solve.'
        else:
            print(self.depth, end = ': ')
            print(self.parentMove)
            return self.parent.printSolution()
        
    #find the current position of the blank
    def findBlank(self):
        for x in range(3):
            for y in range(3):
                if(self.board[x][y] == 'b'):
                    return x, y
                
    #declare the number of maximum nodes to use 
    def maxNodes(self, n):
        self.mnodes = n

    #Solve A* Search with an input string representing either h1 or h2
    def solveAstar(self, heuristic):
        numNodes = 1
        openList = [self]
        closedList = []

        #as long as there is an open state
        while(len(openList) > 0):
            x = openList.pop(0)

            if(numNodes > self.mnodes):
                return 'The search has exceeded the maximum alloted nodes. Terminating search.'

            if(x.isSolved()):
                if(len(closedList) == 0):
                    return 'The current board is already solved'
                else:
                    print('Number of nodes used: ' + str(numNodes))
                    return x.printSolution()
                    
            #checks every possible child for the current state that is being expanded
            nextChildren = x.makeNextChildren()
            inOpen = inClosed = False
            for child in nextChildren:
                numNodes += 1
                inOpen = child in openList
                inClosed = child in closedList
                heur = child.getHeuristic(heuristic)
                f = heur + child.depth

                #if the state is newly found
                if(not inOpen and not inClosed):
                    openList.append(child)
                
                #if the state exists in either the open or closed branch
                elif(inOpen):
                    #gets the other instance of the board from the open list and compares
                    oldPosition = openList[openList.index(child)]
                    if(f < oldPosition.depth + oldPosition.getHeuristic(heuristic)):
                        oldPosition.depth = child.depth
                        oldPosition.parent = child.parent
                        oldPosition.parentMove = child.parentMove
                elif(inClosed):
                    #gets the other instance of the board from the open list and compares
                    oldPosition = closedList[closedList.index(child)]
                    if(f < oldPosition.depth + oldPosition.getHeuristic(heuristic)):
                        openList.append(child)
                        closedList.remove(oldPosition)
                    
            #If there are no more options to do with that state, then close it.
            closedList.append(x)
            #Sort the list by the f value = heuristic value + number of moves to that state
            openList = sorted(openList, key = lambda c: c.getHeuristic(heuristic) + c.depth)
        return 'There is no solution for this board.'

    #checks to see if board is solved
    def isSolved(self):
        return self.board == goalBoard

    #make child for branching paths, starts off as a copy
    def makeChild(self):
        p = Puzzle()
        p.setState(self.convertBoard()) #to not have both puzzle classes have the same pinter to the board state
        p.parent = self
        p.depth = self.depth + 1
        p.mnodes = self.mnodes 
        return p
    
    #Returns th calculated heuristic of a given state and a heuristic, h1 or h2
    def getHeuristic(self, heuristic):
        if (heuristic == 'h1'):
            return self.calcH1()
        elif(heuristic == 'h2'):
            return self.calcH2()
        
    #This is to create a list of every possible child of a given parent puzzle
    def makeNextChildren(self):
        moves = self.validMoves()

        #x and y are position to move b to
        def makeNextChild(dire):
            c = self.makeChild()
            c.move(dire)
            return c

        possibleChildren = []
        for move1 in moves:
            possibleChildren.append(makeNextChild(move1))
        return possibleChildren

    #Calculate H1
    def calcH1(self):
        h1 = 0
        for x in range(3):
            for y in range(3):
                if(self.board[x][y] != 'b' and goalBoard[x][y] != self.board[x][y]):
                    h1 += 1
        #loop thru the state
        return h1

    #Calculate H2
    def calcH2(self):
        h2 = 0
        for x in range(3):
            for y in range(3):
                if(self.board[x][y] != 'b'):
                    ind1 = int(self.board[x][y]) % 3 #use to get the y
                    ind2 = int(int(self.board[x][y]) / 3) #use to get the x position of the number in the goal state
                    h2 += abs(x - ind2) + abs(y - ind1)
        #loop thru the state
        return h2



    # The main method that allows for user input
def main():
    #n is the puzzle state unique to the command file
    n = Puzzle()
    for line in fileinput.input('commands.txt'):
        exec(line)

    p = Puzzle()
    inp = ''
    random.seed(100)
    while(inp != 'quit'):
        inp = input('Here is a list of functions. Type what function you would like to run!\nsetState\tprintState\trandomizeState\tmove\tmaxNodes\tsolve a-star\n->')
        print()
        if(inp == 'setState'):
            p.setState(input("Input Board State: \n>>"))

        if(inp == 'printState'):
            p.printState()
        
        if(inp == 'move'):
            p.move(input('What direction do you want to move? (up, down, left, right): '))
        
        if(inp == 'randomizeState'):
            p.randomizeState(int(input('How many steps should we randomize?: ')))
        
        if(inp == 'maxNodes'):
            p.maxNodes(int(input('What is the maximum number of nodes allowed to be used during search: ')))

        if(inp == 'solve a-star'):
            print(p.solveAstar(input('What heuristic do you want to use? (h1 or h2): ')))


if __name__ == '__main__':
    main()