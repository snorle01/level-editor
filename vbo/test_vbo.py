import numpy
from engine.vbo import *

class test_VBO(base_VBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.name = "test"
        self.format = "3f"
        self.attribs = ["position"]

    def get_vertex_data(self):
        vertex = [(0.5, 0, 0), (-0.5, 1, 0), (-0.5, 0, 0),
                  (0.5, 0, 0), ( 0.5, 1, 0), (-0.5, 1, 0)]

        vertex_data = numpy.array(vertex, dtype="f4")
        return vertex_data