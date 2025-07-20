from typing import List, TYPE_CHECKING
from engine.model import base_model
if TYPE_CHECKING:
    from engine import engine_class

class base_scene:
    def __init__(self, engine):
        self.engine:engine_class = engine
        self.objects:List[base_model] = []

    def render(self):
        for object in self.objects:
            object.render()

    def update(self):
        pass

    def add_object(self, object:base_model):
        self.objects.append(object)

    def add_textures(self, name:str, path:str):
        self.engine.texture.load_texture(name, path)