
from math import log

def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing','flippers']
    #change to discrete values
    return dataSet, labels

#计算一个数据集的商
def calcShannonEnt(dataSet):
	numEntries  = len(dataSet)
	labelCounts = {}
	for featVec in dataSet:
		currentLabel = featVec[-1]
		if currentLabel not in labelCounts.keys():
			labelCounts[currentLabel] = 0
		labelCounts[currentLabel] += 1
	shannontEnt = 0.0
	for key in labelCounts:
		prob = float(labelCounts[key]) / numEntries
		shannontEnt -= prob * log(prob, 2)
	return shannontEnt

# 按照一个特征的取值 进行划分，返回划分后的值
def splitDataSet(dataSet, axis, value) :
	'''
	待划分数据集, 特征，返回的特征值
	'''
	retDataSet = []  # dataset传递引用，所以新申明一个
	for featVec in dataSet:
		if featVec[axis] != value:
			continue
		reducedFeatVec = featVec[:axis]
		reducedFeatVec.extend(featVec[axis+1:])
		retDataSet.append(reducedFeatVec)
	return retDataSet


# 选择最好的划分
def chooseBestFeatureToSplit(dataSet):
	numFeatures = len(dataSet[0]) - 1
	baseEntropy = calcShannonEnt(dataSet)
	bestInfoGain= 0.0
	bestFeature = -1
	for i in range(numFeatures):
		featList  = [example[i] for example in dataSet]
		uniqueVals= set(featList)
		newEntropy= 0.0
		for value in uniqueVals: # 对于一个特征的所有取值
			subDataSet = splitDataSet(dataSet, i, value)
			prob = len(subDataSet) / float(len(dataSet))
			newEntropy += prob * calcShannonEnt(subDataSet)
		infoGain = baseEntropy - newEntropy
		if infoGain > bestInfoGain:
			bestInfoGain = infoGain
			bestFeature  = i
	return bestFeature

def majorityCnt(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]



def createTree(dataSet, labels):
	classList = [example[-1] for example in dataSet]
	if classList.count(classList[0]) == len(classList): # 列表完全相同
		return classList[0]
	if len(dataSet[0]) == 1: # 遍历完所有特征，叶子返回最多的分类
		return majorityCnt(classList)
	bestFeatIndex = chooseBestFeatureToSplit(dataSet)
	bestFeatLabel = labels[bestFeatIndex]
	myTree = {bestFeatLabel:{}}
	del(labels[bestFeatIndex])
	featValues = [example[bestFeatIndex] for example in dataSet] #得到划分特征的所有值
	uniqueVals = set(featValues)
	for value in uniqueVals:
		subLabels = labels[:] #因为列表传递引用
		myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeatIndex, value), subLabels)
	return myTree


def  classify(inputTree, featLables, testVec):

	firstStr   = list(inputTree.keys())[0]
	secondDict = inputTree[firstStr]
	featIndex  = featLables.index(firstStr)
	for key in secondDict.keys():
		if testVec[featIndex] != key:
			continue
		if type(secondDict[key]).__name__ == 'dict':
			classLabel = classify(secondDict[key], featLables, testVec)
		else:
			classLabel = secondDict[key]
	return classLabel


def storeTree(inputTree, filename) :
	import pickle
	fw = open(filename, 'w')
	pickle.dump(inputTree, fw)
	fw.close()

def grabTree(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)


def test():
	fr = open('lenses.txt')
	lenses = [inst.strip().split('\t') for inst in fr.readlines()]
	lensesLabels = ['age', 'prescript', 'astigmatic', 'tearRate']
	lensesTree   = trees.createTree(lenses, lensesLabels)
	treePlotter.createPlot(lensesTree)
