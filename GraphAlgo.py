from queue import Queue
import heapq

class GraphAlgo:
    def __init__(self, problem):
        self.f = Queue()
        self.f.put(problem.initialState())
        self.e = []
        self.problem = problem
        self.pathCost = 0
        self.maxMemoryUsage = 0
        self.seenNodes = 0
        self.expandedNodes = 0
        self._depth = 0


    def showResult(self, start, pathCostNotCalculate=False, bidirectionalNode=None):#bidirectionalNode is for bidirectionalSearch
        path = []
        actions = []
        while start.parent != None:
            path.append(start.state)
            actions.append(start.parent['action'])
            start = start.parent['node']
        path.append(start.state)
        path.reverse()
        actions.reverse()
        if bidirectionalNode:
            del path[-1]
            while bidirectionalNode.parent != None:
                path.append(bidirectionalNode.state)
                actions.append(bidirectionalNode.parent['action'].invert())
                bidirectionalNode = bidirectionalNode.parent['node']
            path.append(bidirectionalNode.state)
        print('actions: ', actions)
        print('path: ', path)
        print('seen nodes: ', self.seenNodes)
        print('expanded nodes: ', self.expandedNodes)
        print('max memory usage: ', self.maxMemoryUsage)
        if pathCostNotCalculate:
            print('path cost: ', len(path))
        else:
            print('path cost: ', self.pathCost)
        

    def BFS(self):
        while True:
            if len(self.f.queue) == 0:
                print('f is empty!!!')
                return
            node = self.f.get()
            self.e.append(node)
            for action in self.problem.actions(node):
                child = self.problem.result(node, action)
                child.parent = {'node': node, 'action': action}
                if child.state not in [x.state for x in self.f.queue] and child.state not in [x.state for x in self.e]:
                    if self.problem.isGoal(child):
                        self.seenNodes = self.f.qsize() + len(self.e) + 1
                        self.expandedNodes = len(self.e)
                        self.maxMemoryUsage = self.f.qsize() + len(self.e)
                        self.showResult(child, True)
                        return
                    else:
                        self.f.put(child)

    def DFS(self):
        if not self.recursivDFS(self.f.get()):
            print('not found!!!')

    def recursivDFS(self, node):
        self.seenNodes += 1
        self._depth += 1
        self.maxMemoryUsage = max(self.maxMemoryUsage, self._depth)
        if self.problem.isGoal(node):
            self.pathCost = self._depth
            self.showResult(node)
            return True
        else:
            for action in self.problem.actions(node):
                child = self.problem.result(node, action)
                child.parent = {'node': node, 'action': action}
                result = self.recursivDFS(child)
                if result:
                    return True
            self._depth -= 1
            self.expandedNodes += 1
            return False

    def DFSGraphSearch(self):
        self.f = []
        self.f.append(self.problem.initialState())
        while True:
            if len(self.f) == 0:
                print('f is empty!!!')
                return
            node = self.f.pop()
            self.e.append(node)
            for action in self.problem.actions(node):
                child = self.problem.result(node, action)
                child.parent = {'node': node, 'action': action}
                if child.state not in [x.state for x in self.f] and child.state not in [x.state for x in self.e]:
                    if self.problem.isGoal(child):
                        self.seenNodes = len(self.f) + len(self.e) + 1
                        self.expandedNodes = len(self.e)
                        self.maxMemoryUsage = len(self.f) + len(self.e)
                        self.showResult(child, True)
                        return
                    else:
                        self.f.append(child)


    def depthLimitedSearch(self, limit): #DFS with Depth-Limited-Search
        if not self.recursivDLS(self.f.get(), limit):
            print('not found!!!')

    def recursivDLS(self, node, limit):
        limit -= 1
        self.seenNodes += 1
        self._depth += 1
        self.maxMemoryUsage = max(self.maxMemoryUsage, self._depth)
        if self.problem.isGoal(node):
            self.pathCost = self._depth
            self.showResult(node)
            return True
        elif limit == 0:
            self._depth -= 1
            return False
        else:
            for action in self.problem.actions(node):
                child = self.problem.result(node, action)
                child.parent = {'node': node, 'action': action}
                result = self.recursivDLS(child, limit)
                if result:
                    return True
            self._depth -= 1
            self.expandedNodes += 1
            return False


    def iterativeDeepeningSearch(self):
        limit = 0
        node = self.f.get()
        while self.maxMemoryUsage >= limit:
            limit += 1
            if self.recursivDLS(node, limit):
                return
            self._depth = 0



    def bidirectionalSearch(self, goal):
        g = Queue()
        g.put(goal)
        h = []
        while True:
            if len(self.f.queue) == 0:
                print('f is empty!!!')
                return
            if len(g.queue) == 0:
                print('g is empty!!!')
                return
            subscribe = next((node.state for node in self.f.queue if node.state in [node.state for node in g.queue]), None)
            if(subscribe):
                self.seenNodes = self.f.qsize() + len(self.e) + g.qsize() + len(h) 
                self.expandedNodes = len(self.e) + len(h)
                self.maxMemoryUsage = self.f.qsize() + len(self.e) + g.qsize() + len(h)
                self.showResult(next(node for node in self.f.queue if node.state == subscribe),True ,next(node for node in g.queue if node.state == subscribe))
                return

            node1 = self.f.get()
            self.e.append(node1)
            for action in self.problem.actions(node1):
                child1 = self.problem.result(node1, action)
                child1.parent = {'node': node1, 'action': action}
                if child1.state not in [x.state for x in self.f.queue] and child1.state not in [x.state for x in self.e]:
                    self.f.put(child1)

            subscribe = next((node.state for node in self.f.queue if node.state in [node.state for node in g.queue]), None)
            if(subscribe):
                self.seenNodes = self.f.qsize() + len(self.e) + g.qsize() + len(h) 
                self.expandedNodes = len(self.e) + len(h)
                self.maxMemoryUsage = self.f.qsize() + len(self.e) + g.qsize() + len(h)
                self.showResult(next(node for node in self.f.queue if node.state == subscribe),True ,next(node for node in g.queue if node.state == subscribe))
                return
            
            node2 = g.get()
            h.append(node2)
            for action in self.problem.actions(node2):
                child2 = self.problem.result(node2, action)
                child2.parent = {'node': node2, 'action': action}
                if child2.state not in [x.state for x in g.queue] and child2.state not in [x.state for x in h]:
                    g.put(child2)


    def uniformCostSrearch(self):
        self.f = []
        heapq.heappush(self.f, (0, self.problem.initialState()))
        while True:
            if not self.f:
                print("f is empty!!!")
                return
            myTuple = heapq.heappop(self.f)
            node = myTuple[1]
            nodePathCost = myTuple[0]
            if self.problem.isGoal(node):
                self.seenNodes = len(self.f) + len(self.e) + 1
                self.expandedNodes = len(self.e)
                self.maxMemoryUsage = len(self.f) + len(self.e) + 1
                self.pathCost = nodePathCost
                self.showResult(node)
                return

            self.e.append(node)
            for action in self.problem.actions(node):
                child = self.problem.result(node, action)
                pathCost = nodePathCost + self.problem.cost(node, action)
                child.parent = {'node': node, 'action': action}
                if ( child.state not in [x[1].state for x in self.f] ) and ( child.state not in [x.state for x in self.e] ):
                    heapq.heappush(self.f, (pathCost, child))
                else:
                    temp = next((x for x in self.f if (x[1].state == child.state and x[0] > pathCost)), None)
                    if temp:
                        self.f.remove(temp)
                        heapq.heappush(self.f, (pathCost, child))

    def AStar(self):
        self.f = []
        heapq.heappush(self.f, (self.problem.h(self.problem.initialState()), self.problem.initialState()))
        while True:
            if not self.f:
                print("f is empty!!!")
                return
            myTuple = heapq.heappop(self.f)
            node = myTuple[1]
            nodePathCost = myTuple[0]
            if self.problem.isGoal(node):
                self.seenNodes = len(self.f) + len(self.e) + 1
                self.expandedNodes = len(self.e)
                self.maxMemoryUsage = len(self.f) + len(self.e) + 1
                self.pathCost = nodePathCost - self.problem.h(node)
                self.showResult(node)
                return

            self.e.append(node)
            for action in self.problem.actions(node):
                child = self.problem.result(node, action)
                pathCost = nodePathCost - self.problem.h(node) + self.problem.cost(node, action) + self.problem.h(child)
                child.parent = {'node': node, 'action': action}
                if ( child.state not in [x[1].state for x in self.f] ) and ( child.state not in [x.state for x in self.e] ):
                    heapq.heappush(self.f, (pathCost, child))
                else:
                    temp = next((x for x in self.f if (x[1].state == child.state and x[0] > pathCost)), None)
                    if temp:
                        self.f.remove(temp)
                        heapq.heappush(self.f, (pathCost, child))


