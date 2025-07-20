from engine.model import *
from vbo.test_vbo import test_VBO

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from engine.engine import engine_class

class test_model(base_model):
    def __init__(self, engine):
        super().__init__(engine)
        self.engine: engine_class = engine
        self.get_VAO(test_VBO(self.engine.ctx), "color", "test")

    def render(self):
        self.VAO.render(moderngl.LINE_LOOP)