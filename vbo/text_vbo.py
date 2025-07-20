import numpy
from engine.vbo import *

class text_VBO(base_VBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.name = "text"
        self.format = "3f 2f"
        self.attribs = ["position", "uv_vert"]

    def get_vertex_data(self):
        vertex = [(1, 0, 0), (0, 1, 0), (0, 0, 0),
                  (1, 0, 0), ( 1, 1, 0), (0, 1, 0)]
        uv_vert = [(1, 0), (0, 1), (0, 0),
                   (1, 0), (1, 1), (0, 1)]

        vertex_data = numpy.hstack([vertex, uv_vert])
        vertex_data = numpy.array(vertex_data, dtype="f4")
        return vertex_data