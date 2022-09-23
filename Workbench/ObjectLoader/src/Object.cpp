/**
*	Daniel Gonzalez
*	CS5310 - Final Project
*	Object - this class loads object data and stores it,
*	and calls on the correct buffer layout for the data it has
*/
#include "Object.hpp"

Object::Object(const std::string& filePathName){
	outline = false;
	texture = nullptr;
	normalMap = nullptr;
	bool success = false;
	std::ifstream file(filePathName);
	//keeps track of what order the data comes in for face values
	std::string dataOrder = "";
	//vertex position coordinates
	std::vector<float> vdata;
	//normal coordinates
	std::vector<float> ndata;
	//texture coordinates
	std::vector<float> tdata;
	//used to point to one of the vectors
	std::vector<float>* data = &vdata;

	if(file.is_open()){
		std::string line;
		
		//save the directory we're in, if it exists
		if(filePathName.find_last_of("/") != std::string::npos){
			filePath = filePathName.substr(0, filePathName.find_last_of("/") + 1);
		}
		else{
			filePath = "";
		}

		while(getline(file, line)){
			switch(line.at(0)){
				case 'v':			
					//normal
					if(line.at(1) == 'n'){
						if(dataOrder.back() != 'n'){dataOrder += 'n';}
						data = &ndata;
						line = line.substr(3);
					}
					//texture
					else if(line.at(1) == 't'){
						if(dataOrder.back() != 't'){dataOrder += 't';}
						data = &tdata;
						line = line.substr(3);
					}
					//vertex position
					else{
						if(dataOrder.back() != 'v'){dataOrder += 'v';}
						data = &vdata;
						line = line.substr(2);
					}
					//split and iterate through line by spaces, save numbers
					while (line.find(" ") != -1){
						std::string coord = line.substr(0, line.find(" "));
						data->push_back(stof(coord));
						line.erase(0, line.find(" ") + 1);
					}
					data->push_back(stof(line)); //get last number
				break;	
				
				case 'f':		
					float x, y, z, s, t, nx, ny, nz; //xyz position, st texture coordinates, uvw normal vector
					line = line.substr(2);
					
					//assumes faces are split into 3 vertices as triangles
					for(int i=0; i<3; i++){

						std::string indices = line.substr(0, line.find(" "));
						for(int j = 0; j < dataOrder.size(); j++){
							while(indices.at(0)=='/'){
								indices.erase(0, indices.find("/") + 1);
							}
							//make sure it starts at 0
							int index = stoi( indices.substr(0, indices.find("/")) ) - 1;
							//int index = 1;
							switch(dataOrder.at(j)){
								case 'v':
									//3 floats for every 1 vertex
									index *= 3;
									//get coordinates for vertex position
									x=vdata.at(index);
									y=vdata.at(index+1);
									z=vdata.at(index+2);
								break;
								case 't':
									//2 floats for every 1 vertex
									index *= 2;
									//get coordinates for texture
									s=tdata.at(index);
									t=tdata.at(index+1);
								break;
								case 'n':
									//3 floats for every 1 vertex
									index *=3;
									//get normal vector coordinates
									nx = ndata.at(index);
									ny = ndata.at(index+1);
									nz = ndata.at(index+2);
								break;
							}
							indices.erase(0, indices.find("/") + 1);
						}
						//have all data for a vertex, create and add it, repeat
						Vertex vert(x, y, z, s, t, nx, ny, nz);
						addVertex(vert);
						line.erase(0, line.find(" ") + 1);
					}
				break;
				
				//mtllib file name
				case 'm':
					if(line.substr(0, 6) != "mtllib"){break;} //invalid
					texture = new Texture();
					LoadMtl(filePath + line.substr(7));
				break;
				
				//usemtl does not do anything yet, since i'm assuming each object only has one material
				case 'u':
					if(line.substr(0, 6) != "usemtl"){break;}
				break;
				
				
			}
		}
		file.close();
		success = true;
		
	}
	else{
		errorLog << "Error opening file! Check spelling or file path." << std::endl;

	}
	
	if(success){
		CalculateTangents();
		MaxMinCoords();
		GenerateBuffers(); //only generate buffers if object was successfully loaded
	}
	
}

