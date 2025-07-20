import pygame
from engine.model import *
from vbo.text_vbo import text_VBO

class text_model(base_model):
    def __init__(self, engine, text: str, position: tuple[int, int, int], scale: tuple[int, int, int]):
        super().__init__(engine)
        self.engine: engine_class = engine
        self.text = text
        self.position = position
        self.scale = scale
        self.m_model = self.get_model_matrix()

        font: pygame.font.Font = pygame.font.SysFont(None, 30)
        surface = font.render(self.text, True, (0, 0, 0))
        self.texture = self.engine.texture.surface_to_alpha_texture(surface)

        self.get_VAO(text_VBO(self.engine.ctx), "texture", "text")

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
    
    def render(self):
        self.VAO.program["m_model"].write(self.m_model)
        self.VAO.program["texture_0"] = 0
        self.texture.use(location=0)
        self.VAO.render() #moderngl.LINE_LOOP