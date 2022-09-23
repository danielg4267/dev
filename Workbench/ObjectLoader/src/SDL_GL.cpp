/**
Daniel Gonzalez
Fall 2021
CS5310
SDL_GL - handles creation of a window and rendering within it
*/
#include <glad/glad.h>
#include <SDL2/SDL.h>
#include "SDL_GL.hpp"

SDL_GL::SDL_GL(unsigned int w, unsigned int h){
	
	screenWidth = w;
	screenHeight = h;
	
	//This logic mostly comes from past labs' SDLGraphicsProgram() constructor
	
	bool success = true;
	

	
	m_window = NULL;
	//initialize SDL
	if (SDL_Init(SDL_INIT_VIDEO) != 0){
		errorLog << "Error initializing SDL: "<< SDL_GetError() << std::endl;
		success = false;
	}
	else{
		//OpenGL 3.3
		SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 3);
		SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 3);
		SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE);
		
		//doublebuffer
		SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, 1);
		SDL_GL_SetAttribute(SDL_GL_DEPTH_SIZE, 24);
		
		//create window
		m_window = SDL_CreateWindow("Object Loader",
						SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
						screenWidth, screenHeight,
						SDL_WINDOW_OPENGL | SDL_WINDOW_SHOWN);
						
		//check window was created
		if (m_window == NULL){
			errorLog << "Error creating SDL_GL Window:" << SDL_GetError() << std::endl;
			success = false;
		}
						
		SDL_GLContext context;
		context = SDL_GL_CreateContext(m_window);
		
		//check context was created
		if (context == NULL){
			errorLog << "Error creating SDL_GL Context: " << SDL_GetError() << std::endl;
			success = false;
		}
		
		//load OpenGL functions
		if (!gladLoadGLLoader(SDL_GL_GetProcAddress)){
			errorLog << "Error loading GLAD library" << std::endl;
			success = false;
		}
	}
	
	m_renderer = new SceneManager();
	
	if (success){
		errorLog << "No errors detected upon initialization." << std::endl;
	}
	
	
	initGL();
	
	
	
}


SDL_GL::~SDL_GL(){
	
	//save errorLog (this is mostly for me since cout doesn't work when we use SDL)
	/*std::ofstream errors("errors.txt");
	errors << errorLog.str() << std::endl;*/

	//final quit commands for SDL/GL
	SDL_DestroyWindow( m_window );
	m_window = NULL;
	//object->~ObjLoader();
	SDL_Quit();
}

void SDL_GL::initGL(){
	
		
		// Disable depth test and face culling.
		glEnable(GL_DEPTH_TEST);
		glDisable(GL_CULL_FACE);

}
/*
void SDL_GL::LoadObject(const std::string& filePathName){
	object = new ObjLoader(screenWidth, screenHeight);
	object->LoadObject(filePathName);
}*/

void SDL_GL::run(){
	
	//exit loop bool
	bool quit = false;
	//whether to render wireframe or fill
	bool wireframe = true;
	float cameraSpeed = 0.15;
	int mouseX;
	int mouseY;
	SDL_Event e;
	while(!quit){
		
		//user clicked/pressed something
		while(SDL_PollEvent(&e) != 0){
				//pressed X
				switch(e.type){
					case SDL_QUIT:
						quit = true;
					break;

					case SDL_MOUSEMOTION:
					// Handle mouse movements
					mouseX = e.motion.x;
					mouseY = e.motion.y;
					m_renderer->GetCamera()->MouseLook(mouseX, mouseY);
					//m_renderer->MousePick(mouseX, mouseY);
					break;
					
					case SDL_MOUSEBUTTONDOWN:
						SDL_GetMouseState(&mouseX, &mouseY);
						m_renderer->MousePick(mouseX, mouseY);
					break;
					
					//pressed key
					case SDL_KEYDOWN:
						switch(e.key.keysym.sym){
							case SDLK_RSHIFT:
								m_renderer->GetCamera()->MoveUp(cameraSpeed);
							break;
							case SDLK_RCTRL:
								m_renderer->GetCamera()->MoveDown(cameraSpeed);
							break;
							case SDLK_DOWN:
								m_renderer->GetCamera()->MoveBackward(cameraSpeed);
							break;
							case SDLK_UP:
								m_renderer->GetCamera()->MoveForward(cameraSpeed);
							break;
							case SDLK_LEFT:
								m_renderer->GetCamera()->MoveLeft(cameraSpeed);
							break;
							case SDLK_RIGHT:
								m_renderer->GetCamera()->MoveRight(cameraSpeed);
							break;
							case SDLK_w:
								wireframe = !wireframe;
							break;
							case SDLK_q:
								quit = true;
							break;
						}
					break;
				}
			}
		
		//change mode if necessary
		if(wireframe){
			glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
		}
		else{
			glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);
		}
			

		//render and display
		//render();
		m_renderer->Render(screenWidth, screenHeight);
		SDL_GL_SwapWindow(m_window);
		

	}
		
	SDL_DestroyWindow(m_window);
	SDL_Quit();

	
}
/*
void SDL_GL::render(){

		// Initialize clear color
		// This is the background of the screen.
		glViewport(0, 0, screenWidth, screenHeight);
		glClearColor( 0.3f, 0.3f, 0.3f, 1.f );
		//Clear color buffer and Depth Buffer
		glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT);
		
		//glDrawElements(GL_TRIANGLES, object->indexSize(), GL_UNSIGNED_INT, nullptr);   
}*/
	