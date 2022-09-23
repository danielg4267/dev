/** @file main.cpp
 *  @brief Entry point into our program.
 *  
 *  Welcome to the Great Looking Software Render 
 *  code base (Yes, I needed something with a gl prefix).
 *
 *  This is where you will implement your graphics API.
 *
 *  Compile on the terminal with: 
 *
 *  clang++ -std=c++17 main.cpp -o main
 *
 *  @author Mike Shah
 *  @bug No known bugs.
 */

// Load our libraries
#include <iostream>

// Some define values
#define WINDOW_HEIGHT 320
#define WINDOW_WIDTH 320

// C++ Standard Libraries
#include <iostream>

// User libraries
#include "GL.hpp"
#include "Color.hpp"
#include "Image.hpp"
#include "Maths.hpp"

#include <cmath>

// Create a canvas to draw on.
Image canvas(WINDOW_WIDTH,WINDOW_HEIGHT);

// Implementation of Bresenham's Line Algorithm
// The input to this algorithm is two points and a color
// This algorithm will then modify a canvas (i.e. image)
// filling in the appropriate colors.
void DrawLine(Vec2 v0, Vec2 v1, Image& image, ColorRGB c){
    bool steep = false;
    if(std::abs(v0.x-v1.x)<std::abs(v0.y-v1.y)){
        // If the line is steep we want to transpose the image.
        std::swap(v0.x,v0.y);
        std::swap(v1.x,v1.y);
        steep = true;
    }
    if(v0.x>v1.x){  // make it left-to-right
        std::swap(v0.x, v1.x);
        std::swap(v0.y, v1.y);
    }
    for(int x = v0.x; x <= v1.x; ++x){
        float t = (x-v0.x)/(float)(v1.x-v0.x);
        int y = std::round(v0.y*(1.0f-t) + v1.y*t);
        if(steep){
            canvas.SetPixelColor(y,x,c);
        }else{
            canvas.SetPixelColor(x,y,c);
        }
    }
}

