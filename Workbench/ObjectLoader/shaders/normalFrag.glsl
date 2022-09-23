#version 330 core

in vec2 v_texCoord;
in vec3 TangentLightPos;
in vec3 TangentViewPos;
in vec3 TangentFragPos;
in vec3 v_normal;
uniform sampler2D u_Texture;
uniform sampler2D u_NormalMap;

uniform int u_clicked;

out vec4 FragColor;

void main(){
	
	vec3 normal = texture(u_NormalMap, v_texCoord).rgb;
	normal = normalize(normal * 2.0f - 1.0f);
	vec3 viewDir = normalize(TangentViewPos - TangentFragPos);
	
	vec3 lightColor = vec3(1.0, 1.0, 1.0);
	//ambient light
	float ambientIntensity = 0.1f;
	vec3 ambient = ambientIntensity * lightColor;
	
	//direction vectors based on inputs
	vec3 lightDir = normalize (TangentLightPos - TangentFragPos);
	vec3 reflectDir = reflect(-lightDir, normal);
	
	//diffuse impact
	float diffImpact = max(dot(normal, lightDir), 0.0);
	vec3 diffuse = diffImpact * lightColor;
	
	//specular light
	float specIntensity = 0.9f;
	float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
	vec3 specular = specIntensity * spec * lightColor;
	
	vec3 Lighting = specular;// + specular + diffuse;
	
	vec3 color = texture(u_Texture, v_texCoord).rgb;
	
	FragColor = vec4(color * Lighting, 1.0);
	
	
	
	
}