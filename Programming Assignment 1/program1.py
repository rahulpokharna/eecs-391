import random
import math
import fileinput

goalState = 'b12 345 678' #used to check final state
goalBoard = [['b', '1', '2'], ['3', '4', '5'], ['6', '7', '8']] #used to check final board


class Puzzle:

    #onstructor
    def __init__(self):
        self.board = [[0 for x in range(3)] for y in range(3)] #array for representing the board
        self.mnodes = 10000 #max nodes allowed during search, stop when limit is reached
        self.parent = None
        self.parentMove = 'Completed'
        self.depth = 0
        self.h = 1000000
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
        self.h = h1
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
        self.h = h2
        return h2



    # The main method that allows for user input
def main():
    #n is the puzzle state unique to the command file
    n = Puzzle()
    c = RubikCube()
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


def RubikCube(Puzzle):
    
    #strings are treated as arrays of characters
    self.board = 'yyyyggggoooobbbbrrrrwwww'
    self.goalCube = 'yyyyggggoooobbbbrrrrwwww'
    
    self.manHelper = [[0, 1, 2, 1, 2, 3, 2, 1],
            [1, 0, 1, 2, 3, 2, 1, 2],
            [2, 1, 0, 1, 2, 1, 2, 3],
            [1, 2, 1, 0, 1, 2, 3, 2],
            [2, 3, 2, 1, 0, 1, 2, 1],
            [3, 2, 1, 2, 1, 0, 1, 2],
            [2, 1, 2, 3, 2, 1, 0, 1],
            [1, 2, 1, 0, 1, 2, 3, 2]];


    def __init__(self):
        print('hi')
    
    def setState(self, inp):
        self.board = inp
    
    def randomizeState(self, n):
        moves = ["F", "F'", "U", "U'", "R", "R'"]
        self.setState(goalCube)
        for x in range(n):
            #randomly choose 1 to 4, each being a direction
            d = random.choice(moves)
            self.move(d)
        print('After randomizing, the ', end='')
        self.printState()

    def move(self, dir):
        if(dir == "U"):
            self.moveU()
        
        if(dir == "U'"):
            self.moveU()
            self.moveU()
            self.moveU()
        
        if(dir == "F"):
            self.moveF()
        
        if(dir == "F'"):
            self.moveF()
            self.moveF()
            self.moveF()

        if(dir == "R"):
            self.moveR()

        if(dir == "R'"):
            self.moveR()
            self.moveR()
            self.moveR()

    def moveU(self):
        self.swap4(0, 1, 2, 3);
        self.swap4(4, 16, 12, 8);
        self.swap4(5, 17, 13, 9);
    
    def moveF(self):
        self.swap4(3, 12, 21, 6);
        self.swap4(8, 9, 10, 11);
        self.swap4(2, 15, 20, 5);

    def moveR(self):
        self.swap4(12, 13, 14, 15);
        self.swap4(2, 16, 22, 10);
        self.swap4(1, 19, 21, 9);

    def swap4(c1, c2, c3, c4):
        self.swap(c1, c2);
        self.swap(c1, c3);
        self.swap(c1, c4);

    def swap(self, c1, c2):
        self.board[c1], self.board[c2] = self.board[c2], self.board[c1] 

    #using inheritance so the same methods as the normal puzzle class
    def validMoves(self):
        return ["F", "F'", "U", "U'", "R", "R'"]

    def isSolved(self):
        return self.board == self.goalCube

    def makeChild(self):
        p = RubikCube()
        p.setState(self.board) #to not have both puzzle classes have the same pinter to the board state
        p.parent = self
        p.depth = self.depth + 1
        p.mnodes = self.mnodes 
        return p

    def printState(self):
        print('Current board state:', end="\n  ")
        print(self.board[0], end = "")
        print(self.board[1], end = "   \n  ")
        print(self.board[3], end = "")
        print(self.board[2], end = "   \n")
        print(self.board[4], end = "")
        print(self.board[5], end = "")
        print(self.board[8], end = "")
        print(self.board[9], end = "")
        print(self.board[12], end = "")
        print(self.board[13], end = "")
        print(self.board[16], end = "")
        print(self.board[17], end = "\n")
        print(self.board[7], end = "")
        print(self.board[6], end = "")
        print(self.board[11], end = "")
        print(self.board[10], end = "")
        print(self.board[15], end = "")
        print(self.board[14], end = "")
        print(self.board[19], end = "")
        print(self.board[18], end = "\n  ")
        print(self.board[20], end = "")
        print(self.board[21], end = "")
        print(self.board[23], end = "")
        print(self.board[22], end = "   \n")

    def toArray(self):
        cubeArray = [['0' for x in range(3)] for  y in range(8)]
        cubeArray[0] = [self.board[0], self.board[16], self.board[4]]
        cubeArray[1] = [self.board[1], self.board[13], self.board[17]]
        cubeArray[2] = [self.board[2], self.board[9], self.board[12]]
        cubeArray[3] = [self.board[3], self.board[5], self.board[8]]
        cubeArray[4] = [self.board[20], self.board[6], self.board[11]]
        cubeArray[5] = [self.board[21], self.board[10], self.board[15]]
        cubeArray[6] = [self.board[22], self.board[14], self.board[19]]
        cubeArray[7] = [self.board[23], self.board[7], self.board[18]]
        return cubearray

    def goalState(self):
        cubeArray = [['0' for x in range(3)] for  y in range(8)]
        cubeArray[0] = [self.goalCube[0], self.goalCube[16], self.goalCube[4]]
        cubeArray[1] = [self.goalCube[1], self.goalCube[13], self.goalCube[17]]
        cubeArray[2] = [self.goalCube[2], self.goalCube[9], self.goalCube[12]]
        cubeArray[3] = [self.goalCube[3], self.goalCube[5], self.goalCube[8]]
        cubeArray[4] = [self.goalCube[20], self.goalCube[6], self.goalCube[11]]
        cubeArray[5] = [self.goalCube[21], self.goalCube[10], self.goalCube[15]]
        cubeArray[6] = [self.goalCube[22], self.goalCube[14], self.goalCube[19]]
        cubeArray[7] = [self.goalCube[23], self.goalCube[7], self.goalCube[18]]
        return cubearray;


    def calcH1(self):
        goalA = self.goalState()
        boardArray = self.toArray()
        for x in range(8):
            goalA[x].sort()
            boardArray[x].sort()

        calcArray = []
        for x in range(8):
            for y in range(8):
                if boardArray[x] == goalA[y]:
                    calcArray[y] = y
        m = 0
        for x in range(8):
            m += self.manHelper[x][calcArray[x]]
        return m

    def calcH2(self):
        h2 = 0
        
        goalA = self.goalState()
        boardArray = self.toArray()

        for x in range(8):
            if goalA[x] != boardArray[x]:
                h2 += 1
        
        return h2


if __name__ == '__main__':
    main()