import numpy, moderngl
from typing import Dict, List

class VBOs_class:
    def __init__(self, ctx:moderngl.Context):
        self.VBOs: Dict[str, base_VBO] = {}

    def __getitem__(self, item):
        return self.VBOs[item]

    def destroy(self):
        [VBO.destroy() for VBO in self.VBOs.values()]

# parent class holds most of the functions needed
class base_VBO:
    def __init__(self, ctx:moderngl.Context):
        self.ctx = ctx
        self.VBO = self.get_VBO()
        self.format: str = None
        self.attribs: List[str] = None
        self.name: str = ""

    def get_vertex_data(self): ...

    @staticmethod
    def get_data(vertices: List[tuple[int, int, int]], indices: List[tuple[int, int, int]]):
        data = []
        for triangle in indices:
            for ind in triangle:
                data.append(vertices[ind])
        return numpy.array(data)

    def get_VBO(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo
    
    def destroy(self):
        self.VBO.release()
    
class texture_VBO(base_VBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.name = "texture"
        self.format = "3f 2f"
        self.attribs = ["position", "uv_vert"]

    def get_vertex_data(self):
        vertex = [(1, 0, 0), (0, 1, 0), (0, 0, 0),
                  (1, 0, 0), (1, 1, 0), (0, 1, 0)]
        uv_vert = [(1, 0), (0, 1), (0, 0),
                   (1, 0), (1, 1), (0, 1)]

        vertex_data = numpy.hstack([vertex, uv_vert])
        vertex_data = numpy.array(vertex_data, dtype="f4")
        return vertex_data