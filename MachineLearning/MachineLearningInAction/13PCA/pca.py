from numpy import *

def loadDataSet(fileName, delim='\t'):
    fr = open(fileName)
    stringArr = [line.strip().split(delim) for line in fr.readlines()]
    datArr = [list(map(float,line)) for line in stringArr]
    return mat(datArr)

def pca(dataMat, topNfeat=9999999):
    meanVals    = mean(dataMat, axis=0) # 均值
    meanRemoved = dataMat - meanVals    # 减去均值 #remove mean
    covMat      = cov(meanRemoved, rowvar=0)    # 协方差
    eigVals,eigVects = linalg.eig(mat(covMat))  # 特征值和特征向量
    eigValInd   = argsort(eigVals)              #sort, sort goes smallest to largest
    eigValInd   = eigValInd[:-(topNfeat+1):-1]  #cut off unwanted dimensions
    redEigVects = eigVects[:,eigValInd]         #reorganize eig vects largest to smallest
    lowDDataMat = meanRemoved * redEigVects     #transform data into new dimensions
    reconMat = (lowDDataMat * redEigVects.T) + meanVals
    return lowDDataMat, reconMat


    