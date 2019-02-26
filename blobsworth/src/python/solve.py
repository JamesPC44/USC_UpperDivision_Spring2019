#!/usr/bin/python3

# Created by William Edwards, 2018-10-25

"""
Solution to the Blobsworth problem for the Fall 2018
ACM codeathon 240/350 division.
"""

import heapq
from pdb import set_trace
from collections import defaultdict

# Constants
SLIDE_COST = 1
STRETCH_COST = 2

# First we'll create some useful helper classes
class PriorityQueue(object):
    class Entry(object):
        def __init__(self, value, priority):
            self._val = value
            self._pri = priority

        def __getitem__(self, i):
            if i == 0:
                return self._pri
            if i == 1:
                return self._val
            raise IndexError()

        def __setitem__(self, i, val):
            if i == 0:
                self._pri = val
            elif i == 1:
                self._val = val
            else:
                raise IndexError()

        def __lt__(self, other):
            return self._pri < other._pri

    def __init__(self):
        self._heap = []
        self._entrymap = {}
        self._DELETED = "<deleted>"

    def __bool__(self):
        self._pop_deleted()
        return len(self._heap) > 0
    
    def __contains__(self,  item):
        return item in self._entrymap

    def __iter__(self):
        for entry in self._heap:
            if entry[1] != self._DELETED:
                yield entry[1]

    def _pop_deleted(self):
        while len(self._heap) > 0 and self._heap[0][1] == self._DELETED:
            heapq.heappop(self._heap)

    def push(self, item, priority):
        entry = PriorityQueue.Entry(item, priority)
        self._entrymap[item] = entry
        heapq.heappush(self._heap, entry)

    def pop(self):
        self._pop_deleted()
        if len(self._heap) == 0:
            return None
        entry = heapq.heappop(self._heap)
        item = entry[1]
        del self._entrymap[item]
        return item

    def peek(self):
        self._pop_deleted()
        if len(self._heap) == 0:
            return None
        return self._heap[0][1]

    def update(self, item, new_priority):
        entry = self._entrymap[item]
        entry[1] = self._DELETED
        del self._entrymap[item]
        self.push(item, new_priority)

    def push_update(self, item, priority):
        if item in self:
            self.update(item, priority)
        else:
            self.push(item, priority)

class Node(object):
    def __init__(self, cells, heuristic=None):
        """
        Construct a new instance of a node. Cells is a set
        of tuples (row, col).
        """
        self.cells = cells
        self.g = float("inf")
        self.f = float("inf")
        self.bp = None
        if heuristic is None:
            self.h = 0
        else:
            self.h = heuristic(self)

class NodeDict(object):
    def __init__(self, heuristic=None):
        self._nodes = dict()
        if heuristic is None:
            self._heuristic = lambda x: 0
        else:
            self._heuristic = heuristic

    def __getitem__(self, cells):
        if cells in self._nodes:
            return self._nodes[cells]
        else:
            node = Node(cells, self._heuristic)
            self._nodes[cells] = node
            return node

class World(object):
    EMPTY = 0
    OBSTACLE = 1
    GOAL = 2

    def __init__(self, grid):
        """
        grid: two dimensional list of values taken from {EMPTY, OBSTACLE, GOAL}
        representing the grid of the world.
        """
        self._grid = grid
        self._row_bound = len(grid)
        self._col_bound = len(grid[0])

    def collides(self, cells):
        """
        Checks to see whether a set of cells collides with any obstacles or the
        boundaries of the grid.
        """
        for row, col in cells:
            if row < 0:
                return True
            if col < 0:
                return True
            if row >= self._row_bound:
                return True
            if col >= self._col_bound:
                return True
            if self._grid[row][col] == World.OBSTACLE:
                return True
        return False

    def has_goal(self, cells):
        for row, col in cells:
            if self._grid[row][col] == World.GOAL:
                return True
        return False

def get_adjacent_cells(cell):
    try:
        row, col = cell
    except TypeError:
        print(cell)
    return [(row+1, col), (row-1, col), (row, col+1), (row, col-1)]

# Heuristic Computation
def compute_heuristic(world):
    open_ = PriorityQueue()
    g_vals = defaultdict(lambda: float("inf"))
    # Add goal nodes
    for row, grid_row in enumerate(world._grid):
        for col, contents in enumerate(grid_row):
            if contents == World.GOAL:
                open_.push((row, col), 0)
                g_vals[(row, col)] = 0
    while open_:
        current = open_.pop()
        if current == None:
            print(open_._heap)
            print(bool(open))
        for adj in get_adjacent_cells(current):
            row, col = adj
            if row < 0 or row >= world._row_bound:
                continue
            if col < 0 or col >= world._col_bound:
                continue
            if world._grid[row][col] == World.OBSTACLE:
                continue
            if g_vals[current] + 1 < g_vals[adj]:
                g_vals[adj] = g_vals[current] + 1
                open_.push_update(adj, g_vals[adj])


    def heuristic(node):
        heur = float("inf")
        for cell in node.cells:
            if g_vals[cell] < heur:
                heur = g_vals[cell]
        return heur
    return heuristic

