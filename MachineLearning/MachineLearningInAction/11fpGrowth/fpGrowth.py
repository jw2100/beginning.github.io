class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode      #needs to be updated
        self.children = {} 
    
    def inc(self, numOccur):
        self.count += numOccur
        
    def disp(self, ind=1):
        print('  '*ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind+1)
    # def __lt__(self, other):
    #     return self.count < other.count
    # def __eq__(self, other):
    #     return self.count == other.count

def createTree(dataSet, minSup = 1):
    headerTable = {}
    # 统计次数
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    # 删除不符合的次数
    for k in list(headerTable.keys()):
        if headerTable[k] < minSup:
            del(headerTable[k])
    freqItemSet = set(headerTable.keys())
    if len(freqItemSet) == 0:
        return None,None
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]
    retTree = treeNode('NULL Set', 1, None)
    for tranSet, count in dataSet.items():
        localD = {}
        # 每一个数据集只保留符合条件的元素
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key = lambda p:p[1], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count)
    return retTree, headerTable

# 一个数据集 + 数 + 头指针表 + 一个数据集的数量
def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children: # 数据集的第一个元素在根的子集中
        inTree.children[items[0]].inc(count)
    else:
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] == None: # 头指标表为空的话
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            # 确保链接指向树中该元素的每一个实例
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    # 递归填充
    if len(items) > 1:
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)

# 找到当前元素实例的最后一个，并且链式当前的
def updateHeader(nodeToTest, targetNode):
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode



def loadSimpDat():
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpDat

def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict

# 发现以给定元素项结尾的所有路径--
def ascendTree(leafNode, prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)

def findPrefixPath(basePat, treeNode):
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats
    


def mineTree(inTree, headerTable, minSup, preFix, freqItemSet):
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p:p[1][0])]
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemSet.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        myCondTree, myHead = createTree(condPattBases, minSup)
        if myHead != None:
            print('conditional tree for: ',newFreqSet)
            myCondTree.disp(1)        
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemSet)

