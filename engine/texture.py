import pygame, moderngl
from typing import Dict

class texture_class:
    def __init__(self, engine):
        self.engine = engine
        self.ctx: moderngl.Context = self.engine.ctx
        self.textures: Dict[str, moderngl.Texture] = {}

        # make error texture
        surface = pygame.Surface((64, 64))
        surface.fill((255, 0, 255))
        for y in range(4):
            for x in range(2):
                x_pos = x * 32
                if y % 2:
                    x_pos += 16
                pygame.draw.rect(surface, (0, 0, 0), (x_pos, y * 16, 16, 16))

        self.error = self.surface_to_texture(surface)
        """
        # turn it into openGL texture
        self.error = self.ctx.texture(size=surface.get_size(), components=3, data=pygame.image.tostring(surface, "RGB"))
        # mipmaps
        self.error.filter = (moderngl.LINEAR_MIPMAP_LINEAR, moderngl.LINEAR)
        self.error.build_mipmaps()
        self.error.anisotropy = 32.0
        """

    def surface_to_texture(self, surface: pygame.Surface):
        # turn it into openGL texture
        surface = pygame.transform.flip(surface, flip_x=False, flip_y=True)
        surface = self.ctx.texture(size=surface.get_size(), components=3, data=pygame.image.tostring(surface, "RGB"))
        # mipmaps
        surface.filter = (moderngl.LINEAR_MIPMAP_LINEAR, moderngl.LINEAR)
        surface.build_mipmaps()
        surface.anisotropy = 32.0
        return surface
    
    def surface_to_alpha_texture(self, surface: pygame.Surface):
        # turn it into openGL texture
        surface = pygame.transform.flip(surface, flip_x=False, flip_y=True)
        surface = self.ctx.texture(size=surface.get_size(), components=4, data=pygame.image.tostring(surface, "RGBA"))
        # mipmaps
        surface.filter = (moderngl.LINEAR_MIPMAP_LINEAR, moderngl.LINEAR)
        surface.build_mipmaps()
        surface.anisotropy = 32.0
        return surface

    # default texture
    def load_texture(self, texture_name: str, path: str):
        texture = pygame.image.load(path).convert()
        texture = pygame.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3, data=pygame.image.tostring(texture, "RGB"))
        # mipmaps
        texture.filter = (moderngl.LINEAR_MIPMAP_LINEAR, moderngl.LINEAR)
        texture.build_mipmaps()
        texture.anisotropy = 32.0
        
        self.textures[texture_name] = texture
    
    def destroy(self):
        [tex.release() for tex in self.textures.values()]

    def get_texture(self, texture_name: str) -> moderngl.Texture:
        if texture_name in self.textures:
            return self.textures[texture_name]
        else:
            print("FAILED TO FIND TEXTURE")
            return self.error