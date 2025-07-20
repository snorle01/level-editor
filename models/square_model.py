from engine.model import *
from engine.rect import rect_class
from vbo.square_vbo import square_frame_VBO, square_VBO

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from engine.engine import engine_class

class square_base_model(base_model):
    def __init__(self, engine, position: tuple[int, int, int], scale: tuple[int, int, int], rect_position, rect_width, rect_height, color: glm.vec3 = glm.vec3(1.0, 0.0, 0.0)):
        super().__init__(engine)
        self.engine: engine_class = engine
        self.position = position
        self.scale = scale
        self.m_model = self.get_model_matrix()
        self.color = color
        self.rect = rect_class(rect_position, rect_width, rect_height)

    def get_model_matrix(self):
        m_model = glm.mat4()
        # translate
        m_model = glm.translate(m_model, self.position)
        # rotate
        m_model = glm.rotate(m_model, 0, glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, 0, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, 0, glm.vec3(0, 0, 1))
        # scale
        m_model = glm.scale(m_model, self.scale)
        return m_model

class square_frame_model(square_base_model):
    def __init__(self, engine, position, scale, rect_position, rect_width, rect_height, color = glm.vec3(1, 0, 0)):
        super().__init__(engine, position, scale, rect_position, rect_width, rect_height, color)
        self.get_VAO(square_frame_VBO(self.engine.ctx), "color", "test")

    def render(self):
        self.VAO.program["m_model"].write(self.m_model)
        self.VAO.program["color"].write(self.color)
        self.VAO.render(moderngl.LINE_LOOP)

class square_model(square_base_model):
    def __init__(self, engine, position, scale, rect_position, rect_width, rect_height, color = glm.vec3(1, 0, 0)):
        super().__init__(engine, position, scale, rect_position, rect_width, rect_height, color)
        self.get_VAO(square_VBO(self.engine.ctx), "color", "test")

    def render(self):
        self.VAO.program["m_model"].write(self.m_model)
        self.VAO.program["color"].write(self.color)
        self.VAO.render()