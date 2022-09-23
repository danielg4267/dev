#ifndef IMAGE_H
#define IMAGE_H
/** @file Image.h
 *  @brief Class for working with images
 *  
 *  Note this is implemented as a header only library.
 *  This is to make this code easy to be shared.
 *
 *  In practice we could extend this 'Image' class to handle
 *  format such as PPM or the Truevision Graphics Adapter(TGA or TARGA) 
 *  which is another relatively simple graphics format for drawing raster
 *  images.
 *
 *  Most art programs (photoshop, GIMP, Paint.Net, etc.) 
 *  are able to load imagse like PPM, TGA, BMP images.
 *
 *
 *  @author Mike Shah
 *  @bug No known bugs.
 */

// Standard Libraries
#include <string>
#include <fstream>

// User Libraries
#include "Color.hpp"

#include <cstring>

class Image{
public:
    
    // Constructor
    // This gives us a blank canvas to draw on.
    //
    Image(unsigned int _width, unsigned int _height);    
    // Destructor
    ~Image();

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
    void SetPixelColor(int x, int y, ColorRGB c);

    // Helper function to write out a .ppm image file
    void OutputImage(std::string fileName);
    

private:
    unsigned char* m_pixelData;
    unsigned int width{0};
    unsigned int height{0};

};

#endif
