/**
Daniel Gonzalez
Fall 2021
CS5310
Shader - Loads Shader source file, creates program
*/
#include <glad/glad.h>
#include <SDL2/SDL.h>
#include "Shader.hpp"


Shader::Shader(const std::string& vShaderPath, const std::string& fShaderPath){
	
	
	std::string vertexShader = LoadShader(vShaderPath);
	std::string fragmentShader = LoadShader(fShaderPath);
	
	//link/create/compile program
	CreateProgram(vertexShader, fragmentShader);
}

Shader::~Shader(){
	glDeleteProgram(shader_ID);
}

void Shader::CreateProgram(const std::string& vShaderSrc, const std::string& fShaderSrc){
	
	//This comes from SDLGraphicsProgram::CreateShader()
	
	//new program
	unsigned int program = glCreateProgram();
	
	//compile shaders
	unsigned int vertexShader = CompileShader(GL_VERTEX_SHADER, vShaderSrc);
	unsigned int fragmentShader = CompileShader(GL_FRAGMENT_SHADER, fShaderSrc);
	
	//attach to program
	glAttachShader(program, vertexShader);
	glAttachShader(program, fragmentShader);
	
	//put program together
	glLinkProgram(program);
	glValidateProgram(program);
	
	//detach shaders
	glDetachShader(program, vertexShader);
	glDetachShader(program, fragmentShader);
	
	//delete shaders
	glDeleteShader(vertexShader);
	glDeleteShader(fragmentShader);
	
	shader_ID = program;
	
}

std::string Shader::LoadShader(const std::string& filePathName){
	
	//This logic comes from lab 5 LoadShader()
	
	std::string source = "";
	std::ifstream file(filePathName);
	
	if (file.is_open()){
		std::string line;
		while(getline(file, line)){
			line += '\n';
			source+=line;
		}
	}
	else{
		errorLog << "Error loading shader file." << filePathName << std::endl;
	}
	/*std::ofstream output("shader.txt", std::ios_base::app);
	output << source;
	output.close();*/
	return source;
	
}

unsigned int Shader::CompileShader(unsigned int type, const std::string& source){
	
	//this code is from CompileShader() in our lab
	
	unsigned int id = glCreateShader(type);
	const char* src = source.c_str();
	glShaderSource(id, 1, &src, nullptr);
	glCompileShader(id);
	
	//check compilation was successful
	int result;
	glGetShaderiv(id, GL_COMPILE_STATUS, &result);
	if(result == GL_FALSE){
		int length;
		glGetShaderiv(id, GL_INFO_LOG_LENGTH, &length);
		char* errorMessages = new char[length]; 
		glGetShaderInfoLog(id, length, &length, errorMessages);
		
		errorLog << "Shader Compilation Failed - Source:\n" 
					<< source << std::endl 
					<< "Error:\n" 
					<< errorMessages << std::endl;
	    delete[] errorMessages;
		//delete bad shader
		glDeleteShader(id);
		return 0;
	}
	
	return id;
	
}

// Set our uniforms for our shader.
void Shader::SetUniformMatrix4fv(const GLchar* name, const GLfloat* value){

    GLint location = glGetUniformLocation(shader_ID,name);

    // Now update this information through our uniforms.
    // glUniformMatrix4v means a 4x4 matrix of floats
    glUniformMatrix4fv(location, 1, GL_FALSE, value);
}

void Shader::SetUniform1i(const GLchar* name, int value){
    GLint location = glGetUniformLocation(shader_ID,name);
    glUniform1i(location, value);
}

void Shader::SetUniform3f(const GLchar* name, float v0, float v1, float v2){
    GLint location = glGetUniformLocation(shader_ID,name);
    glUniform3f(location, v0, v1, v2);
}

unsigned int Shader::getID(){
	return shader_ID;
}