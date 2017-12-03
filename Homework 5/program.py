import matplotlib.pyplot as plt
import numpy as np
#below is copied from internet to compute nCr
import math
import random

def nCr(n,r):
    f = math.factorial
    return f(n) // f(r) // f(n-r)

def question1b():
    probList = []
    for y in range(5):
        probList.append(probabilityY(y, .75, 4))

    plt.figure(0)
    plt.plot(probList, 'ro')
    plt.plot(probList, 'k')
    plt.axis([-.1, 5, -.01, .5])
    plt.ylabel('Probability of y')
    plt.xlabel('Value of y')
    plt.title('Probability of y given theta = 3/4 and n = 4')

    return probList

def probabilityY(y, theta, n):
    probability = pow(theta, y) * pow(1 - theta, n - y) * nCr(n,y)
    return probability

def question1c(iteration, flips):
    probList = []
    #set of points from 0 to 1 with step intervals of .01
    theta = np.arange(0, 1, .01)
    #manually changed the below values for the four graphs
    y = flips[0]
    n = flips[1]
    for t in theta:
        probList.append(postProbTheta(t, y, n))

    plt.figure(iteration + 1)
    plt.plot(theta, probList, 'ro')
    plt.plot(theta, probList, 'k')
    
    #plt.axis([-.1, 1.1, -.01, 2])
    plt.ylabel('Probability of theta')
    plt.xlabel('Value of theta')
    plt.title('p(θ | y={}, n={})'.format(y,n))
    

def question1():
    question1b()
    
    flips = [(1,1),(2,2),(2,3),(3,4)]
    for x in range(4):
        question1c(x, flips[x])
        

def postProbTheta(theta, y, n):
    probability = pow(theta, y) * pow(1 - theta, n - y) * nCr(n,y) * (n + 1)
    return probability


def question2():
    prior = [.1, .2, .4, .2, .1]
    limeProb = [0, .25, .5, .75, 1]
    dataH = []
    for x in range(4):
        dataH.append(generateData(limeProb[x], 100))

    for x in range(4):
        #here we cal the graph for each bag, and print out each value
        priorPlot, limeProbPlot = calcForBag(x, dataH[x])
        graphForBag(x, priorPlot, limeProbPlot)



#for each given bag, 0, 1, 2, 3 representing h1, h2, h3, h4 respectively
def calcForBag(bag, dataH):
    
    prior = [.1, .2, .4, .2, .1]
    limeProb = [0, .25, .5, .75, 1]
    plotColor = ['ro', 'b^', 'gx', 'yp', 'kD']
    
    totalCandyProb = 0
    for z in range(5):
        totalCandyProb = totalCandyProb + (prior[z] * limeProb[z])
        
    # Used to calculate 2c and graph it
    sumList = [0, 0, 0, 0, 0]
    priorPlot = [ [.1], [.2], [.4], [.2], [.1] ]
    limeProbPlot = [.5]

    for x in range(len(dataH)):
        #probability that a candy drawn is what it is
        totalCandyProb = 0

        #probability that you draw a lime
        totalLimeProb = 0

        for z in range(5):
            # 1 is a cherry, 0 is a lime. P(Cherry) = 1 - p(lime)
            if(dataH[x] == 1):
                totalCandyProb = totalCandyProb + (prior[z] * (1 - limeProb[z]))
            else:
                totalCandyProb = totalCandyProb + (prior[z] * limeProb[z])

        if(dataH[x] == 1):
            totalLimeProb = 1 - totalCandyProb
        else:
            totalLimeProb = totalCandyProb   

        for y in range(5):
            if(dataH[x] == 1):
                prior[y] = (1 - limeProb[y]) * prior[y] / totalCandyProb
            else:
                prior[y] = limeProb[y] * prior[y] / totalCandyProb
            #put labels
            sumList[y] += prior[y]
            
            priorPlot[y].append(prior[y])

        #separate subplot to show the probability that next is lime
        limeProbPlot.append(totalLimeProb)

    return priorPlot, limeProbPlot

def graphForBag(bag, priorPlot, limeProbPlot):
    
    prior = [.1, .2, .4, .2, .1]
    limeProb = [0, .25, .5, .75, 1]
    plotColor = ['ro', 'b^', 'gx', 'yp', 'kD']
    
    for z in range(5):
        plt.figure(bag + 5)
        plt.subplot(121)
        plt.title('Data set having bag h{}'.format(bag + 1))
        plt.plot(0, prior[z], plotColor[z], label='h{}'.format(z + 1))
        plt.legend()
        plt.subplot(122)
        plt.title('Probability next candy is lime')

    for y in range(5):
        plt.figure(bag + 5)
        plt.subplot(121)
        plt.plot(range(101), priorPlot[y], plotColor[y], label='h{}'.format(y + 1))

    plt.subplot(122)
    plt.plot(range(101),limeProbPlot, 'ko')

def graphForError(bag):
    
    limeProb = [0, .25, .5, .75, 1]
    bagSum = [0, 0, 0, 0, 0]
    plotColor = ['ro', 'b^', 'gx', 'yp', 'kD']
    #for each bag type we are testing, do trials to show reduction in uncertainty for the specific bag
    #for x in range(4):
    x = bag
    bagAvg = [ [], [], [], [], [] ]
    for y in range(100):
        priorPlot, limeProbPlot = calcForBag(y, generateData(limeProb[x], 100))
        for z in range(5):
            bagSum[z] += priorPlot[z][len(priorPlot[z]) - 1]#final value of the probability that a certain bag is the type of bag the data represents
            bagAvg[z].append((bagSum[z]/(y + 1)))
    
    for y in range(5):    
        plt.figure(x + 9)
        plt.title('Error reduction with data as bag h{}'.format(x + 1))
        plt.plot(bagAvg[y], plotColor[y], label='h{}'.format(y + 1))

    

def generateData(probLime, length):
    data = []
    for x in range(length):
        if(probLime > 0 ):
            rVel = (random.uniform(0,1) * 4)
        else:
            rVel = 1;

        # 0 is lime, 1 is cherry
        if rVel < 4 * probLime:
            data.append(0)
        else:
            data.append(1)
        
    return data

if __name__ == "__main__":
    question1()
    question2()
    for x in range(4):
        graphForError(x)
    plt.legend()
    plt.show()