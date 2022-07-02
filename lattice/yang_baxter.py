from abc import abstractmethod
from itertools import product

from lattice.vertex import HVertexInterface, RVertexInterface


symbol_dict = dict([(-1, "⊖"), (0, "?"), (1, "⊕")])


class YangBaxter:
    def __init__(self, h_verts, r_verts):
        self.h_verts = h_verts
        self.r_verts = r_verts


class TopVertex(HVertexInterface):
    def __init__(self, state):
        self.state = state

    def get_all(self):
        return [self.state.values[0], self.state.values[1], self.state.values[2], self.state.values[3]]


class BottomVertex(HVertexInterface):
    def __init__(self, state):
        self.state = state

    def get_all(self):
        return [self.state.values[2], self.state.values[4], self.state.values[5], self.state.values[6]]


class LeftVertex(RVertexInterface):
    def __init__(self, state):
        self.state = state

    def get_all(self):
        return [self.state.values[7], self.state.values[3], self.state.values[6], self.state.values[8]]


class RightVertex(RVertexInterface):
    def __init__(self, state):
        self.state = state

    def get_all(self):
        return [self.state.values[1], self.state.values[7], self.state.values[8], self.state.values[4]]


class YBState:
    def get_top(self):
        return TopVertex(self)

    def get_bot(self):
        return BottomVertex(self)

    @abstractmethod
    def get_diag(self):
        pass

    def is_valid(self):
        top = self.get_top()
        bot = self.get_bot()
        diag = self.get_diag()
        return any(map(lambda v: top.can_realize(v), self.yb.h_verts)) and \
               any(map(lambda v: bot.can_realize(v), self.yb.h_verts)) and \
               any(map(lambda v: diag.can_realize(v), self.yb.r_verts))

    @abstractmethod
    def set_boundary(self, boundary):
        pass

    @abstractmethod
    def unset_indices(self):
        pass

    def iter_solutions(self):
        unset_indices = self.unset_indices()
        for values in product([-1, 1], repeat=3):
            for (i, val) in enumerate(values):
                self.values[unset_indices[i]] = val
            if self.is_valid():
                yield self

    @abstractmethod
    def compute_weight(self):
        pass


class LeftYBState(YBState):
    def __init__(self, yb):
        self.yb = yb
        self.values = [0 for i in range(9)]

    def get_diag(self):
        return LeftVertex(self)

    def unset_indices(self):
        return [3, 2, 6]

    def set_boundary(self, boundary):
        self.values[8] = boundary[0]
        self.values[7] = boundary[1]
        self.values[0] = boundary[2]
        self.values[1] = boundary[3]
        self.values[4] = boundary[4]
        self.values[5] = boundary[5]

    def compute_weight(self):
        product = 1
        product *= self.get_top().compute_weight(self.yb.h_verts, 1)
        product *= self.get_bot().compute_weight(self.yb.h_verts, 2)
        product *= self.get_diag().compute_weight(self.yb.r_verts, 1, 2)
        return product

    def print(self):
        top = list(map(lambda v: symbol_dict[v], self.get_top().get_all()))
        bot = list(map(lambda v: symbol_dict[v], self.get_bot().get_all()))
        diag = list(map(lambda v: symbol_dict[v], self.get_diag().get_all()))
        print(f"""
   {top[0]}
{diag[0]} {diag[1]}+{top[1]}
 X {top[2]}
{diag[3]} {diag[2]}+{bot[1]}
   {bot[2]}
""")


class RightYBState(YBState):
    def __init__(self, yb):
        self.yb = yb
        self.values = [0 for i in range(9)]

    def get_diag(self):
        return RightVertex(self)

    def unset_indices(self):
        return [1, 4, 2]

    def set_boundary(self, boundary):
        self.values[6] = boundary[0]
        self.values[3] = boundary[1]
        self.values[0] = boundary[2]
        self.values[7] = boundary[3]
        self.values[8] = boundary[4]
        self.values[5] = boundary[5]

    def compute_weight(self):
        product = 1
        product *= self.get_top().compute_weight(self.yb.h_verts, 2)
        product *= self.get_bot().compute_weight(self.yb.h_verts, 1)
        product *= self.get_diag().compute_weight(self.yb.r_verts, 1, 2)
        return product

    def print(self):
        top = list(map(lambda v: symbol_dict[v], self.get_top().get_all()))
        bot = list(map(lambda v: symbol_dict[v], self.get_bot().get_all()))
        diag = list(map(lambda v: symbol_dict[v], self.get_diag().get_all()))
        print(f"""
 {top[0]}
{top[3]}+{top[1]} {diag[1]}
 {top[2]} X
{bot[3]}+{bot[1]} {diag[2]}
 {bot[2]}
""")