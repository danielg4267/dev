/**
*	Daniel Gonzalez
*	CS5310 - Final Project
*	Object - This class stores information relevant to
*	an object and can be updated as needed.
*/

#include <glad/glad.h>
#include <fstream>
#include<string>
#include <sstream>
#include <vector>
#include "glm/glm.hpp"
#include "glm/gtx/transform.hpp"
#include "Texture.hpp"
#include "VertexBufferLayout.hpp"

class Object{
	public:
		Object(const std::string& filePathName);
		~Object();
		render();
		void addVertex(Vertex& v);
		void LoadMtl(const std::string& mtllib);
		void GenerateBuffers();
		void Render();
		void CalculateTangents();
		void Clicked();
		void Clicked_RayIntersect(glm::vec3 viewPos, glm::vec3 mouseRay);
		void MaxMinCoords();
		
		//to determine if it should have an outline
		bool outline;

		
	
	private:
		
		std::stringstream errorLog;
		std::vector<Vertex> vertexData;
		std::vector<unsigned int> indexData;
		std::string filePath;
		std::string mtllib;
		Texture* texture;
		Texture* normalMap;
		VertexBufferLayout buffer;
		
		//bounding box coordinates/normals, super inaccurate for clicking but good enough for now
		float x_max, x_min, y_max, y_min, z_max, z_min;
		
		
};

		