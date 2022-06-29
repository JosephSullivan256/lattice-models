
from itertools import chain
from itertools import product
import io
from sympy import symbols


TOP = 0
RIGHT = 1
BOTTOM = 2
LEFT = 3


class Vertex:
    def __init__(self, values_word, weight):
        self.values = wtv(values_word)
        # should be lambda of row/col
        self.weight = weight


class LatticeModel:
    def __init__(self, rows, cols, admissible_vertices):
        self.rows = rows
        self.cols = cols
        self.offset = 2 * self.cols + 1
        self.verts = admissible_vertices

    def boundary_indices(self):
        top = (index_in_lattice(0, c, TOP, self) for c in range(self.cols))
        right = (index_in_lattice(r, self.cols-1, RIGHT, self) for r in range(self.rows))
        bottom = (index_in_lattice(self.rows-1, self.cols-1-c, BOTTOM, self) for c in range(self.cols))
        left = (index_in_lattice(self.rows-1-r, 0, LEFT, self) for r in range(self.rows))
        return chain(top, right, bottom, left)


def index_in_lattice(r, c, direction, latmod: LatticeModel):
    if direction == BOTTOM:
        return latmod.offset * (r + 1) + c
    elif direction == LEFT:
        return latmod.offset * r + latmod.cols + c
    elif direction == RIGHT:
        return latmod.offset * r + latmod.cols + c + 1
    elif direction == TOP:
        return latmod.offset * r + c


class StateVertex:
    def __init__(self, row, col, state):
        self.r = row
        self.c = col
        self.state = state

    def set(self, direction, value):
        self.state.values[index_in_lattice(self.r, self.c, direction, self.state.latmod)] = value

    def get(self, direction):
        return self.state.values[index_in_lattice(self.r, self.c, direction, self.state.latmod)]

    def get_all(self):
        return [self.get(i) for i in range(4)]


class LatticeModelState:
    def __init__(self, latmod: LatticeModel):
        self.latmod = latmod

        values_length = self.latmod.offset * self.latmod.rows + self.latmod.cols
        self.values = [0 for i in range(values_length)]

    def get_vertex(self, r, c):
        return StateVertex(r, c, self)

    def set_boundary(self, values):
        for (i, value) in zip(self.latmod.boundary_indices(), values):
            self.values[i] = value

    def is_valid(self):
        for r in range(self.latmod.rows):
            for c in range(self.latmod.cols):
                bad = True
                current = self.get_vertex(r, c).get_all()
                for v in self.latmod.verts:
                    if current == v.values:
                        bad = False
                        break
                if bad:
                    return False
        return True

    def iter_vertices(self):
        for r in range(self.latmod.rows):
            for c in range(self.latmod.cols):
                yield self.get_vertex(r, c)

    # only makes sense if all values are set
    def compute_weight(self):
        product = 1
        for r in range(self.latmod.rows):
            for c in range(self.latmod.cols):
                current = self.get_vertex(r, c).get_all()
                for v in self.latmod.verts:
                    if current == v.values:
                        product *= v.weight(r, c)
        return product

    def compute_partition_function(self):
        sum = 0
        for sol in self.iter_solutions():
            weight = sol.compute_weight()
            sol.print()
            print(weight)
            sum += weight
        return sum

    def iter_solutions(self):
        unset_indices = []
        for (i, val) in enumerate(self.values):
            if val == 0:
                unset_indices.append(i)

        copy = LatticeModelState(self.latmod)
        copy.values = self.values.copy()

        for values in product([-1, 1], repeat=len(unset_indices)):
            for (i, val) in enumerate(values):
                copy.values[unset_indices[i]] = val
            if copy.is_valid():
                yield copy

    def print(self):
        out = io.StringIO()
        for r in range(self.latmod.rows):
            for c in range(self.latmod.cols):
                out.write(" ")
                out.write(symbol_dict[self.values[self.latmod.offset * r + c]])
            out.write("\n")
            for c in range(self.latmod.cols):
                out.write(symbol_dict[self.values[self.latmod.offset * r + self.latmod.cols + c]])
                out.write("+")
            out.write(symbol_dict[self.values[self.latmod.offset * r + self.latmod.cols*2]])
            out.write("\n")
        for c in range(self.latmod.cols):
            out.write(" ")
            out.write(symbol_dict[self.values[self.latmod.offset * self.latmod.rows + c]])
        out.write("\n")
        print(out.getvalue())
        out.close()


value_dict = {
    "+": 1,
    "-": -1,
    " ": 0
}

symbol_dict = dict([(-1, "⊖"), (0, "?"), (1, "⊕")])


# word to values
def wtv(word):
    return [value_dict[c] for c in list(word)]


if __name__ == '__main__':
    latmod = LatticeModel(3, 3, [
        Vertex("++++", lambda r, c: 1),
        Vertex("----", lambda r, c: 0),
        Vertex("-+-+", lambda r, c: 1),
        Vertex("+-+-", lambda r, c: symbols('z' + str(r + 1))),
        Vertex("++--", lambda r, c: symbols('z' + str(r + 1))),
        Vertex("--++", lambda r, c: 1)
    ])
    state = LatticeModelState(latmod)
    state.set_boundary(wtv("-+++++-+++++"))
    state.print()
    print(state.compute_partition_function())
