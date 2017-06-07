"""Google FooBar Prepare the Bunnies Escape Challenge
Find the shortest path through a maze, you can remove one obstacle.

input = [[0, 1, 1, 0],
         [0, 0, 0, 1],
         [1, 1, 0, 0],
         [1, 1, 1, 0]]

output = 7

"""
import collections
import pdb

actions = [[-1, 0],  # Up
           [1, 0],   # Down
           [0, 1],   # Left
           [0, -1]]  # Right

class Node(object):
    def __init__(self, loc, depth = 0, bar_removed = False):
        self.loc = loc
        self.depth = depth
        self.bar_removed = bar_removed
        self.children = None

    def __id(self):
        return (self.loc, self.depth, self.bar_removed)
    
    def __repr__(self):
        return str(self.__id())
    
    def __eq__(self, other):
        return self.__id() == other.__id()

    def __hash__(self):
        return hash(self.__id())

class Frontier(object):
    def __init__(self, nodes=None, node_set=None):
        self.nodes = nodes or collections.deque([])
        self.node_set = node_set or set()

    def get_children(self, maze, node):
        valid_moves = []
        row, col = node.loc
        for i in range(len(actions)):
            row2 = row + actions[i][0]
            col2 = col + actions[i][1]
            #pdb.set_trace()
            if row2 >= 0 and row2 < len(maze) and col2 >= 0 and col2 < len(maze[0]):
                if maze[row2][col2] == 0:
                    child = Node((row2, col2), node.depth+1, node.bar_removed)
                    valid_moves.append(child)
                elif maze[row2][col2] == 1 and not node.bar_removed:
                    child = Node((row2, col2), node.depth+1, True)
                    valid_moves.append(child)
        return valid_moves
    
    # adds a new board state to the frontier
    def add_node(self, maze, node):
        self.nodes.append(node)
        self.node_set.add(node)
        node.children = self.get_children(maze, node)

    def __repr__(self):
        return self.nodes     

def answer(maze):
    frontier = Frontier()
    start = Node((0, 0))
    goal = (len(maze) - 1, len(maze[0]) - 1)
    visited = set()

    frontier.add_node(maze, start)

    while frontier.nodes:
        state = frontier.nodes.popleft()
        #pdb.set_trace()
        visited.add(state)
        if state.loc == goal:
            return state.depth + 1
        else:
            for i in range(len(state.children)):
                if not state.children[i].loc in visited and not state.children[i] in frontier.node_set:
                    frontier.add_node(maze, state.children[i])



def test1():
    return [[0, 1, 1, 0],
         [0, 0, 0, 1],
         [1, 1, 0, 0],
         [1, 1, 1, 0]]

def test2():
    return [[0,0,0,0,0,0],
            [1,1,1,1,1,0],
            [0,0,0,0,0,0],
            [0,1,1,1,1,1],
            [0,1,1,1,1,1],
            [0,0,0,0,0,0]]

def test3():
    return [[0,0,0,0,0,0],
            [1,1,1,1,0,0],
            [1,1,1,0,0,0],
            [0,0,0,0,1,1],
            [0,1,1,1,1,1],
            [0,0,0,0,0,0]]
# 13
def test4():
    return [[0,1],
            [1,0]]

def test5():
    return [[0,0,0,0,0,0],
            [0,1,1,1,0,0],
            [1,1,1,0,0,0],
            [1,0,0,0,1,1],
            [0,0,1,1,1,1],
            [0,0,0,1,0,0]]
#17

def test6():
    return [[0,0,0,0,0,0],
            [1,1,1,1,1,1],
            [0,0,0,0,0,0]]

def test7():
    return [[0,1],
            [0,0],
            [0,0],
            [1,1],
            [1,0]]

def test8():
    return [
 [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
 [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
 [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
 [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  
 [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
 [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], 
 [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], 
 [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], 
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], 
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
 [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
 ]

def test9():
    return [[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
              [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
              [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

def test10():
    return [[0,0,0,0,0],
            [0,0,1,0,1],
            [0,0,0,0,1],
            [0,0,1,1,1],
            [0,1,1,0,1],
            [0,0,0,0,1],
            [0,0,1,0,0]]

tests = [test1(), test2(), test3(), test4(), test5(), test6(), test7(), test8(), test9(), test10()]
for t in tests:
    print answer(t)

print answer(test2())