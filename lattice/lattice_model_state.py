import io
from itertools import product

from lattice.lattice_model import index_in_lattice, LatticeModel, VertexInterface

symbol_dict = dict([(-1, "⊖"), (0, "?"), (1, "⊕")])
tikz_dict = dict([(-1, "-"), (0, " "), (1, "+")])


class StateVertex(VertexInterface):
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

    def get_all_indices(self):
        return [index_in_lattice(self.r, self.c, i, self.state.latmod) for i in range(4)]


class LatticeModelState:
    def __init__(self, latmod: LatticeModel):
        self.latmod = latmod
        self.values = [0 for i in range(self.latmod.values_length)]

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
            sum += weight
        return sum

    def iter_solutions(self, unset_indices=None, start=0):
        if unset_indices is None:
            unset_indices = []
            for (i, val) in enumerate(self.values):
                if val == 0:
                    unset_indices.append(i)
        if start >= len(unset_indices):
            yield self
        else:
            j = unset_indices[start]
            self.values[j] = -1
            if not self.bad_change(j, unset_indices, start):
                yield from self.iter_solutions(unset_indices, start + 1)
            self.values[j] = 1
            if not self.bad_change(j, unset_indices, start):
                yield from self.iter_solutions(unset_indices, start + 1)

    def bad_change(self, i, unset_indices, start):
        for r, c in self.latmod.adjacent_vertices(i):
            current = self.get_vertex(r, c)
            # unset potentially set values
            for i in current.get_all_indices():
                # uses fact that unset_indices is ordered
                if i > unset_indices[start] and i in unset_indices:
                    self.values[i] = 0
            matches_something = False
            for v in self.latmod.verts:
                if current.can_realize(v):
                    matches_something = True
                    break
            if not matches_something:
                return True
        return False

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
