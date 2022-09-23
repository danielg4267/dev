/**
*	Daniel Gonzalez
*	CS5310 - Final Project
*	Scene Manager - Contains all the objects for the scene, sets the background,
*	chooses shaders and updates textures/camera angles.
*/
# include <fstream>
#include "SceneManager.hpp"
#include "Camera.hpp"


SceneManager::SceneManager(){
	
	m_camera = new Camera();
	//TODO: should be able to choose objects at start
	//TODO: maybe find a way to obtain all the shaders in a folder as well?
	m_shaders.push_back(new Shader("./shaders/normalVert.glsl", "./shaders/normalFrag.glsl"));
	m_shaders.push_back(new Shader("./shaders/toonVert.glsl", "./shaders/toonFrag.glsl"));
	m_shaders.push_back(new Shader("./shaders/basicVert.glsl", "./shaders/basicFrag.glsl"));

	LoadObject("./../common/objects/bunny_centered.obj");
	LoadObject("./../common/objects/windmill/windmill.obj");
	LoadObject("./../common/objects/chapel/chapel_obj.obj");
	LoadObject("./../common/objects/capsule/capsule.obj");
	
}

SceneManager::~SceneManager(){
	
	
}

void SceneManager::LoadObject(const std::string& filePathName){
	
	m_objects.push_back(new Object(filePathName));
	
}

void SceneManager::Render(int screenWidth, int screenHeight){
		
		glViewport(0, 0, screenWidth, screenHeight);
		glClearColor( 0.8f, 0.8f, 0.8f, 1.f );
		glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT);
		glEnable(GL_DEPTH_TEST);
		glEnable(GL_TEXTURE_2D);
		
		
		float x_displacement = 0.0f;
		
		for(int i =0; i< m_shaders.size(); i++){
			
			Update(m_shaders[i]);
			float z_displacement = -5.0f;
			
			for(int j=0; j<m_objects.size(); j++){
				//just to position it better - will add proper transform functions later
				UpdateModel(m_shaders[i], x_displacement, z_displacement);
				//was it clicked?
				if(m_objects[j]->outline){m_shaders[i]->SetUniform1i("u_clicked", 1);}
				m_objects[j]->Render();
				z_displacement-=5.0f;
				m_shaders[i]->SetUniform1i("u_clicked", 0);
			}
			x_displacement += 5.0f;
		}
		
	
}

void SceneManager::Update(Shader* shader){
	
	//make sure we're using the right shader
	glUseProgram(shader->getID());
	//calculate the MVP matrices
	glm::mat4 model = glm::translate(glm::mat4(1.0f),glm::vec3(0.0f,0.0f,-5.0f)); //this is by default, in case for some reason "update model" isn't called later
	glm::mat4 view = m_camera->GetWorldToViewMatrix();
	glm::mat4 projection = glm::perspective(45.0f,(float)1920/(float)1080,0.1f,20.0f); //TODO: width/height should be variable

	glm::vec3 pos = m_camera->GetCurrentPos();
	glm::vec3 viewDir = m_camera->GetViewDir();
	
	//set uniforms in the program
	shader->SetUniformMatrix4fv("model",&model[0][0]);
	shader->SetUniformMatrix4fv("view", &view[0][0]);
	shader->SetUniformMatrix4fv("projection", &projection[0][0]);
	//update position
	shader->SetUniform3f("u_lightPos", pos.x, pos.y, pos.z);
	shader->SetUniform3f("u_viewPos", pos.x, pos.y, pos.z);
	shader->SetUniform3f("u_viewDir", viewDir.x, viewDir.y, viewDir.z); //this is mostly for the toon shader
	
	//make sure texture/normal map are in the right slot
	shader->SetUniform1i("u_Texture", 0);
	shader->SetUniform1i("u_NormalMap", 1);
	
}
void SceneManager::UpdateModel(Shader* shader, float x_displacement, float z_displacement){
	glm::mat4 model = glm::translate(glm::mat4(1.0f),glm::vec3(x_displacement,0.0f,z_displacement));
	shader->SetUniformMatrix4fv("model",&model[0][0]);
}

void SceneManager::MousePick(float mouseX, float mouseY){
	//this function takes the XY screen coordinates of a mouse click
	//and goes in reverse order of the MVP matrix to put it in world space
	
	//TODO: width/height should be variable! I say it so often but I'm so lazy goddamn
	//this converts it to normalized openGL coordinate space [-1, 1]
	float x = (2 * mouseX) / 1920 - 1;  
	float y = (2* mouseY) / 1080 - 1;
	glm::vec4 normalCoords = glm::vec4(x, -y, -1.0f, 1.0f); //pointing into the screen at the coordinates we found
	
	//reverse projection matrix and multiply to get to clip space
	glm::mat4 projection = glm::perspective(45.0f,(float)1920/(float)1080,0.1f,20.0f);
	glm::mat4 inverseProjection = glm::inverse(projection);
	glm::vec4 eyeCoords = inverseProjection * normalCoords;
	eyeCoords.z = -1.0f; eyeCoords.w = 1.0f; //to make sure we're still pointing into the screen
	
	//inverse view matrix to get into world space
	glm::mat4 inverseView = glm::inverse(m_camera->GetWorldToViewMatrix());
	glm::vec4 worldCoords = inverseView * eyeCoords;
	glm::vec3 mouseRay = glm::normalize(glm::vec3(worldCoords.x, worldCoords.y, worldCoords.z));
	for(int i = 0; i<m_objects.size(); i++){
		//this function doesn't work quite just yet, but uncomment it to see my poor attempt at ray-tracing
		//m_objects[i]->Clicked_RayIntersect(m_camera->GetCurrentPos(), mouseRay);
		m_objects[i]->Clicked();
	}
	
}

Camera* SceneManager::GetCamera(){return m_camera;}