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

class Cube:
    def __init__(self, initNode):
        self.initialNode = Node(initNode)
        print("Cube:")

    def initialState(self):
        return self.initialNode

    def actions(self, node):
        return [Action.T, Action.TC, Action.F, Action.FC, Action.R, Action.RC]

    def result(self, node, action):
        if action == Action.F:
            return self._f(node)
        elif action == Action.FC:
            return self._fc(node)
        elif action == Action.T:
            return self._t(node)
        elif action == Action.TC:
            return self._tc(node)
        elif action == Action.R:
            return self._r(node)
        elif action == Action.RC:
            return self._rc(node)

    def isGoal(self, node):
        if(node.state[0:4] == [node.state[0]]*4) and (node.state[4:8] == [node.state[4]]*4) and (node.state[8:12] == [node.state[8]]*4) and (node.state[12:16] == [node.state[12]]*4) and (node.state[16:20] == [node.state[16]]*4) and (node.state[20:24] == [node.state[20]]*4):
            return True
        return False

    def cost(self, node, action):
        return 1 #not used

    def h(self, node):
        return 1 #not used
    
    def _f(self, node):
        inp = node.state
        f = inp.copy()
        f[3] = inp[17]
        f[2] = inp[19]
        f[20] = inp[2]
        f[22] = inp[3]
        f[9] = inp[20]
        f[8] = inp[22]
        f[19] = inp[9]
        f[17] = inp[8]
        f[4] = inp[6]
        f[5] = inp[4]
        f[7] = inp[5]
        f[6] = inp[7]
        return Node(f)

    def _fc(self, node):
        inp = node.state
        fc = inp.copy()
        fc[2] = inp[20]
        fc[3] = inp[22]
        fc[17] = inp[3]
        fc[19] = inp[2]
        fc[8] = inp[17]
        fc[9] = inp[19]
        fc[22] = inp[8]
        fc[20] = inp[9]
        fc[4] = inp[5]
        fc[5] = inp[7]
        fc[7] = inp[6]
        fc[6] = inp[4]
        return Node(fc)
    
    def _t(self, node):
        inp = node.state
        t = inp.copy()
        t[21] = inp[14]
        t[20] = inp[15]
        t[5] = inp[21]
        t[4] = inp[20]
        t[17] = inp[5]
        t[16] = inp[4]
        t[14] = inp[17]
        t[15] = inp[16]
        t[0] = inp[2]
        t[1] = inp[0]
        t[3] = inp[1]
        t[2] = inp[3]
        return Node(t)

    def _tc(self, node):
        inp = node.state
        tc = inp.copy()
        tc[14] = inp[21]
        tc[15] = inp[21]
        tc[21] = inp[5]
        tc[20] = inp[4]
        tc[5] = inp[17]
        tc[4] = inp[16]
        tc[17] = inp[14]
        tc[16] = inp[15]
        tc[2] = inp[0]
        tc[0] = inp[1]
        tc[1] = inp[3]
        tc[3] = inp[2]
        return Node(tc)

    def _r(self, node):
        inp = node.state
        r = inp.copy()
        r[3] = inp[7]
        r[1] = inp[5]
        r[15] = inp[3]
        r[13] = inp[1]
        r[11] = inp[15]
        r[9] = inp[13]
        r[7] = inp[11]
        r[5] = inp[9]
        r[20] = inp[22]
        r[22] = inp[23]
        r[23] = inp[21]
        r[21] = inp[20]
        return Node(r)

    def _rc(self, node):
        inp = node.state
        rc = inp.copy()
        rc[7] = inp[3]
        rc[5] = inp[1]
        rc[3] = inp[15]
        rc[1] = inp[13]
        rc[15] = inp[11]
        rc[13] = inp[9]
        rc[11] = inp[7]
        rc[9] = inp[5]
        rc[22] = inp[20]
        rc[23] = inp[22]
        rc[21] = inp[23]
        rc[20] = inp[21]
        return Node(rc)

class Action(Enum):
    T = 1
    TC = 2
    F = 3
    FC = 4
    R = 5
    RC = 6
    def invert(self):
        return {
            Action.T : Action.TC,
            Action.TC : Action.T,
            Action.F : Action.FC,
            Action.FC : Action.F,
            Action.R : Action.RC,
            Action.RC : Action.R,
        }[self]

inp = input()
inp = inp.split()


cube = Cube(inp)
alg = GraphAlgo(cube)
# alg.uniformCostSrearch()
alg.depthLimitedSearch(14)


# inp = ['g', 'g', 'g', 'g', 'o', 'o', 'o', 'o', 'b', 'b', 'b', 'b', 'r', 'r', 'r', 'r', 'w', 'w', 'w', 'w', 'y', 'y', 'y', 'y']
# o y o o g w r r b b r g g y g b w y w y b o w r 



