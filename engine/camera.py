import glm, pygame
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from engine import engine_class

fov = 50
near = 0.1
far = 100
speed = 0.01
sensitivity = 0.05

class camera_class:
    def __init__(self, engine, position: tuple[int, int, int] = (0,0,0), yaw: int = 0, pitch: int = 0):
        self.engine: engine_class = engine
        window_width, window_height = pygame.display.get_surface().get_size()
        self.aspect_ratio = window_width / window_height
        self.position = glm.vec3(position)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)
        self.yaw = yaw
        self.pitch = pitch

        self.m_view = self.get_view_matrix()
        self.m_proj = self.get_projection_matrix()

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self) -> glm.mat4x4:
        return glm.perspective(glm.radians(fov), self.aspect_ratio, near, far)
    
    def update_camera_vectors(self):
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def update(self):
        self.update_camera_vectors()
        self.m_view = self.get_view_matrix()

    def rotate(self, xy: tuple[int,int]):
        rel_x, rel_y = xy
        self.yaw += rel_x * sensitivity
        self.pitch -= rel_y * sensitivity
        self.pitch = max(-89, min(89, self.pitch))