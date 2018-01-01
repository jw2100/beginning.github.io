from numpy import *

class treeNode():
	def __init__(self, feat, val, right, left):
		featureToSplitOn = feat
		valueOfSplit = val
		rightBranch  = right
		leftBranch   = left



def loadDataSet(filename):
	dataMat = []
	fr = open(filename)
	for line in fr.readline():
		curLine = line.strip().split('\t')
		fltLine = map(float, curLine)
		dataMat.append(fltLine)
	return dataMat


def binSplitDataSet(dataSet, feature, value):
	mat0 = dataSet[nonzero(dataSet[:, feature] >  value)[0], :][0]
	mat1 = dataSet[nonzero(dataSet[:, feature] <= value)[0], :][0]
	return mat0, mat1

