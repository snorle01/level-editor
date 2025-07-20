import pygame, moderngl
from engine.vao import VAOs_class
from engine.texture import texture_class
from engine.camera import camera_class
from engine.scene import base_scene

class engine_class:
    def __init__(self, scene, icon = None):
        if not icon == None:
            pygame.display.set_icon(icon)
        pygame.init()
        # initilize variables
        self.clock = pygame.time.Clock()
        self.time = 0
        # set atribute of openGL
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

        pygame.display.set_mode((0, 0), flags=pygame.OPENGL | pygame.DOUBLEBUF | pygame.FULLSCREEN)

        # change mouse settings
        #pygame.event.set_grab(True)
        #pygame.mouse.set_visible(False)

        self.ctx = moderngl.create_context()
        self.ctx.enable(flags=moderngl.DEPTH_TEST | moderngl.CULL_FACE) # | moderngl.CULL_FACE

        self.VAO = VAOs_class(self.ctx)
        self.texture = texture_class(self)
        self.camera = camera_class(self, (0, 0, 0))
        self.scene: base_scene = scene(self)

        self.clear_color = ((0, 1, 0.75))

    def destroy(self):
        self.VAO.destroy
        self.texture.destroy()