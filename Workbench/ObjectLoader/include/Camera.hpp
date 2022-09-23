/**
*	Daniel Gonzalez
*	CS5310 - Final Project
*	Camera - this class is the camera. It's heavily inspired
*	from camera class from previous labs.
*/
#ifndef CAMERA_HPP
#define CAMERA_HPP
#include "glm/glm.hpp"
#include "glm/gtx/transform.hpp"

class Camera{
	
	public:
	
		Camera();
		void MoveForward(float speed);
		void MoveBackward(float speed);
		void MoveLeft(float speed);
		void MoveRight(float speed);
		void MoveUp(float speed);
		void MoveDown(float speed);
		glm::mat4 GetWorldToViewMatrix()const;
		glm::vec3 GetCurrentPos();
		glm::vec3 GetViewDir();
		void MouseLook(int mouseX, int mouseY);
		
	
	
	
	
	private:
	
		glm::vec3 m_upDir;
		glm::vec3 m_viewDir;
		glm::vec3 m_eyePos;
		glm::vec2 m_oldMousePos;
	
	
	
	
};

#endif