/** Draws a triangle whose v0 vertex is the highest point of the triangle,
*   and whose v1 and v2 vertices have the same y value below it.
*   Uses Bresenham's Algorithm to draw lines from v0 -> v1 and v0->v2, 
*   while filling a horizontal line of pixels every step of the way. 
*	(I believe this is scan line rasterization)
*/
void FillFlatBottomTriangle(Vec2 v0, Vec2 v1, Vec2 v2,Image& image, ColorRGB c){
	 
	 //left to right
	 if(v1.x > v2.x){
		 std::swap(v1, v2);
	 }
	 
	 //if slope > 1 it's steep
	 float slope1 = (v0.y - v1.y)/(float)(v0.x - v1.x);
	 float slope2 = (v0.y - v2.y)/(float)(v0.x - v2.x);
	 
	 //start position
	 int y = v0.y;
	 int v1_current_y  = v0.y;
	 int v1_current_x = v0.x;
	 int v2_current_x = v0.x;
	 int v2_current_y = v0.y;
	 canvas.SetPixelColor(v1_current_x, y, c);
	 
	 //iterate downward
	 while(y > v1.y){

		 //if-else steps through v0 -> v1 line until y iterates by 1
		 //change in y > change in x, y will iterate by 1 after 1 iteration
		 if(std::abs(slope1) > 1){
			float t = (y-v0.y)/(float)(v1.y-v0.y);
			v1_current_x = std::round(v0.x*(1.0f-t) + v1.x*t);
			canvas.SetPixelColor(v1_current_x, y, c);
		 }
		 //change in x > change in y, iterate x by 1 until y has changed by 1
		 else{
			 while(v1_current_y == y){
				canvas.SetPixelColor(v1_current_x, v1_current_y, c);
				if(slope1 > 0){v1_current_x--;}
				else{v1_current_x++;}
				float t = (v1_current_x-v0.x)/(float)(v1.x-v0.x);
				v1_current_y = std::round(v0.y*(1.0f-t) + v1.y*t);
			 }
			 
		 }
		//if-else steps through v0 -> v2 line until y iterates by 1
		//change in y > change in x, y will iterate by 1 after 1 iteration
		 if(std::abs(slope2) > 1){
			float t = (y-v0.y)/(float)(v2.y-v0.y);
			v2_current_x = std::round(v0.x*(1.0f-t) + v2.x*t);
			canvas.SetPixelColor(v2_current_x, y, c);
			
		 }
		 //change in x > change in y, iterate x by 1 until y has changed by 1
		 else{
			 while(v2_current_y == y){
				canvas.SetPixelColor(v2_current_x, v2_current_y, c);
				if(slope2 > 0){v2_current_x--;}
				else{v2_current_x++;}
				float t = (v2_current_x-v0.x)/(float)(v2.x-v0.x);
				v2_current_y = std::round(v0.y*(1.0f-t) + v2.y*t); 
			 }
		 }
		 y--;
		 //draw horizontal line at current y value from left line to right line
		 for(int x = v1_current_x; x <= v2_current_x; x++){
			 canvas.SetPixelColor(x, y, c);
		 }
		 
	 }
}
/** Draws a triangle whose v0 vertex is the lowest point of the triangle,
*   and whose v1 and v2 vertices have the same y value above it.
*   Uses Bresenham's Algorithm to draw lines from v0 -> v1 and v0->v2, 
*   while filling a horizontal line of pixels every step of the way. 
*	(I believe this is scan line rasterization)
*/
void FillFlatTopTriangle(Vec2 v0, Vec2 v1, Vec2 v2,Image& image, ColorRGB c){
	
	//left to right
	if(v1.x > v2.x){
		 std::swap(v1, v2);
	 }
	 //if slope > 1 it's steep
	 float slope1 = (v0.y - v1.y)/(float)(v0.x - v1.x);
	 float slope2 = (v0.y - v2.y)/(float)(v0.x - v2.x);
	 
	 //start position
	 int y = v0.y;
	 int v1_current_y  = v0.y;
	 int v1_current_x = v0.x;
	 int v2_current_x = v0.x;
	 int v2_current_y = v0.y;
	 canvas.SetPixelColor(v1_current_x, y, c);
	 //iterate downward
	 while(y < v1.y){

		 //if-else steps through v0 -> v1 line until y iterates by 1
		 //change in y > change in x, y will iterate by 1 after 1 iteration
		 if(std::abs(slope1) > 1){
			float t = (y-v0.y)/(float)(v1.y-v0.y);
			v1_current_x = std::round(v0.x*(1.0f-t) + v1.x*t);
			canvas.SetPixelColor(v1_current_x, y, c);
		 }
		 //change in x > change in y, iterate x by 1 until y has changed by 1
		 else{
			 while(v1_current_y == y){
				canvas.SetPixelColor(v1_current_x, v1_current_y, c);
				if(slope1 > 0){v1_current_x++;}
				else{v1_current_x--;}
				float t = (v1_current_x-v0.x)/(float)(v1.x-v0.x);
				v1_current_y = std::round(v0.y*(1.0f-t) + v1.y*t);
			 }
			 
		 }
		//if-else steps through v0 -> v2 line until y iterates by 1
		//change in y > change in x, y will iterate by 1 after 1 iteration
		 if(std::abs(slope2) > 1){
			float t = (y-v0.y)/(float)(v2.y-v0.y);
			v2_current_x = std::round(v0.x*(1.0f-t) + v2.x*t);
			canvas.SetPixelColor(v2_current_x, y, c);
			
		 }
		 //change in x > change in y, iterate x by 1 until y has changed by 1
		 else{
			 while(v2_current_y == y){
				canvas.SetPixelColor(v2_current_x, v2_current_y, c);
				if(slope2 > 0){v2_current_x++;}
				else{v2_current_x--;}
				float t = (v2_current_x-v0.x)/(float)(v2.x-v0.x);
				v2_current_y = std::round(v0.y*(1.0f-t) + v2.y*t); 
			 }
		 }
		 y++;
		 //draw horizontal line at current y value from left line to right line
		 for(int x = v1_current_x; x <= v2_current_x; x++){
			 canvas.SetPixelColor(x, y, c);
		 }
		 
	 }
}

