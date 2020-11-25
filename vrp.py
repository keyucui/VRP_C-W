from operator import itemgetter
from math import *


class Vrp(object):

    # -----------初始数据定义---------------------
    def __init__(self):

        # 9个客户分别需要的货物的需求量，第0位为配送中心自己
        self.q = [0, 0.3, 1.8, 0.5, 1.4, 0.6, 1.2, 1.5, 0.8, 0.6]
        # 9个客户分别需要的货物的体积，第0位为配送中心自己
        self.v = [0, 11, 5, 12.5, 10, 8, 15.8, 4.8, 14.6, 6]
        self.mans = 9       # 客户数量
        self.tons = 5       # 车辆载重
        self.vols = 50      # 车辆容积
        self.distanceLimit = 60     # 行驶距离限制
        self.distance = []    # 各个客户及配送中心距离
        self.savings = []     # 节约度
        self.Routes = []      # 路线
        self.Cost = 0         # 总路程
        # 下面是10个字母点与index数字的映射map
        self.dot_map = {0: 'P', 1: 'A', 2: 'B', 3: 'C', 4: 'D',
                        5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I'}

    # -----------计算最短距离---------------------
    def distanceCalculate(self):
        # 邻接矩阵
        dis = [
            [0, 9, inf, 12, 12, 11, 16, 20, 15, 16, 9],
            [9, 0, 5, inf, inf, inf, inf, inf, 16, inf, 4],
            [inf, 5, 0, 6, inf, inf, inf, inf, inf, inf, 3],
            [12, inf, 6, 0, 6, inf, inf, inf, inf, inf, 5],
            [12, inf, inf, 6, 0, 4, inf, inf, inf, inf, inf],
            [11, inf, inf, inf, 4, 0, 17, inf, inf, inf, inf],
            [16, inf, inf, inf, inf, 17, 0, 10, inf, inf, inf],
            [20, inf, inf, inf, inf, inf, 10, 0, 15, 8, inf],
            [15, 16, inf, inf, inf, inf, inf, 15, 0, 8, inf],
            [16, inf, inf, inf, inf, inf, inf, 8, 8, 0, inf],
            [9, 4, 3, 5, inf, inf, inf, inf, inf, inf, inf]
        ]

        '''
        Floyd计算各点间最短距离
        '''
        # i为中间节点
        for i in range(11):
            # j为起点
            for j in range(11):
                # k为终点
                for k in range(11):
                    # 更新最短距离
                    dis[j][k] = min(dis[j][k], dis[j][i] + dis[i][k])

        # 初始化最短距离,其中有一个多余的中间节点不需要
        self.distance = [[dis[i][j] for i in range(10)] for j in range(10)]


    def savingsAlgorithms(self):
        for i in range(1, len(self.q)):
            self.Routes.append([i])

        usedValue = 0
        # 计算得到节约表
        for i in range(1, len(self.Routes) + 1):                                                 # 使用Sij = Ci0 + C0j - Cij计算节约度
            for j in range(1, len(self.Routes) + 1):
                if i == j:
                    pass
                else:
                    saving = (self.distance[i][0] + self.distance[0][j]) - self.distance[i][j]

                    self.savings.append([i, j, round(saving, 4)])                                          # 将结果以元组形式存放在列表中
        # print(self.savings)
        self.savings = sorted(self.savings, key=itemgetter(2), reverse=True)
        # 按照节约度从大到小进行排序

        print(len(self.savings))
        # for i in range(len(self.savings)):
        #     print(self.savings[i][0],'--',self.savings[i][1], "  ",self.savings[i][2])           # 打印节约度
        for ii, save in enumerate(self.savings):
            print(self.dot_map[save[0]], '--', self.dot_map[save[1]], "  ", save[2])  # 打印节约度

        for i in range(len(self.savings)):
            startRoute = []
            endRoute = []
            routeDemand = 0
            routeVolume = 0
            # 更新路线过程
            for j in range(len(self.Routes)):
                # 目前最大节约值的起点i是否该点j路线上，则j路线则加入路线，相互换位置不影响，因为后面我们都删除再插入了
                if self.savings[i][0] == self.Routes[j][-1]:
                    endRoute = self.Routes[j]
                elif self.savings[i][1] == self.Routes[j][0]:
                    startRoute = self.Routes[j]

                # 如果已经有起点路线和end路线
                if startRoute and endRoute:
                    # 把路线的需求量相加
                    usedValue += 1

                    print(i, startRoute, endRoute)
                    for k in range(len(startRoute)):
                        routeDemand += self.q[startRoute[k]]
                        routeVolume += self.v[startRoute[k]]
                    for k in range(len(endRoute)):
                        routeDemand += self.q[endRoute[k]]
                        routeVolume += self.v[endRoute[k]]
                    routeDistance = 0
                    routestore = [0]+endRoute+startRoute+[0]

                    # 从p0开始 将该路线距离加进来 最后返回到p0
                    for ii in range(len(routestore) - 1):
                        # print(routestore[i],routestore[i+1])
                        # print(self.distance[routestore[i]][routestore[i+1]])
                        routeDistance += self.distance[routestore[ii]][routestore[ii+1]]

                    #print(routestore,"== ==:",routeDistance)

                    # 满足容量、体积和行驶距离的限制对路线进行更改
                    if (routeDemand <= self.tons) \
                        and (routeVolume <= self.vols) \
                        and (routeDistance <= self.distanceLimit):

                        self.Routes.remove(startRoute)
                        self.Routes.remove(endRoute)
                        self.Routes.append(endRoute + startRoute)
                        print('  合并：', [self.dot_map[dot] for dot in endRoute + startRoute])
                    break

            print('第{}个节约值未被使用'.format(i))

        for i in range(len(self.Routes)):
            self.Routes[i].insert(0, 0)
            self.Routes[i].insert(len(self.Routes[i]), 0)
        print('节约法总共计算了{}个节约值，其中有{}个被使用， 使用率为{}'.format(len(self.savings)/2, usedValue, usedValue/len(self.savings) * 2))


    def printRoutes(self):
        k = 1
        for i in self.Routes:
            costs = 0
            for j in range(len(i)-1):
                costs += self.distance[i[j]][i[j+1]]
            # print("路线:  ",i,"  路程:  ",costs)
            print("路线{}: {}  路程: {}".format(k, ' ==> '.join([self.dot_map[dot] for dot in i]), costs))
            k += 1


    def calcCosts(self):
        for i in range(len(self.Routes)):
            for j in range(len(self.Routes[i]) - 1):
                self.Cost += self.distance[self.Routes[i][j]][self.Routes[i][j + 1]]

        print("\nTotal Distance: ", round(self.Cost, 3))


    def start(self):
        print("== == == == == == == == == == == == == == == 导入数据 == == == == == == == = == == == == == == == =")
        self.distanceCalculate()
        print("== == == 距离表 == == ==")
        for i in self.distance:
            print(i)
        print("== == == 需求表 == == ==")
        print(self.q)
        print("== == == 限制条件 == == ==")
        print("车辆最大载重：", self.tons)
        print("车辆最大容量：", self.vols)
        print("车辆最长运输距离：", self.distanceLimit)
        print("== == == == == == == == == == == == == == == 节约度 == == == == == == == = == == == == == == == =")
        self.savingsAlgorithms()          # 函数调用计算节省量并生成路线
        print("== == == == == == == == == == == == == == == 结果 == == == == == == == = == == == == == == == =\n")
        self.printRoutes()
        self.calcCosts()
        self.distanceCalculate()
