/**
Daniel Gonzalez
Fall 2021
CS5310
Main
*/

#include "SDL_GL.hpp"
int main(int argc, char* argv[]){
	/*
	if (argc < 2){
		std::cout << "Need an object to load!" << std::endl;
		exit(-1);
	}*/
	
	//create new obj loader
	SDL_GL program(1920, 1080);
	
	//program.LoadObject(argv[1]);
	
	//begin loop
	program.run();
	
	
	return 0;
}