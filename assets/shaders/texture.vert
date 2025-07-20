#version 330 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 uv_vert;

out vec2 uv_pos;

uniform mat4 m_model;

void main() {
    gl_Position = m_model * vec4(position, 1.0);
    uv_pos = uv_vert;
}