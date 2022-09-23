#version 330 core

in vec2 v_texCoord;
in vec3 v_normal;
in vec3 FragPos;

uniform vec3 u_lightPos;
uniform vec3 u_viewPos;
uniform vec3 u_viewDir;
uniform sampler2D u_Texture;
uniform sampler2D u_NormalMap;

//a uniform to determine if the fragment should consider calculating an outline
uniform int u_clicked;

out vec4 FragColor;

void main(){

	vec3 viewDir = normalize(u_viewPos - FragPos);
	vec3 lightDir = normalize (u_lightPos - FragPos);
	
	float intensity = dot(lightDir, normalize(v_normal));
	float outline = dot(normalize(v_normal), viewDir);
	//uncomment if you want actual texture - but I think it looks better with simple colors/textures (which i don't have!)
	//vec3 color = texture(u_Texture, v_texCoord).rgb;
	
	vec3 color = vec3(1.0f, 0.6f, 0.6f);
	if(u_clicked != 0 && outline <= 0.2){color=vec3(0.0f, 1.0f, 0.0f);}
	else{
		if(intensity > 0.95){
			color *= 1.0;
			
		}
		else if (intensity > 0.5){
			color *= 0.6;
		}
		else if(intensity > 0.25){
			color *= 0.4;
		}
		else{
			color *= 0.2;
		}
	}
	
	FragColor = vec4(color, 1.0);
	//FragColor = vec4(1.0f, 0.0f, 0.0f, 1.0f);
	
	
	
	
	
	
	
	
	//vec3 reflectDir = reflect(-lightDir, normal);

	/*vec3 lightColor = vec3(1.0, 1.0, 1.0);
	//ambient light
	float ambientIntensity = 0.1f;
	vec3 ambient = ambientIntensity * lightColor;
	
	vec3 normal = texture(u_NormalMap, v_texCoord).rgb;
	normal = normalize(normal * 2.0 - 1.0);
	
	//direction vectors based on inputs
	vec3 viewDir = normalize(u_viewPos - FragPos);
	vec3 lightDir = normalize (LightPos - TangentFragPos);
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
	
	FragColor = vec4(color * Lighting, 1.0);*/
	
	
	//vec4 texColor = texture(u_Texture, v_texCoord);
	//FragColor = texColor;
	
	
	
}