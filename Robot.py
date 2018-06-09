from GraphAlgo import GraphAlgo
from enum import Enum
from queue import Queue
import heapq

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
    def __gt__(self, other):
        return False

class Robot:
    def __init__(self, n, m, numOfWalls, walls):
        self.initialNode = Node([1, 1])
        self.n = n
        self.m = m
        self.numOfWalls = numOfWalls
        self.walls = walls
        print("Robot:")

    def initialState(self):
        return self.initialNode

    def actions(self, node):
        actions = []
        coordinate = node.state
        if coordinate[1] > 1 and (coordinate + [coordinate[0], coordinate[1] - 1]) not in self.walls and ([coordinate[0], coordinate[1] - 1] + coordinate) not in self.walls:
            actions.append(Action.U)
        if coordinate[0] > 1 and (coordinate + [coordinate[0] - 1, coordinate[1]]) not in self.walls and ([coordinate[0] - 1, coordinate[1]] + coordinate) not in self.walls:
            actions.append(Action.L)
        if coordinate[0] < self.n and (coordinate + [coordinate[0] + 1, coordinate[1]]) not in self.walls and ([coordinate[0] + 1, coordinate[1]] + coordinate) not in self.walls:
            actions.append(Action.R)
        if coordinate[1] < self.m and (coordinate + [coordinate[0], coordinate[1] + 1]) not in self.walls and ([coordinate[0], coordinate[1] + 1] + coordinate) not in self.walls:
            actions.append(Action.D)
        return actions


    def result(self, node, action):
        if action == Action.L:
            return Node([node.state[0] - 1, node.state[1]])
        elif action == Action.R:
            return Node([node.state[0] + 1, node.state[1]])
        elif action == Action.U:
            return Node([node.state[0], node.state[1] - 1])
        elif action == Action.D:
            return Node([node.state[0], node.state[1] + 1])

    def isGoal(self, node):
        if(node.state == [self.n, self.m]):
            return True
        return False

    def cost(self, node, action):
        return 1

    def h(self, node):
        return ((self.n - node.state[0])**2 + (self.m - node.state[1])**2)**0.5
    


class Action(Enum):
    L = 1
    R = 2
    U = 3
    D = 4
    def invert(self):
        return {
            Action.L : Action.R,
            Action.R : Action.L,
            Action.U : Action.D,
            Action.D : Action.U,
        }[self]



inp = input()

split = inp.split()
n = int(split[0])
m = int(split[1])

inp = input()
split = inp.split()
numOfWalls = int(split[0])

walls = []

for i in range(0, numOfWalls):
    inp = input()
    split = inp.split()
    walls.append([int(x) for x in split])

robot = Robot(n, m, numOfWalls, walls)
alg = GraphAlgo(robot)
alg.bidirectionalSearch(Node([m,m]))

'''
sample input:
5 5 
4
3 2 4 2
3 3 4 3
2 3 2 4
3 3 3 4

first line: dimention of enviroment
secend line: number of walls
for 1 to 4 
    walls between to square
'''
