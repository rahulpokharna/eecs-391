import matplotlib.pyplot as plt
import numpy as np
#below is copied from internet to compute nCr
import math
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

if __name__ == "__main__":
    question1()