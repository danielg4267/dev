// Standard Libraries
#include <string>
#include <fstream>
#include <cstring>
#include <iostream>

// User Libraries
#include "Color.hpp"
#include "Image.hpp"



Image::Image(unsigned int _width, unsigned int _height){
    width = _width;
    height = _height;
    // This creates a new dynamically allocated array
    // with each element initialized to 128.
    // This will produce a 'gray' canvas.
    m_pixelData = new unsigned char[width*height*3];
    memset(m_pixelData, 128, width*height*3);
}

// Destructor
Image::~Image(){
    delete[] m_pixelData;
}

// Sets an individual pixel to a color.
//
// Note: We are working with a 1-D array and
// each pixel consists of 3 values. There is a
// little conversion going on here.
//
// Another way to think of this is that 'width'
// is the pitch of an image, or how long a row is.
// y*width moves us down a row, and x moves us along
// that row. We multiply by 3, such that ColorRGB
// is a tuple with 3 values(ColorRGBA would be by 4).
// Finally, we increment appropriately to set r,g,b.
void Image::SetPixelColor(int x, int y, ColorRGB c){
    m_pixelData[((y*width+x)*3)] = c.r;
    m_pixelData[((y*width+x)*3)+1] = c.g;
    m_pixelData[((y*width+x)*3)+2] = c.b;
}

// Helper function to write out a .ppm image file
void Image::OutputImage(std::string fileName){
   std::ofstream myFile(fileName.c_str());
   if(myFile.is_open()){
        myFile << "P3" << "\n";
        myFile << "320 320" << "\n";
        myFile << "255" << "\n";       
        for(int i =0; i < width*height*3;i++){
            myFile << (int)m_pixelData[i] <<  " " << "\n";
        }
        myFile.close();
   }

}


