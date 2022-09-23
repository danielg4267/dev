/**
*	Daniel Gonzalez
*	CS5310 - Final Project
*	VertexBufferLayout - this class creates buffers of data
*	to be sent to the GPU.
*/

#include <glad/glad.h>
#include <vector>

struct Vertex{
	
	//vertex position coordinates
	float x,y,z;
	//texture coordinates for diffuse and normal maps
	float s,t;
	//normal values per vertex (for flat shading) - i didnt know what to name them!
	float nx, ny, nz;
	//tangents
	float tx, ty, tz;
	//bitangents
	float btx, bty, btz;

	Vertex(float _x, float _y, float _z, float _s, float _t, float _nx, float _ny, float _nz): 
			x(_x),y(_y),z(_z),s(_s),t(_t), nx(_nx), ny(_ny), nz(_nz) {tx = ty = tz = btx = bty = btz = 0;}
	
	//the tangents and bitangents don't really need to be compared in the cases of this program,
	//but it's something I'm thinking about changing for the future, I'm not sure if it would matter or not
	bool operator== (const Vertex &rhs){
		if( (x == rhs.x) && (y == rhs.y) && (z == rhs.z) && 
			(s == rhs.s) && (t == rhs.t) && 
			(nx == rhs.nx) && (ny == rhs.ny) && (nz == rhs.nz) ){
			return true;
		}
		return false;
	}
};

class VertexBufferLayout{
	
	public:
		VertexBufferLayout();
		~VertexBufferLayout();
		
		//different types of buffer layouts
		
		//only vertex data
		void CreateBuffer_v();
		
		//vertex and texture data
		void CreateBuffer_vt(std::vector<Vertex>& vertexData, std::vector<unsigned int>& indexData);
		
		//vertex, texture, and normal data
		void CreateBuffer_vtn(std::vector<Vertex>& vertexData, std::vector<unsigned int>& indexData);
		
		//binds the buffer objects we've created
		void Bind();
		
	private:
	
		GLuint VBO;
		GLuint IBO;
		GLuint VAO;
	
};