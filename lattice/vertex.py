from abc import abstractmethod

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


class HVertexInterface(VertexInterface):
    @abstractmethod
    def get_all(self):
        pass

    def compute_weight(self, admissible, r):
        for v in admissible:
            if self.get_all() == v.values:
                return v.weight(r)
        return 1


class Vertex(HVertexInterface):
    def __init__(self, values_word, weight):
        self.values = wtv(values_word)
        # should be lambda of row/col
        self.weight = weight

    def get_all(self):
        return self.values


class RVertexInterface(VertexInterface):
    @abstractmethod
    def get_all(self):
        pass

    def compute_weight(self, admissible, r1, r2):
        for v in admissible:
            if self.get_all() == v.values:
                return v.weight(r1, r2)
        return 1


class RVertex(VertexInterface):
    def __init__(self, values_word, weight):
        self.values = wtv(values_word)
        # should be lambda of row/col
        self.weight = weight

    def get_all(self):
        return self.values