//sorts them from low to high 
void SortTriPoints(Vec2* v){
	
	//basically bubble sort since this is so small
	if(v[0].y >= v[1].y){
		Vec2 tmp = v[1];
		v[1] = v[0];
		v[0] = tmp;
	}
	if(v[1].y > v[2].y){
		Vec2 tmp = v[2];
		v[2] = v[1];
		v[1] = tmp;
	}
	if(v[0].y > v[1].y){
		Vec2 tmp = v[1];
		v[1] = v[0];
		v[0] = tmp;
	}
	
}


// Draw a triangle
void DrawTriangle(Vec2 v0, Vec2 v1, Vec2 v2,Image& image, ColorRGB c){
    if(glFillMode==LINE){
        DrawLine(v0,v1,image,c);
        DrawLine(v1,v2,image,c);
        DrawLine(v2,v0,image,c);
    }
	else{
		//sort to find middle-most point
		Vec2 v[4] = {v0, v1, v2};
		SortTriPoints(v);
		
		//it was a flat bottom
		if(v[0].y == v[1].y){
			FillFlatBottomTriangle(v2, v1, v0, image, c);
			return;
		}
		//it was a flat top
		else if(v[1].y == v[2].y){
			FillFlatTopTriangle(v0, v1, v2, image, c);
		}
		//other, needs to be split in to two triangles, one flat top one flat bottom
		else{
			
			//intercept theorem to find x value of midpoint 
			//on line opposite the middle vertex
			int x3 = std::round(v[2].x 
								+ (((float)(v[1].y - v[2].y)
								/(float)(v[0].y - v[2].y))
								*(v[0].x - v[2].x))); 
			Vec2 v3 = Vec2(x3, v[1].y);
			v[3] = v3;
			
			//draw two triangles
			FillFlatBottomTriangle(v[2], v[1], v[3], image, c);
			FillFlatTopTriangle(v[0], v[1], v[3], image, c);
		}
	}
}


// Main
int main(){

	//std::cout<<"OLO"<<std::endl;
    // A sample of color(s) to play with
    ColorRGB red;
    red.r = 255; red.g = 0; red.b = 0;
	
	ColorRGB blue;
	blue.r = 0; blue.g = 0; blue.b = 255;
	
	ColorRGB green;
	green.r = 0; green.g = 255; green.b = 0;
	
	ColorRGB pink;
	pink.r = 255; pink.g = 0; pink.b = 255;
            
    // Set the fill mode
    glPolygonMode(FILL);

	

    // Data for our triangles
    Vec2 tri[3] = {Vec2(160,60),Vec2(150,10),Vec2(75,190)};
	Vec2 tri2[3] = {Vec2(300,200),Vec2(280,110),Vec2(210,190)};
	Vec2 tri3[3] = {Vec2(5,5),Vec2(99,20),Vec2(10,300)};
	Vec2 tri4[3] = {Vec2(100,300),Vec2(120,180),Vec2(250,310)};

    // Draw triangles
    DrawTriangle(tri[0],tri[1],tri[2],canvas,red);
	DrawTriangle(tri2[0],tri2[1],tri2[2],canvas,blue);
	DrawTriangle(tri3[0],tri3[1],tri3[2],canvas,green);
	DrawTriangle(tri4[0],tri4[1],tri4[2],canvas,pink);

    // Output the final image
    canvas.OutputImage("graphics_lab.ppm");

    return 0;
}
