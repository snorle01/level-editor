import numpy
from engine.vbo import base_VBO
from engine.level import level
from typing import List

class level_VBO(base_VBO):
    def __init__(self, ctx, level:level):
        self.level = level
        super().__init__(ctx)
        self.name = "level"
        self.format = "3f 2f"
        self.attribs = ["position", "uv_vert"]

    def get_vertex_data(self):
        vertex: List[int, int, int] = []
        uv_vert: List[int, int] = []

        # floor
        index = 0
        for index in range(self.level.size[0] * self.level.size[1]):
            if self.level.floor[index] == 0:
                continue # skip

            x = self.level.index_to_X(index)
            y = self.level.index_to_Y(index)

            # vertex 1
            vertex.append((x + 1, 0, y + 0))
            vertex.append((x + 0, 0, y + 0)) 
            vertex.append((x + 0, 0, y + 1))
            # vertex 2
            vertex.append((x + 1, 0, y + 0))
            vertex.append((x + 0, 0, y + 1))
            vertex.append((x + 1, 0, y + 1))

            # texture cordinates
            # vertex 1
            uv_vert.append((0, 0))
            uv_vert.append((1, 0))
            uv_vert.append((1, 1))
            # vertex 2
            uv_vert.append((0, 0))
            uv_vert.append((1, 1))
            uv_vert.append((0, 1))

        # wall
        def make_upright_wall(start_pos:tuple[int, int], end_pos:tuple[int, int]):
            # vertex 1
            vertex.append((start_pos[0], 1, start_pos[1]))
            vertex.append((start_pos[0], 0, start_pos[1]))
            vertex.append((end_pos[0], 0, end_pos[1]))
            # vertex 2
            vertex.append((start_pos[0], 1, start_pos[1]))
            vertex.append((end_pos[0], 0, end_pos[1]))
            vertex.append((end_pos[0], 1, end_pos[1]))

            # vertex 1
            uv_vert.append((0, 1))
            uv_vert.append((0, 0))
            uv_vert.append((1, 0))
            # vertex 2
            uv_vert.append((0, 1))
            uv_vert.append((1, 0))
            uv_vert.append((1, 1))

        index = 0
        for index in range(self.level.size[0] * self.level.size[1]):
            if self.level.wall[index] == 0:
                continue # skip

            x = self.level.index_to_X(index)
            y = self.level.index_to_Y(index)
            
            # wall up
            if y - 1 >= 0 and self.level.wall[self.level.XY_to_index((x, y - 1))] == 0:
                make_upright_wall((x + 1, y), (x, y))
            # wall down
            if y + 1 < self.level.size[1] and self.level.wall[self.level.XY_to_index((x, y + 1))] == 0:
                make_upright_wall((x, y + 1), (x + 1, y + 1))
            # wall right
            if x + 1 < self.level.size[0] and self.level.wall[self.level.XY_to_index((x + 1, y))] == 0:
                make_upright_wall((x + 1, y + 1), (x + 1, y))
            # wall left
            if x - 1 >= 0 and self.level.wall[self.level.XY_to_index((x - 1, y))] == 0:
                make_upright_wall((x, y), (x, y + 1))

        # outside wall
        # up
        for x in range(self.level.size[0]):
            if self.level.wall[x] == 0:
                make_upright_wall((x, 0), (x + 1, 0))

        # down
        y = self.level.size[1]
        for x in range(self.level.size[0]):
            if self.level.wall[self.level.XY_to_index((x, y - 1))] == 0:
                make_upright_wall((x + 1, y), (x, y))

        # right
        x = self.level.size[0]
        for y in range(self.level.size[1]):
            if self.level.wall[self.level.XY_to_index((x - 1, y))] == 0:
                make_upright_wall((x, y), (x, y + 1))

        # left
        for y in range(self.level.size[1]):
            if self.level.wall[self.level.XY_to_index((0, y))] == 0:
                make_upright_wall((0, y + 1), (0, y))

        # ceiling
        index = 0
        for index in range(self.level.size[0] * self.level.size[1]):
            if self.level.ceiling[index] == 0:
                continue # skip
            
            x = self.level.index_to_X(index)
            y = self.level.index_to_Y(index)

            # vertex 1
            vertex.append((x + 1, 1, y + 0))
            vertex.append((x + 0, 1, y + 1))
            vertex.append((x + 0, 1, y + 0)) 
            # vertex 2
            vertex.append((x + 1, 1, y + 0))
            vertex.append((x + 1, 1, y + 1))
            vertex.append((x + 0, 1, y + 1))

            # texture cordinates
            # vertex 1
            uv_vert.append((1, 0))
            uv_vert.append((0, 1))
            uv_vert.append((0, 0))
            # vertex 2
            uv_vert.append((1, 0))
            uv_vert.append((1, 1))
            uv_vert.append((0, 1))

        # compile vertex data
        vertex_data = numpy.hstack([vertex, uv_vert])
        vertex_data = numpy.array(vertex_data, dtype="f4")
        return vertex_data