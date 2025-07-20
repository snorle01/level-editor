from engine.vbo import VBOs_class, base_VBO
from engine.shader import shader_programs
from typing import Dict
import moderngl

class VAOs_class:
    def __init__(self, ctx:moderngl.Context):
        self.ctx = ctx
        self.VBOs_class: VBOs_class = VBOs_class(ctx)
        self.programs = shader_programs(ctx)
        self.VAOs: Dict[str, moderngl.VertexArray] = {}

    # VAO_name is the name of the variable in the vao dict
    def get_VAO(self, VAO_name: str, program_name: str, VBO_name: str) -> moderngl.VertexArray:
        program:moderngl.Program = self.programs.programs[program_name]
        VBO:base_VBO = self.VBOs_class.VBOs[VBO_name]
        VAO = self.ctx.vertex_array(program, [(VBO.VBO, VBO.format, *VBO.attribs)], skip_errors=True)
        self.VAOs[VAO_name] = VAO
    
    def destroy(self):
        self.VBOs_class.destroy()
        self.programs.destroy()
        [VAO.release() for VAO in self.VAOs.values()]