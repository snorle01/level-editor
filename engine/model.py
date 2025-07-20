import moderngl
import glm
import math
from engine.vbo import *
from engine.level import level
from typing import TYPE_CHECKING

from engine.level.level_vbo import level_VBO

if TYPE_CHECKING:
    from engine import engine_class

class base_model:
    def __init__(self, engine):
        self.engine: engine_class = engine
        self.VAO: moderngl.VertexArray

    def render(self):
        self.VAO.render()

    def get_VAO(self, VBO_class: base_VBO, shader_name: str, VAO_name: str):
        self.engine.VAO.VBOs_class.VBOs[VBO_class.name] = VBO_class
        self.engine.VAO.programs.get_shader_program(shader_name)
        self.engine.VAO.get_VAO(VAO_name, shader_name, VBO_class.name)

        self.VAO = self.engine.VAO.VAOs[VAO_name]

class world_model(base_model):
    def __init__(self, engine, pos: tuple[int,int,int] = (0,0,0), rot: tuple[int,int,int] = (0,0,0), scale: tuple[int,int,int] = (1,1,1)):
        super().__init__(engine)
        self.pos = glm.vec3(pos)
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.m_model = self.get_model_matrix()

    def get_model_matrix(self):
        m_model = glm.mat4()
        # translate
        m_model = glm.translate(m_model, self.pos)
        # rotate
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0, 0, 1))
        # scale
        m_model = glm.scale(m_model, self.scale)
        return m_model
    
    def render(self):
        self.VAO.program["m_proj"].write(self.engine.camera.m_proj)
        self.VAO.program["m_view"].write(self.engine.camera.m_view)
        self.VAO.program["m_model"].write(self.m_model)
        super().render()

class texture_model(world_model):
    def __init__(self, engine, texture_name: str, pos = (0, 0, 0), rot = (0, 0, 0), scale = (1, 1, 1)):
        super().__init__(engine, pos, rot, scale)
        self.texture = self.engine.texture.get_texture(texture_name)
        self.get_VAO(texture_VBO(self.engine.ctx), "texture", "texture")

    def render(self):
        self.VAO.program["texture_0"] = 0
        self.texture.use(location=0)
        super().render()

class level(world_model):
    def __init__(self, engine, level_data:level, texture_name: str, pos = (0, 0, 0), rot = (0, 0, 0), scale = (1, 1, 1)):
        super().__init__(engine, pos, rot, scale)
        self.texture = self.engine.texture.get_texture(texture_name)
        self.get_VAO(level_VBO(self.engine.ctx, level_data), "texture", "level")

    def render(self):
        self.VAO.program["texture_0"] = 0
        self.texture.use(location=0)
        super().render()