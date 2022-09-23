/**
*	Daniel Gonzalez
*	CS5310 - Final Project
*	VertexBufferLayout - Generates different types of buffers depending on 
*	data given.
*/
#include "VertexBufferLayout.hpp"	

VertexBufferLayout::VertexBufferLayout(){
	
}

VertexBufferLayout::~VertexBufferLayout(){
	
}

void VertexBufferLayout::CreateBuffer_vt(std::vector<Vertex>& vertexData, std::vector<unsigned int>& indexData){
	
	//new VAO
	glGenVertexArrays(1, &VAO);
	glBindVertexArray(VAO);
	 
	//new VBO
	glGenBuffers(1, &VBO);
	glBindBuffer(GL_ARRAY_BUFFER, VBO);
	//use data currently stored
	glBufferData(GL_ARRAY_BUFFER, vertexData.size()*sizeof(float)*5, vertexData.data(), GL_STATIC_DRAW);
	
	//only using position attribute
	glEnableVertexAttribArray(0);
	glVertexAttribPointer(0,  3, GL_FLOAT, GL_FALSE, sizeof(float) * 5, (void*)0);
	
	glEnableVertexAttribArray(1);
	glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, sizeof(float) * 5, (char*)(sizeof(float)*3));
	
	//index buffer array, using data stored
	glGenBuffers(1, &IBO);
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, IBO);
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, indexData.size()*sizeof(unsigned int), indexData.data(), GL_STATIC_DRAW);
	
	
}

void VertexBufferLayout::CreateBuffer_vtn(std::vector<Vertex>& vertexData, std::vector<unsigned int>& indexData){
	
	//new VAO
	glGenVertexArrays(1, &VAO);
	glBindVertexArray(VAO);
	 
	//new VBO
	glGenBuffers(1, &VBO);
	glBindBuffer(GL_ARRAY_BUFFER, VBO);
	//position attribute
	glBufferData(GL_ARRAY_BUFFER, vertexData.size()*sizeof(float)*14, vertexData.data(), GL_STATIC_DRAW);
	
	//position attribute
	glEnableVertexAttribArray(0);
	glVertexAttribPointer(0,  3, GL_FLOAT, GL_FALSE, sizeof(float) * 14, (void*)0);
	//texture attribute
	glEnableVertexAttribArray(1);
	glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, sizeof(float) * 14, (char*)(sizeof(float)*3));
	//normal attribute
	glEnableVertexAttribArray(2);
	glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, sizeof(float) * 14, (char*)(sizeof(float)*5));
	//tangent attribute
	glEnableVertexAttribArray(3);
	glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, sizeof(float) * 14, (char*)(sizeof(float)*8));
	//bitangent attribute
	glEnableVertexAttribArray(4);
	glVertexAttribPointer(4, 3, GL_FLOAT, GL_FALSE, sizeof(float) * 14, (char*)(sizeof(float)*11));
	
	//index buffer array, using data stored
	glGenBuffers(1, &IBO);
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, IBO);
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, indexData.size()*sizeof(unsigned int), indexData.data(), GL_STATIC_DRAW);
	
	
}

void VertexBufferLayout::Bind(){
	glBindVertexArray(VAO);
	glBindBuffer(GL_ARRAY_BUFFER, VBO);
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, IBO);
	
}