/*
 * Daniel Gonzalez
 * CS5008
 * Summer 2021
 * Lab 6 - Dijkstra's Algorithm Header File
 *
 * This file contains all of the declarations of functions
 * used in this program, and the comments explaining how they work.
 *
 */

#ifndef __LAB6_H
#define __LAB6_H
#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <limits.h>

//Longest a city name can be
#define CITYLENGTH 20

//file name to use
#define FILENAME "city.dat"

//largest input user can give
#define MAXCHAR 255

/**************************************
 *          DEFINITIONS
 *************************************/

/* 
 * Represents a city, holds an array of char (string)
 * for its name, an integer for distance, and an 
 * integer representing the index of the previous
 * node on its path.
 */
typedef struct city{
	char cityName[CITYLENGTH];
	int distance;
	int previous;
} data_t;

/*
 * Dynamic array struct holds data_t
 */
typedef struct {
    data_t *array;
    size_t capacity;
    size_t size;
    size_t front;
} dynarray_t;

/*
 * smallestDist() takes a dynamic array and returns the
 * index of the data_t struct with the smallest distance value.
 * Returns the first index it finds with the smallest value.
 */
int smallestDist(dynarray_t* unexplored);

/*
 * copyArray() takes a pointer to two dynamic arrays,
 * and copies all the elements from the source array
 * to the copy array. Uses dynarray_enqueue()
 */
void copyArray(dynarray_t* source, dynarray_t* copy);

/*
 * resetDistances() takes a dynamic array of cities and
 * resets all of their distance attributes to infinity
 */
void resetDistances(dynarray_t* cities);

/*
 * dijkstra() runs Dijkstra's algorithm on an dynamic array of cities, given the
 * dynamic array, the index of the source city, the index of the destination city, the 
 * size of the array, and the adjacency matrix representing the connections between them.
 * Returns the integer of the shortest path. Updates info in the dynarray as it goes.
 */
int dijkstra(dynarray_t* cities, int source, int dest, size_t size, int distances[][size]);

/*
 * readDistances() opens a file, corresponds cities it finds with indexes in
 * a dynamic array, and saves the distances between them in the matching indexes
 * in an adjacency matrix.
 */
void readDistances(size_t size, int distances[][size], dynarray_t* cities);

/*
 * readNames() opens a file and saves the cities it finds in a dynamic array
 * of data_t. Does not add duplicates, and does not save distances between
 * cities.
 */
void readNames(dynarray_t* cities);

/*
 * Checks that a string of characters
 * is only a string of letters. Returns true
 * if it is, false otherwise.
 */
bool isValidName(char* string);

/*
 * saveCity() takes a char array and a data_t pointer
 * and saves as much of the string as the data_t struct 
 * can allow.
 */
void saveCity(char* name, data_t* city);


/* 
 * getIndex() takes a city name (an array of char) and 
 * searches for that city in a dynamic array of cities.
 * Returns the index it is found in, -1 if it is not found.
 */
int getIndex(char* name, dynarray_t* cities, size_t size);

/*
 * selectionSort takes a dynamic array of cities and sorts
 * them alphabetically by their name. Mutates the original
 * array.
 */
void selectionSort(dynarray_t* dynarray, size_t arrayLength);

/*
 * dynarray_remove() takes a dynamic array pointer and an index,
 * and removes the element at that index. Shifts the other 
 * elements in the array. Returns the removed data_t element.
 */
data_t dynarray_remove(dynarray_t* a, int index);

/*
 * printMatrix() takes an adjacency matrix and its size,
 * and prints the contents of the matrix. Good for checking
 * inputs are saved correctly.
 */
void printMatrix(size_t size, int matrix[][size]);

/*
 * printPath() takes the dynamic array of cities as well
 * as the index of the destination city, and iterates
 * through their path and prints out the result.
 */
void printPath(dynarray_t* cities, int dest);

/**************************************
 *             Lab 5 Dynamic Array 
 *             Provided Functions 
 *         (The ones I explicitly used)
 *************************************/

void dynarray_init(dynarray_t* a);
void dynarray_free(dynarray_t* a);

void dynarray_enqueue(dynarray_t* a, data_t item);
data_t dynarray_dequeue(dynarray_t* a);

void dynarray_push(dynarray_t*, data_t item);
data_t dynarray_pop(dynarray_t* a);

#endif
