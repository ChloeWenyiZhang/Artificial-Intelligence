import copy

def showMap(matrix):
    for x in range(0, 3):
        for y in range(0, 3):
            print(matrix[x][y], end=' ')
        print('\n')
    print("--------")
    return

def move(matrix, srcX, srcY, drcX, drcY):
    temp = matrix[srcX][srcY]
    matrix[srcX][srcY] = matrix[drcX][drcY]
    matrix[drcX][drcY] = temp
    return matrix


class Node:
    def __init__(self, matrix, g=0, h=0):
        self.matrix = matrix  # 把九宫格抽象为矩阵
        self.father = None  # 父节点
        self.g = g  # g(x)
        self.h = h  # h(x)
    """
    估价函数————类似曼哈顿距离
     """
    def setH(self, endNode):
        for x in range(0, 3):
            for y in range(0, 3):
                for m in range(0, 3):
                    for n in range(0, 3):
                        if self.matrix[x][y] == endNode.matrix[m][n]:
                            #self.h += abs(x * y - m * n)
                            if (self.matrix[x][y] != 0):
                                self.h += abs(x - m + y - n)

    def setG(self, g):
        self.g = g

    def setFather(self, node):
        self.father = node

    def getG(self):
        return self.g

    def getF(self):
        return self.h + self.g

class A:
    def __init__(self, startNode, endNode):
        self.openList = []
        self.closeList = []
        self.startNode = startNode
        self.endNode = endNode
        self.currentNode = startNode
        self.pathlist = []
        self.step = 0
        return

    def isSame(self):
        if self.startNode.matrix == self.endNode.matrix:
            return True

    def getMinFNode(self):
        """
        获得openlist中F值最小的节点
        """
        nodeTemp = self.openList[0]
        for node in self.openList:
            if node.getF() < nodeTemp.getF():
                nodeTemp = node
        return nodeTemp

    def nodeInOpenlist(self, node):
        for nodeTmp in self.openList:
            if nodeTmp.matrix == node.matrix:
                return True
        return False

    def nodeInCloselist(self, node):
        for nodeTmp in self.closeList:
            if nodeTmp.matrix == node.matrix:
                return True
        return False

    def endNodeInOpenList(self):
        for nodeTmp in self.openList:
            if nodeTmp.matrix == self.endNode.matrix:
                return True
        return False

    def getNodeFromOpenList(self, node):
        for nodeTmp in self.openList:
            if nodeTmp.matrix == node.matrix:
                return nodeTmp
        return None

    def searchOneNode(self, node):
        """
        搜索一个节点
        """
        # closeList不用考虑
        if self.nodeInCloselist(node):
            return
        # G(x)计算
        gTemp = self.step

        # 如果不在openList中，就加入openlist
        if self.nodeInOpenlist(node) == False:
            node.setG(gTemp)
            # 计算启发h(x)
            node.setH(self.endNode)
            # 加入openList
            self.openList.append(node)
            # 当前节点置为父节点
            node.father = self.currentNode

        # 如果在openList中，判断currentNode到当前点的G是否更小
        # 如果更小，就重新计算g(x)，并且改变父节点
        else:
            nodeTmp = self.getNodeFromOpenList(node)
            if self.currentNode.g + gTemp < nodeTmp.g:
                nodeTmp.g = self.currentNode.g + gTemp
                nodeTmp.father = self.currentNode
        return

    def searchNear(self):
        """
        寻找下一个可以移动的数字
        然后找到0所在的位置令它们进行交换
        """
        x=0
        y=0
        flag = False
        for x in range(0, 3):
            for y in range(0, 3):
                if self.currentNode.matrix[x][y] == 0:
                    flag = True
                    break
            if flag == True:
                break
        self.step += 1
        if x - 1 >= 0:
            matrixTemp = move(copy.deepcopy(self.currentNode.matrix), x, y, x - 1, y)
            self.searchOneNode(Node(matrixTemp))
        if x + 1 < 3:
            matrixTemp = move(copy.deepcopy(self.currentNode.matrix), x, y, x + 1, y)
            self.searchOneNode(Node(matrixTemp))
        if y - 1 >= 0:
            matrixTemp = move(copy.deepcopy(self.currentNode.matrix), x, y, x, y - 1)
            self.searchOneNode(Node(matrixTemp))
        if y + 1 < 3:
            matrixTemp = move(copy.deepcopy(self.currentNode.matrix), x, y, x, y + 1)
            self.searchOneNode(Node(matrixTemp))
        return

    def start(self):
        '''''
        开始寻路
        '''
        # 将初始节点加入openList
        self.startNode.setH(self.endNode)
        self.startNode.setG(self.step)
        self.openList.append(self.startNode)

        while True:
            # 获取openList里F值最小的节点
            # 并把它添加到closeList，从openList删除
            self.currentNode = self.getMinFNode()
            self.closeList.append(self.currentNode)
            self.openList.remove(self.currentNode)
            self.step = self.currentNode.getG()
            self.searchNear()
            # 检验是否结束
            if self.endNodeInOpenList():
                nodeTmp = self.getNodeFromOpenList(self.endNode)
                while True:
                    self.pathlist.append(nodeTmp)
                    if nodeTmp.father != None:
                        nodeTmp = nodeTmp.father
                    else:
                        return True
            elif len(self.openList) == 0:
                return False
            elif self.step > 100:
                return False
        return True

    def showPath(self):
        for node in self.pathlist[::-1]:  # 是返回倒序的原列表
            showMap(node.matrix)

    def showSteps(self):
        print(self.step)