void Object::LoadMtl(const std::string& mtllib){
	if(texture == nullptr){texture = new Texture();}
	
	std::ifstream file(mtllib);
	if(file.is_open()){
		
		std::string line;
		
		while(getline(file, line)){
			
			//right now, this does nothing but look for the PPM file we need
			if(line.substr(0, 6) == "map_Kd"){
				texture->LoadTexture(filePath + line.substr(7));
				texture->Bind(0);
				//shader->SetUniformMatrix1i("u_Texture", 0);
			}
			else if(line.substr(0,8) == "map_Bump"){
				normalMap = new Texture();
				normalMap->LoadTexture_diff(filePath + line.substr(9));
				normalMap->Bind(1);
			}
		}
		
		file.close();
	}
}

void Object::addVertex(Vertex& v){
	
	bool present = false;
	
	//this is clearly very slow, but it gets the job done for now!
	int i;
	for (i=0; i<vertexData.size(); i++){
		if(v == vertexData.at(i)){
			present = true;
			break;
		}
	}

	indexData.push_back(i);
	if(!present){
		vertexData.push_back(v);
	}
	
}

void Object::GenerateBuffers(){
	
	//for now im just assuming vertex and texture
	buffer.CreateBuffer_vtn(vertexData, indexData);
	
	
}

void Object::Render(){
	
	buffer.Bind();
	if(texture != nullptr){texture->Bind(0);}
	if(normalMap != nullptr){normalMap->Bind(1);}
	glDrawElements(GL_TRIANGLES, indexData.size(), GL_UNSIGNED_INT, nullptr);  
	
}

//just my basic clicked function for demonstrative purposes
void Object::Clicked(){outline = !outline;}

void Object::MaxMinCoords(){
	
	//Imagine a cube around the object, with x/y/z coordinates at their
	//minimums and maximums. that is my goal with this function
	x_max = x_min = vertexData[0].x;
	y_max = y_min = vertexData[0].y;
	z_max = z_min = vertexData[0].z;
	
	for(int i = 1; i < vertexData.size(); i++){
		if(vertexData[i].x < x_min){x_min = vertexData[i].x;}
		if(vertexData[i].x > x_max){x_max = vertexData[i].x;}
		if(vertexData[i].y < y_min){y_min = vertexData[i].y;}
		if(vertexData[i].y > y_max){y_max = vertexData[i].y;}
		if(vertexData[i].z < z_min){z_min = vertexData[i].z;}
		if(vertexData[i].z > z_max){z_max = vertexData[i].z;}
	}
	

	
}

void Object::Clicked_RayIntersect(glm::vec3 viewPos, glm::vec3 mouseRay){
	//this function looks at the cube around the object and checks if the ray the mouse click is
	//sending into the screen will hit at least two of the sides of the cube

	bool pos_xy = false;
	bool neg_xy = false;
	bool pos_zy = false;
	bool neg_zy = false;
	//posOnPlane any point in plane
	//must do all this 6 times, negative normal as well
	glm::vec3 x_normal = glm::vec3(1.0f, 0.0f, 0.0f);
	glm::vec3 y_normal = glm::vec3(0.0f, 1.0f, 0.0f);
	glm::vec3 z_normal = glm::vec3(0.0f, 0.0f, 1.0f);
	
	//ray-plane intersect with positive xy plane bounding box
	float rDotn = dot(mouseRay, z_normal);
	float s = dot(z_normal, (glm::vec3(x_min,y_min,z_max) - viewPos)) / rDotn;
	glm::vec3 intersect = viewPos + s * mouseRay;
	if(x_min <= intersect.x && intersect.x <= x_max
	&& y_min <= intersect.y && intersect.y <= y_max
	&& z_min <= intersect.z && intersect.z <= z_max){
		pos_xy = true;
	}
	
	//ray-plane intersect with negative xy plane bounding box
	rDotn = dot(mouseRay, -z_normal);
	s = dot(-z_normal, (glm::vec3(x_min,y_min,z_max) - viewPos)) / rDotn;
	intersect = viewPos + s * mouseRay;
	if(x_min <= intersect.x && intersect.x <= x_max
	&& y_min <= intersect.y && intersect.y <= y_max
	&& z_min <= intersect.z && intersect.z <= z_max){
		neg_xy = true;
	}
	//ray-plane intersect with positive zy plane bounding box
	rDotn = dot(mouseRay, x_normal);
	s = dot(x_normal, (glm::vec3(x_min,y_min,z_max) - viewPos)) / rDotn;
	intersect = viewPos + s * mouseRay;
	if(x_min <= intersect.x && intersect.x <= x_max
	&& y_min <= intersect.y && intersect.y <= y_max
	&& z_min <= intersect.z && intersect.z <= z_max){
		pos_zy = true;
	}
	//ray-plane intersect with negative zy plane bounding box
	rDotn = dot(mouseRay, -x_normal);
	s = dot(-x_normal, (glm::vec3(x_min,y_min,z_max) - viewPos)) / rDotn;
	intersect = viewPos + s * mouseRay;
	if(x_min <= intersect.x && intersect.x <= x_max
	&& y_min <= intersect.y && intersect.y <= y_max
	&& z_min <= intersect.z && intersect.z <= z_max){
		neg_zy = true;
	}
	
	//this obviously means if you click straight on, it won't count,
	//but i just wanted to demonstrate accuracy (which I have failed at T_T)
	//i also did not test anything in the horizontal plane (y normals) for ease of demonstration,
	//especially since my camera doesn't go up and down yet
	if((pos_xy && pos_zy)
	|| (pos_xy && neg_zy)
	|| (neg_xy && pos_zy)
	|| (neg_xy && neg_zy)){
		outline = !outline;
	}
}

