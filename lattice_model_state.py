import io
from itertools import product

from lattice_model import index_in_lattice, LatticeModel


symbol_dict = dict([(-1, "⊖"), (0, "?"), (1, "⊕")])
tikz_dict = dict([(-1, "-"), (0, " "), (1, "+")])


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
            # sol.print()
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

    def write_tikz(self, out):
        out.write(
"""
\\begin{tikzpicture}
"""
        )
        for r in range(self.latmod.rows):
            for c in range(self.latmod.cols):
                v = self.get_vertex(r, c)
                out.write(
                    "\\vertex{{ {} }}{{ {} }}{{ ${}$ }}{{ ${}$ }}{{ ${}$ }}{{ ${}$ }}\n"
                    .format(c, -r, *[tikz_dict[v.get(i)] for i in range(4)])
                )
        out.write(
"""
\\end{tikzpicture}
"""
        )
