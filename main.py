#coded by Divij Garg
import random
import statistics
import numpy as np
import scipy.stats
from matplotlib import pyplot as plt

meansOfSamples = []  # stores the mean frequency of each of the samples
stDevOfSamples = []  # stores the mean standard deviation of each of the samples
pastPositions = []  # stores the positions for each sample
freqArray = []  # stores the frequencies for each space in each of the samples
expectedFrequencies = []
communityChest=[] #types: 1=go, 2=jail, 0=do nothinf
chance=[] #1=go, 2=jail, 3=boardwalk, 4=illinois, 5=st charles, 6=railroad, 7=utility, 8=go back 3 spaces, 9=reading railroad, 0=do nothing

numberOfSamples = 1
trialAmounts = 1000000
populationMean = 0
currentPosition = 0

def main():
    global freqArray, meansOfSamples, numberOfSamples, populationMean, expectedFrequencies, communityChest, chance
    setArrays()
    for i in range(0, numberOfSamples):
        np.random.shuffle(communityChest)
        np.random.shuffle(chance)
        print(communityChest)
        np.random.shuffle(chance)
        doSample(i)
        expectedFrequencies[i] = [statistics.mean(freqArray[i]) for _ in range(0, 40)]
        doChiSquare(freqArray[i], expectedFrequencies[i])
        analyzeData(i)
    populationMean = statistics.mean(meansOfSamples)


def doChiSquare(observed, expected):
    sqDif=[]
    testStatistic=0
    print(observed)
    print(expected)
    for i in range(0,len(observed)):
        sqDif.append((observed[i]-expected[i])*(observed[i]-expected[i])/expected[i])
        testStatistic+=sqDif[i]
    print(testStatistic)
    actualStat=scipy.stats.chi2.ppf(1 - .05, df=39)
    print(1-scipy.stats.chi2.cdf(testStatistic,df=39))
    print(actualStat)


def setArrays():
    global meansOfSamples, stDevOfSamples, pastPositions, expectedFrequencies, freqArray, numberOfSamples, communityChest, chance
    meansOfSamples = [0 for _ in range(0, numberOfSamples)]
    stDevOfSamples = [0 for _ in range(0, numberOfSamples)]
    pastPositions = [[] for _ in range(0, numberOfSamples)]
    expectedFrequencies = [[] for _ in range(0, numberOfSamples)]
    freqArray = [[] for _ in range(0, numberOfSamples)]
    communityChest=[1,2]
    for i in range(0,14):
        communityChest.append(0)
    # 1=go, 2=jail, 3=boardwalk, 4=illinois, 5=st charles, 6=railroad, 7=utility, 8=go back 3 spaces, 9=reading railroad, 0=do nothing
    chance=[1,2,3,4,5,6,6,7,0,0,8,0,0,9,0,0]


def doTurn(index, repeat):
    global currentPosition, pastPositions
    if (repeat >= 3):
        # print()
        changePos(10,index)
    else:
        roll1 = rollDice()
        roll2 = rollDice()
        currentPosition += roll2 + roll1

        if currentPosition >= 40:
            currentPosition = currentPosition % 40
        if currentPosition==7 or currentPosition==22 or currentPosition==36:
            doChance(index)
        if currentPosition==2 or currentPosition==17 or currentPosition==33:
            doCommunity(index)
        if currentPosition==30:
            pastPositions[index].append(currentPosition)
            changePos(10,index)
        else:
            pastPositions[index].append(currentPosition)
            if roll2 == roll1:
                # print("repeat")
                doTurn(index, repeat + 1)


def rollDice():
    return (int)((random.random() * 6) + 1)


def analyzeData(index):
    global pastPositions
    # print(pastPositions)
    # https://www.geeksforgeeks.org/plotting-histogram-in-python-using-matplotlib/
    # a=np.array(currentPosition)
    # print(pastPositions)
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.hist(np.array(pastPositions[index]),
            bins=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                  28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40])
    plt.show()


# This code is contributed by avanitrachhadiya2155, https://www.geeksforgeeks.org/count-frequencies-elements-array-o1-extra-space-time/
def findCounts(index, arr):
    global freqArray
    freqArray[index] = [0 for i in range(0, 40)]
    for i in arr:
        freqArray[index][i] += 1


def calcStats(index, arr):
    global meansOfSamples, stDevOfSamples
    mean = statistics.mean(arr)
    stDev = statistics.stdev(arr)
    meansOfSamples[index] = mean
    stDevOfSamples[index] = stDev


def redoData():
    global freqArray
    min = freqArray[0]

    for i in freqArray:
        if min > i:
            min = i

    for i in range(0, len(freqArray)):
        freqArray[i] = freqArray[i] - min


def doSample(index):
    global pastPositions, freqArray, currentPosition, trialAmounts
    for i in range(0, trialAmounts):
        doTurn(index, 0)
    findCounts(index, pastPositions[index])
    calcStats(index, freqArray[index])
    currentPosition = 0
    # analyzeData(index)

def doCommunity(index):
    global currentPosition, pastPositions,communityChest
    # types: 1=go, 2=jail, 0=do nothing
    card=communityChest[0]
    communityChest=np.delete(communityChest,0)
    communityChest=np.append(communityChest,card)
    if card==1:
        changePos(0,index)
    elif card==2:
        changePos(10,index)

def doChance(index):
    global currentPosition, pastPositions,chance
    # 1=go, 2=jail, 3=boardwalk, 4=illinois, 5=st charles, 6=railroad, 7=utility, 8=go back 3 spaces, 9=reading railroad, 0=do nothing
    card=chance[0]
    chance=np.delete(chance,0)
    chance=np.append(chance,card)

    if card==1:
        changePos(0,index)
    elif card==2:
        changePos(10,index)
    elif card==3:
        changePos(39,index)
    elif card==4:
        changePos(24,index)
    elif card==5:
        changePos(11,index)
    elif card==6:
        tempPos=currentPosition-5
        tempPos+=10-tempPos%10
        tempPos+=5
        changePos(tempPos%40, index)
    elif card==7:
        if currentPosition==36 or currentPosition==7:
            changePos(12,index)
        elif currentPosition==22:
            changePos(28,index)
    elif card==8:
        changePos(currentPosition-3,index)
    elif card==9:
        changePos(5,index)

def changePos(newPos, index):
    global pastPositions
    currentPosition=newPos
    pastPositions[index].append(currentPosition)
main()