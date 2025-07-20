#version 330 core

out vec4 FragColor;

in vec2 uv_pos;

uniform sampler2D texture_0;

void main() {
    vec4 texture_color = texture(texture_0, uv_pos);
    if (texture_color.a < 0.1)
        discard;
    FragColor = texture_color;
    //FragColor = texture(texture_0, uv_pos);
}