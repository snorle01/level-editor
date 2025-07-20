#version 330 core

layout (location = 0) in vec3 position;

uniform mat4 m_model;

void main() {
    gl_Position = m_model * vec4(position, 1.0);
}