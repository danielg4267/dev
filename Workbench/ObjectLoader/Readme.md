# Object Loader

This started out as a final project for my computer graphics class. I wanted to try a number of things. Specifically, I wanted to render objects with multiple shaders and textures, as well as try out a toon shader. Adding more than I probably should have to my list of features, I also wanted to be able to click and highlight objects. I quickly discovered highlighting an object is very hard, let alone being able to click on one using ray tracing. The goal was to learn, however, and I certainly did (and still am!). Now, I just want to make a complete object loader for fun.

# Credits

"build.py" was written by my Computer Graphics professor at Northeastern University, Mike Shah, and everything in the "common" folder was provided by him. The folder simply contains libraries and example assets needed for this to run. I've included them all here, for easy download and use if you choose to run this program.

Everything in "include", "shaders", and "src" is my own work.

# TODO

##Bugs
-Fix implementation of highlighted objects
-Normal-mapped textures render incorrectly as the camera approaches
-Objects with too many vertices load slowly

##Features
-Open other .obj files
-Open .obj files made with multiple pieces and textures
-User defined lighting