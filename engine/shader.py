import moderngl
from typing import Dict

class shader_programs:
    def __init__(self, ctx:moderngl.Context):
        self.ctx = ctx
        self.programs: Dict[str, moderngl.Program] = {}

    def __getitem__(self, item):
        return self.programs[item]

    def get_shader_program(self, shader_name:str) -> moderngl.Program:
        with open(f"assets/shaders/{shader_name}.vert") as file:
            vertex_shader = file.read()

        with open(f"assets/shaders/{shader_name}.frag") as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        self.programs[shader_name] = program
    
    def destroy(self):
        [program.release() for program in self.programs.values()]