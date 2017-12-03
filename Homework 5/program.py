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
    # display it here better
    question1b()


    #close the window to display part c

    flips = [(1,1),(2,2),(2,3),(3,4)]
    for x in range(4):
        question1c(x, flips[x])


    
    plt.show()

def postProbTheta(theta, y, n):
    probability = pow(theta, y) * pow(1 - theta, n - y) * nCr(n,y) * (n + 1)
    return probability


def question2():
    prior = [.1, .2, .4, .2, .1]
    limeProb = [0, .25, .5, .75, 1]
    dataH = []
    for x in range(4):
        dataH.append(generateData(limeProb[x]))

    for x in range(4):
        #here we cal the graph for each bag, and print out each value
        graphForBag(x, dataH[x])
    
    plt.show()


#for each given bag, 0, 1, 2, 3 representing h1, h2, h3, h4 respectively
def graphForBag(bag, dataH):
    
    prior = [.1, .2, .4, .2, .1]
    limeProb = [0, .25, .5, .75, 1]
    plotColor = ['ro', 'b^', 'gx', 'yp', 'kD']
    
    totalCandyProb = 0
    for z in range(5):
        totalCandyProb = totalCandyProb + (prior[z] * limeProb[z])
        plt.figure(bag)
        plt.subplot(121)
        plt.title('Data set having bag h{}'.format(bag + 1))
        plt.plot(0, prior[z], plotColor[z], label='h{}'.format(z + 1))
        plt.legend()
        plt.subplot(122)
        plt.title('Probability next candy is lime')
        

    for x in range(100):
        totalCandyProb = 0
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
            plt.figure(bag)
            plt.subplot(121)
            plt.plot(x+1, prior[y], plotColor[y], label='h{}'.format(y + 1))

        #separate subplot to show the probability that next is lime
        plt.subplot(122)
        plt.plot(x,totalLimeProb, 'ko')



def generateData(probLime):
    data = []
    random.seed(100)
    for x in range(100):
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
    #question1()
    question2()