def are_cells_connected(cells):
    """
    Determines whether a set of cells are connected.
    """
    component = set()
    to_expand = set([cells.__iter__().__next__()]) # Initialize set with arbitrary element of cells
    while to_expand:
        current_cell = to_expand.pop()
        component.add(current_cell)
        for neighbor in get_adjacent_cells(current_cell):
            if neighbor in cells and not neighbor in component:
                to_expand.add(neighbor)

    return not bool(component ^ cells)

def get_neighbors(cells):
    neighbors = set()
    for cell in cells:
        for adj in get_adjacent_cells(cell):
            neighbors.add(adj)
    return neighbors

def get_rearrangements(cells):
    rearrangements = set()
    for cell in cells:
        for neighbor in get_neighbors(cells):
            if neighbor in cells:
                continue
            for swap_cell in cells:
                temp_rearr = set(cells)
                temp_rearr.remove(swap_cell)
                temp_rearr.add(neighbor)
                if are_cells_connected(temp_rearr):
                    rearrangements.add(frozenset(temp_rearr))
    return rearrangements

def get_translations(cells):
    translations = set()
    for rowoff, coloff in [(1,0),(-1,0),(0,1),(0,-1)]:
        trans = set()
        for row, col in cells:
            trans.add((row + rowoff, col + coloff))
        translations.add(frozenset(trans))

    return translations

def get_successors(node, nodes, world):
    successors = []
    for cells in get_rearrangements(node.cells):
        if not world.collides(cells):
            successors.append((STRETCH_COST, nodes[cells]))
    for cells in get_translations(node.cells):
        if not world.collides(cells):
            successors.append((SLIDE_COST, nodes[cells]))
    return successors

def expand_node(node, open_, nodes, world):
    successors = get_successors(node, nodes, world)
    for edge_cost, successor in successors:
        if successor.g > node.g + edge_cost:
            successor.g = node.g + edge_cost
            successor.f = successor.g + successor.h
            successor.bp = node
            open_.push_update(successor, successor.f)

def node_to_str(node, world):
    string = ""
    for row in range(0, world._row_bound):
        for col in range(0, world._row_bound):
            if (row, col) in node.cells:
                string += "B"
            elif world._grid[row][col] == World.EMPTY:
                string += "_"
            elif world._grid[row][col] == World.OBSTACLE:
                string += "*"
            elif world._grid[row][col] == World.GOAL:
                string += "G"
        string += "\n"
    return string

def draw_path(node, world):
    while not node is None:
        print("\n")
        print("g={}".format(node.g))
        print(node_to_str(node, world))
        node = node.bp

def solve(start_node, world):
    heuristic = compute_heuristic(world)
    nodes = NodeDict(heuristic=heuristic)
    open_ = PriorityQueue()
    closed = set()
    open_.push(start_node, start_node.f)
    
    while open_:
        current_node = open_.pop()
        if world.has_goal(current_node.cells):
            return current_node.g
        if current_node in closed:
            continue
        closed.add(current_node)
        expand_node(current_node, open_, nodes, world)

    return -1

def load_problem(dimension, blobsize, lines):
    """ str -> (World, Node)
    returns the world and starting node
    corresponding to the search string
    """
    grid = []
    cell_list = []
    for row, line in enumerate(lines):
        grid_row = []
        for col, char in enumerate(line):
            if char == "_":
                grid_row.append(World.EMPTY)
            elif char == "B":
                grid_row.append(World.EMPTY)
                cell_list.append((row, col))
            elif char == "*":
                grid_row.append(World.OBSTACLE)
            elif char == "G":
                grid_row.append(World.GOAL)
            else:
                raise ValueError("Unrecognized character in input grid: {}".format(repr(char)))
        grid.append(grid_row)

    # Sanity check inputs
    if len(grid) != dimension:
        raise ValueError("Wrong number of rows")
    for row in grid:
        if len(grid) != dimension:
            raise ValueError("Wrong number of cols")
    if len(cell_list) != blobsize:
        raise ValueError("Wrong number of blob bits")
    cells = frozenset(cell_list)
    if not are_cells_connected(cells):
        raise ValueError("Blob is not a blob")

    world = World(grid)
    start_node = Node(cells)
    start_node.g = 0
    start_node.f = start_node.h

    return world, start_node

def main():
    # Read problem from stdin
    dimension = int(input())
    blobsize = int(input())
    lines = [input() for i in range(dimension)]
    world, start_node = load_problem(dimension, blobsize, lines)
    solution = solve(start_node, world)
    print(solution)

if __name__ == "__main__":
    main()
