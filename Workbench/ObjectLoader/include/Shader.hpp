/**
Daniel Gonzalez
Fall 2021
CS5310
Shader - Loads Shader source file, creates program
*/
#ifndef SHADER_HPP
#define SHADER_HPP

#include <SDL2/SDL.h>
#include <glad/glad.h>
#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <vector>



class Shader{

	public:
		
		//Constructor/Destructor
		Shader(const std::string& vShaderSrc, const std::string& fShaderSrc);
		~Shader();

		
		//shader helpers
		void CreateProgram(const std::string& vShaderSrc, const std::string& fShaderSrc);
		unsigned int CompileShader(unsigned int type, const std::string& source);
		std::string LoadShader(const std::string& filePathName);
		void SetUniformMatrix4fv(const GLchar* name, const GLfloat* value);
		void SetUniform1i(const GLchar* name, int value);
		void SetUniform3f(const GLchar* name, float v0, float v1, float v2);
		unsigned int getID();
		

		


	
	private:

		
		//useful for saving errors (std::cout doesn't work for me with SDL, I used this to write to files)
		std::stringstream errorLog;
	
		//shader used to render
		unsigned int shader_ID;
		

};
#endif