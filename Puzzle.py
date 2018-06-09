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

class Puzzle:
    def __init__(self, initNode):
        self.initialNode = Node(initNode)
        print("Puzzle:")

    def initialState(self):
        return self.initialNode

    def actions(self, node):
        return {
            0 : [Action.U, Action.L],
            1 : [Action.U, Action.L, Action.R],
            2 : [Action.U, Action.R],
            3 : [Action.U, Action.L, Action.D],
            4 : [Action.U, Action.L, Action.D, Action.R],
            5 : [Action.U, Action.R, Action.D],
            6 : [Action.D, Action.L],
            7 : [Action.D, Action.L, Action.D],
            8 : [Action.D, Action.R],
        }[node.state.index('0')]

    def result(self, node, action):
        if action == Action.L:
            return self._left(node)
        elif action == Action.R:
            return self._right(node)
        elif action == Action.U:
            return self._up(node)
        elif action == Action.D:
            return self._down(node)

    def isGoal(self, node):
        if(node.state == '012345678'):
            return True
        return False

    def cost(self, node, action):
        return 1

    def h(self, node):
        return #what is tabe shohoodi fasele mostaghim???
    
    def _up(self, node):
        s = node.state
        ls = list(s)
        ls[s.index('0')] = ls[s.index('0') + 3]
        ls[s.index('0') + 3] = '0'
        return Node(''.join(ls))

    def _down(self, node):
        s = node.state
        ls = list(s)
        ls[s.index('0')] = ls[s.index('0') - 3]
        ls[s.index('0') - 3] = '0'
        return Node(''.join(ls))

    def _left(self, node):
        s = node.state
        ls = list(s)
        ls[s.index('0')] = ls[s.index('0') + 1]
        ls[s.index('0') + 1] = '0'
        return Node(''.join(ls))
    
    def _right(self, node):
        s = node.state
        ls = list(s)
        ls[s.index('0')] = ls[s.index('0') - 1]
        ls[s.index('0') - 1] = '0'
        return Node(''.join(ls))

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

inp = input().split()
inp += input().split()
inp += input().split()
inp = ''.join(inp)

puzzle = Puzzle(inp)
alg = GraphAlgo(puzzle)
alg.uniformCostSrearch()



