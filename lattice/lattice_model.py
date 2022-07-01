from abc import abstractmethod
from itertools import chain

from util import wtv


class VertexInterface:
    @abstractmethod
    def get_all(self):
        pass

    def can_realize(self, vert):
        values = self.get_all()
        other_values = vert.get_all()
        for i in range(4):
            if values[i] != 0 and values[i] != other_values[i]:
                return False
        return True


class Vertex(VertexInterface):
    def __init__(self, values_word, weight):
        self.values = wtv(values_word)
        # should be lambda of row/col
        self.weight = weight

    def get_all(self):
        return self.values


class LatticeModel:
    def __init__(self, rows, cols, admissible_vertices):
        self.rows = rows
        self.cols = cols
        self.offset = 2 * self.cols + 1
        self.values_length = self.offset * self.rows + self.cols
        self.verts = admissible_vertices

    def boundary_indices(self):
        top = (index_in_lattice(0, c, TOP, self) for c in range(self.cols))
        right = (index_in_lattice(r, self.cols-1, RIGHT, self) for r in range(self.rows))
        bottom = (index_in_lattice(self.rows-1, self.cols-1-c, BOTTOM, self) for c in range(self.cols))
        left = (index_in_lattice(self.rows-1-r, 0, LEFT, self) for r in range(self.rows))
        return chain(top, right, bottom, left)

    def adjacent_vertices(self, i):
        adj = []
        row = i//self.offset
        rem = i % self.offset
        if rem < self.cols:
            col = rem
            if row > 0:
                adj.append((row-1, col))
            if row < self.rows-1:
                adj.append((row, col))
        else:
            col = rem - self.cols
            if col > 0:
                adj.append((row, col-1))
            if col < self.cols:
                adj.append((row, col))
        return adj


def index_in_lattice(r, c, direction, latmod: LatticeModel):
    if direction == BOTTOM:
        return latmod.offset * (r + 1) + c
    elif direction == LEFT:
        return latmod.offset * r + latmod.cols + c
    elif direction == RIGHT:
        return latmod.offset * r + latmod.cols + c + 1
    elif direction == TOP:
        return latmod.offset * r + c


TOP = 0
RIGHT = 1
BOTTOM = 2
LEFT = 3
