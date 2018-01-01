
from numpy import *
import operator
from os import listdir

def createDataSet():
	group  = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
	labels = ['A', 'A', 'B', 'B']
	return group, labels

# KNN algorithm
def classify0(inX, dataSet, labels, k):
	'''
		inX : input vector
		dataSet : training data
	'''
	#computer distinct
	dataSetSize = dataSet.shape[0]
	diffMat     = tile(inX, (dataSetSize, 1)) - dataSet #tile: repeat dataSetSize times in row
	sqDiffMat   = diffMat ** 2
	sqDistances = sqDiffMat.sum(axis=1)
	distances   = sqDistances**0.5

	#select K count (min)
	sortedDistIndicies = distances.argsort() # first sort then get index
	classCount = {}
	for i in range(k):
		voteIlable = labels[sortedDistIndicies[i]]
		classCount[voteIlable] = classCount.get(voteIlable, 0) + 1

	#sort
	sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
	return sortedClassCount[0][0]


#change txt to vector
def file2matrix (filename) :
	fr = open(filename)
	arrayOLines   = fr.readlines()
	numberOfLines = len(arrayOLines)
	#print(numberOfLines);exit();
	returnMat     = zeros((numberOfLines, 3))
	classLableVector = []
	index = 0
	for line in arrayOLines:
		line = line.strip()
		listFromLine = line.split('\t')
		returnMat[index,:]    = listFromLine[0:3]
		# print(type(listFromLine[-1]))
		# print(returnMat)
		classLableVector.append(listFromLine[-1])
		index += 1
	return returnMat, classLableVector


# Mean normalization
def autoNorm (dataSet) :
	minVals = dataSet.min(0) # min(0) : select col min, 
	maxVals = dataSet.max(0) # min()  : select raw min
	ranges  = maxVals - minVals
	normDataSet = zeros(shape(dataSet))
	m = dataSet.shape[0]
	normDataSet = dataSet - tile(minVals, (m,1))
	normDataSet = normDataSet / tile(ranges, (m,1))
	return normDataSet, ranges, minVals


def datingClassTest():
	hoRatio = 0.5
	datingDataMat, datingLables = file2matrix('datingTestSet.txt')
	normMat, ranges, minVals    = autoNorm(datingDataMat)
	m = normMat.shape[0]
	numTestVecs = int(m * hoRatio)
	errorCount  = 0
	for i in range(numTestVecs):
		classifierResult = classify0(normMat[i,:], normMat[numTestVecs:m, :], datingLables[numTestVecs:m], 3)
		print("the classifer came back with:%s --> %s" % (classifierResult, datingLables[i]))

		if (classifierResult != datingLables[i]):
			errorCount += 1.0
	print("total error rate is : %f" % (errorCount/float(numTestVecs)))









def img2vector(filename):
    returnVect = zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j] = int(lineStr[j])
    return returnVect


def handwritingClassTest():
    hwLabels = []
    trainingFileList = listdir('trainingDigits')           #load the training set
    m = len(trainingFileList)
    trainingMat = zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr     = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:] = img2vector('trainingDigits/%s' % fileNameStr)
    testFileList = listdir('testDigits')        #iterate through the test set
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr     = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest  = img2vector('testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
        print("the classifier came back with: %d, the real answer is: %d" % (classifierResult, classNumStr))
        if (classifierResult != classNumStr): errorCount += 1.0
    print("\nthe total number of errors is: %d" % errorCount)
    print("\nthe total error rate is: %f" % (errorCount/float(mTest)))
