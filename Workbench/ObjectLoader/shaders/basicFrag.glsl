#version 330 core

out vec4 color;

in vec2 v_texCoord;
uniform sampler2D u_Texture;

void main(){

	vec4 texColor = texture(u_Texture, v_texCoord);
	color = texColor;
	//color = vec4(1.0, 0.0, 0.0, 0.0);
	
}