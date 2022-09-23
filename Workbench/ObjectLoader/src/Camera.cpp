/**
*	Daniel Gonzalez
*	CS5310 - Final Project
*	Camera - this class is the camera. It's heavily inspired
*	from camera class from previous labs.
*/

#include "Camera.hpp"

Camera::Camera(){
	//initialize values
	m_eyePos = glm::vec3(0.0f, 0.0f, 0.0f);
	m_viewDir = glm::vec3(0.0f, 0.0f, -1.0f);
	m_upDir = glm::vec3(0.0f, 1.0f, 0.0f);
	
}

void Camera::MouseLook(int mouseX, int mouseY){
	//I took this straight from another assignment
	
    // Record our new position as a vector
    glm::vec2 newMousePos(mouseX, mouseY);
    // Detect how much the mouse has moved since
    // the last time
    glm::vec2 mouseDelta = 0.01f*(newMousePos-m_oldMousePos);

    m_viewDir = glm::mat3(glm::rotate(-mouseDelta.x, m_upDir)) * m_viewDir;
    
    // Update our old position after we have made changes 
    m_oldMousePos = newMousePos;
}

void Camera::MoveForward(float speed){
    
	m_eyePos.z -= speed;
}

void Camera::MoveBackward(float speed){
 
	m_eyePos.z += speed;
}

void Camera::MoveLeft(float speed){

	m_eyePos.x -= speed;
}

void Camera::MoveRight(float speed){

	m_eyePos.x += speed;
}

void Camera::MoveUp(float speed){

	m_eyePos.y += speed;
}

void Camera::MoveDown(float speed){

	m_eyePos.y -= speed;
}

glm::mat4 Camera::GetWorldToViewMatrix() const{

    return glm::lookAt( m_eyePos,
                        m_eyePos + m_viewDir, 
                        m_upDir);
}

glm::vec3 Camera::GetCurrentPos(){
	return m_eyePos;
}
glm::vec3 Camera::GetViewDir(){
	return m_viewDir;
}