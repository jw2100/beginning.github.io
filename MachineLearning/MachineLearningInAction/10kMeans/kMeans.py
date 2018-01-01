from numpy import *

def loadDataSet(fileName):      #general function to parse tab -delimited floats
    dataMat = []                #assume last column is target value
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = list(map(float,curLine)) #map all elements to float()
        dataMat.append(fltLine)
    return dataMat

def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2))) #la.norm(vecA-vecB)

def randCent(dataSet, k):
    n = shape(dataSet)[1]
    centroids = mat(zeros((k,n)))#create centroid mat
    for j in range(n):#create random cluster centers, within bounds of each dimension
        minJ = min(dataSet[:,j]) 
        rangeJ = float(max(dataSet[:,j]) - minJ)
        centroids[:,j] = mat(minJ + rangeJ * random.rand(k,1))
    return centroids

def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
    m = shape(dataSet)[0]
    # 对每一个样本第一列保存属于哪个簇，第二列保存平方误差
    clusterAssment = mat(zeros((m,2)))
    # 随机初始化K个簇中心
    centroids = createCent(dataSet, k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        # 找到每一个样本距离最近的簇
        for i in range(m):
            minDist  = inf
            minIndex = -1
            #便利每一个簇
            for j in range(k):
                distJI = distMeas(centroids[j,:], dataSet[i,:])
                if distJI < minDist:
                    minDist  = distJI
                    minIndex = j
            # 样本i的簇发生改变
            if clusterAssment[i, 0] != minIndex:
                clusterChanged = True
            # 更新样本i的簇和平方误差
            clusterAssment[i,:] = minIndex, minDist**2
        print(centroids)
        for cent in range(k):
            # 重新计算每一个簇的点(坐标)
            pstInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]
            centroids[cent,:] = mean(pstInClust, axis=0)
    return centroids, clusterAssment


# 二分K均法
def biKmeans(dataSet, k, distMeas = distEclud):
    m = shape(dataSet)[0]
    #对每一个样本第一列保存属于哪个质新，第二列保存平方误差
    clusterAssment = mat(zeros((m,2)))
    #初始化第一个族
    centList = [mean(dataSet, axis = 0).tolist()[0]] # get one centor
    #初始化 每一个样本的平方误差
    for j in range(m):
        clusterAssment[j,1] = distMeas(mat(centroids), dataSet[j,:])**2
    while (len(centList)) < k:
        # 赋值无穷大
        lowestSSE = inf
        for i in range(len(centList)):
            # 第i个族的所有样本
            ptsInCurrCluster = dataSet[nonzero(clusterAssment[:,0].A == i)[0],:]
            # 进行2分 
            centroidMat, splitClustAss = kMeans(ptsInCurrCluster, 2, distMeas)
            # 第i个族2分之后的总平方误差
            sseSplit    = sum(splitClustAss[:,1])
            # 除第i个族其他的总平方误差
            sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:,0].A != i)[0], 1])
            #找到最低的,保存划分的质点+质点的值+误差值
            if sseSplit + sseNotSplit < lowestSSE:
                bestCentToSplit = i
                bestNewCents    = centroidMat
                bestClustAss    = splitClustAss.copy()
                lowestSSE       = sseSplit + sseNotSplit
        # 结束循环后,最好的划分(第i个)：
        # 最好的划分的第1个簇赋值为，被二分的那个簇
        bestClustAss[nonzero(bestClustAss[:,0].A == 0)[0], 0] = bestCentToSplit
        # 最好的划分的第2个簇赋值为，当前簇的长度(从0开始，所以，类似于+1了)
        bestClustAss[nonzero(bestClustAss[:,0].A == 1)[0], 0] = len(centList)
        print("the bestCentToSplit is :", bestCentToSplit)
        print("the len of bestCentToSplit is :", len(bestCentToSplit))
        # 被二分的那个族的值(坐标)变为新的, 跟上面对应
        centList[bestCentToSplit] = bestNewCents[0,:]
        # 添加一个新的族的值
        centList.append(bestNewCents[1,:])
        clusterAssment[nonzero(clusterAssment[:,0].A==bestCentToSplit)[0], :] = bestClustAss
    return mat(centList), clusterAssment




