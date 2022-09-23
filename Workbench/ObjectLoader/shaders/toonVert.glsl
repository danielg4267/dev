#version 330 core

layout(location=0) in vec3 position;
layout(location=1) in vec2 texCoord;
layout(location=2) in vec3 normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec2 v_texCoord;
out vec3 v_normal;
out vec3 FragPos;


void main(){

	//position of vertex
	gl_Position = projection  * view * model * vec4(position, 1.0f);
	v_texCoord = texCoord;
	v_normal = normal;
	FragPos = vec3(model * vec4(position, 1.0));

	
	
	
	
}