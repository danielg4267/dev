/**
*	Daniel Gonzalez
*	CS5310 - Final Project
*	SceneManager - this class is like the controller of the scene - 
*	it knows all the objects, shaders, camera, and lighting, and manages them
*	and updates them.
*/
#include <glad/glad.h>
#include <vector>
#include <string>
#include "glm/vec3.hpp"
#include "glm/gtc/matrix_transform.hpp"
#include "Object.hpp"
#include "Shader.hpp"
#include "Camera.hpp"

class SceneManager{
	
	public:
		SceneManager();
		~SceneManager();
		void Render(int screenWidth, int screenHeight);
		void LoadObject(const std::string& filePathName);
		void Update(Shader* shader);
		Camera* GetCamera();
		void MousePick(float mouseX, float mouseY);
	
	private:
	
		//a little shortcut for moving things in space, because transformations aren't
		//the main part of my program - but i would use the transform class otherwise
		void UpdateModel(Shader* shader, float x_displacement, float z_displacement);
		
		std::vector<Object*> m_objects;
		std::vector<Shader*> m_shaders;
		Camera* m_camera;
		
		
	
	
};