#version 330 core

layout(location=0) in vec3 position;
layout(location=1) in vec2 texCoord;
layout(location=2) in vec3 normal;
layout(location=3) in vec3 tangent;
layout(location=4) in vec3 bitangent;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

uniform vec3 u_lightPos;
uniform vec3 u_viewPos;

out vec2 v_texCoord;
out vec3 TangentLightPos;
out vec3 TangentViewPos;
out vec3 TangentFragPos;

out vec3 v_normal;
//out vec3 FragPos;

void main(){

	//position of vertex
	gl_Position = projection  * view * model * vec4(position, 1.0f);
	
	//calculate TBN matrix
	vec3 T = normalize(vec3(model* vec4(tangent, 1.0)));
	vec3 B = normalize(vec3(model * vec4(bitangent, 1.0)));
	vec3 N = normalize(vec3(model * vec4(normal, 1.0)));
	mat3 TBN = mat3(T,B,N);
	
	//get positions in tangent space
	TangentLightPos =  TBN * u_lightPos;
	TangentViewPos = TBN * u_viewPos;
	TangentFragPos = TBN * vec3(model * vec4(position, 1.0));
	
	//v_normal = normal;
	//FragPos = vec3(model * vec4(position, 1.0f));
	
	v_normal = normal;
	v_texCoord = texCoord;
	
	
}