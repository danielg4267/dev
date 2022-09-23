/**
Daniel Gonzalez
Fall 2021
CS5310
SDL_GL - handles creation of a window and rendering within it
*/

#include <SDL2/SDL.h>
#include <glad/glad.h>
#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <vector>

#include "SceneManager.hpp"
//#include "ObjLoader.hpp"
//#include "Shader.hpp"


class SDL_GL{

	public:
		
		//Constructor/Destructor
		SDL_GL(unsigned int screenWidth, unsigned int screenHeight);
		~SDL_GL();
		
		//Initializes buffers and loads shaders
		void initGL();
		
		//main loop
		void run();
		
		//calls on object to load an object file
		void LoadObject(const std::string& filePathName);
		
		//render object (glDrawElements)
		void render();
		


	
	private:
		// Screen dimension constants
		int screenHeight;
		int screenWidth;
		
		SceneManager* m_renderer;
		
		//Shader* shader;
		
		//ObjLoader* object;
		
		//useful for saving errors (std::cout doesn't work for me with SDL, I used this to write to files)
		std::stringstream errorLog;

		//SDL window
		SDL_Window* m_window ;
		
		//OpenGL context
		SDL_GLContext context;
		
};