void Object::CalculateTangents(){
	
	//I finished my normal mapping from Assignment 5 :D
	for(int i = 0; i<indexData.size(); i+=3){
		
		Vertex v1 = vertexData[indexData[i+0]];
		Vertex v2 = vertexData[indexData[i+1]];
		Vertex v3 = vertexData[indexData[i+2]];
		
		glm::vec3 pos1 = glm::vec3(v1.x, v1.y, v1.z);
		glm::vec3 pos2 = glm::vec3(v2.x, v2.y, v2.z);
		glm::vec3 pos3 = glm::vec3(v3.x, v3.y, v3.z);
		
		glm::vec2 uv1 = glm::vec2(v1.s, v1.t);
		glm::vec2 uv2 = glm::vec2(v2.s, v2.t);
		glm::vec2 uv3 = glm::vec2(v3.s, v3.t);
		
		glm::vec3 edge1 = pos2 - pos1;
		glm::vec3 edge2 = pos3 - pos1;
		glm::vec2 deltaUV1 = uv2 - uv1;
		glm::vec2 deltaUV2 = uv3 - uv1;
		
		float f = 1.0f / (deltaUV1.x * deltaUV2.y - deltaUV2.x * deltaUV1.y);

		v1.tx = v2.tx = v3.tx = f * (deltaUV2.y * edge1.x - deltaUV1.y * edge2.x);
		v1.ty = v2.ty = v3.ty = f * (deltaUV2.y * edge1.y - deltaUV1.y * edge2.y);
		v1.tz = v2.tz = v3.tz = f * (deltaUV2.y * edge1.z - deltaUV1.y * edge2.z);

		v1.btx = v2.btx = v3.btx = f * (-deltaUV2.x * edge1.x + deltaUV1.x * edge2.x);
		v1.bty = v2.bty = v3.bty = f * (-deltaUV2.x * edge1.y + deltaUV1.x * edge2.y);
		v1.btz = v2.btz = v3.btz = f * (-deltaUV2.x * edge1.z + deltaUV1.x * edge2.z);
		
		if(v1.tx != 0 || v2.tx != 0 || v3.tx != 0
		|| v1.ty != 0 || v2.ty != 0 || v3.ty != 0
		|| v1.tz != 0 || v2.tz != 0 || v3.tz != 0
		|| v1.btx != 0 || v2.btx != 0 || v3.btx != 0
		|| v1.bty != 0 || v2.bty != 0 || v3.bty != 0
		|| v1.btz != 0 || v2.btz != 0 || v3.btz != 0){
			
		}
		
		
		
	}
	
	
}