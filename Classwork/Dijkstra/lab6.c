/*
 * Daniel Gonzalez
 * CS5008
 * Summer 2021
 * Lab 6 - Dijkstra's Algorithm Implementation
 *
 * This file contains the implementation of all the functions
 * needed to read the input file, save its data, and run 
 * Dijkstra's Algorithm. There are more detailed summaries
 * of these functions in the header file, lab6.h
 *
 */

#include "lab6.h"

const int DEFAULT_DYNARRAY_CAPACITY = 2;

/**************************************
 *         ADDED FUNCTIONS
 *************************************/

/*Iterates through the cities array based on the city's "previous" attribute,
 *  prints out the cities it finds*/
void printPath(dynarray_t* cities, int dest){
	
	dynarray_t path;
	dynarray_init(&path);
	
	//add every previous city to the array
	int prev = dest;
	while(prev >= 0){
		dynarray_push(&path, cities->array[prev]);
		prev = cities->array[prev].previous;
	}

	printf("PATH CITIES:\n");

	//print elements backwards (since they were added backwards)
	int i;
	for(i=path.size-1; i>=0; i--){
		printf("%s\n", path.array[i].cityName);
	}
	
	dynarray_free(&path);

}

/*Prints the values found in the adjacency matrix*/
void printMatrix(size_t size, int matrix[][size]){
        
	//iterate through rows
	int i;
        for(i=0; i<size; i++){
                printf("City: %d\n", i);
                
		//iterate through columns
		int j;
                for(j=0; j<size; j++){
                        printf("Connect: %d ", j);
                        printf("Distance: %d\n", matrix[i][j]);

                }
                printf("\n");
        }
}

/* Returns index of the city with the smallest distance attribute*/
int smallestDist(dynarray_t* unexplored){
	
	//initialize to first element to start
	int smallest = unexplored->array[0].distance;
	int smallIndex = 0;
	
	//find smallest saved distance in array
	int i;
	for(i=0; i<unexplored->size; i++){
		if(unexplored->array[i].distance < smallest){
			smallest = unexplored->array[i].distance; 
			smallIndex = i;
		}	
	}

	return smallIndex;

}
/*Copies elements from source array to copy array using dynarray_enqueue().*/
void copyArray(dynarray_t* source, dynarray_t* copy){
	
	//iterates and copies elements to new array
	int i;
	for(i=0; i<source->size; i++){
		dynarray_enqueue(copy, source->array[i]);
	}

}

/*Sets distance attribute of all elements in dynarray to INT_MAX (infinity)
 * and all "previous" index pointers back to -1.*/
void resetDistances(dynarray_t* cities){

	//iterates, sets all distances to "infinity"
	int i;
	for(i=0; i<cities->size; i++){
		cities->array[i].distance = INT_MAX;
		cities->array[i].previous = -1;
	}

}

/*Calculates the shortest path from source to destination city based on adjacency matrix
 * of distances/connections between cities*/
int dijkstra(dynarray_t* cities, int source, int dest, size_t size, int distances[][size]){
	
	//make sure all distances are infinity
	resetDistances(cities);
	
	//queue of unexplored nodes
	dynarray_t unexplored;
	dynarray_init(&unexplored);
	copyArray(cities, &unexplored);
	
	//set source distance to 0 in both
	cities->array[source].distance = 0;
	unexplored.array[source].distance = 0;


	while(unexplored.size > 0){ //when it's empty, all are explored
		
		//search for closest currently unexplored city
		int node = smallestDist(&unexplored);
		data_t city = dynarray_remove(&unexplored, node); //remove, explore its options below
		
		//short circuit, unconnected node!
		if(city.distance == INT_MAX){
			continue; 
		}

		//obtain index in adj matrix of this node
		int index = getIndex(city.cityName, cities, size);
		if(index == dest){
			break; //no need to search more paths
		}
		//for all neighbors (distance>0 = neighbor) of city:
		int i;
		for(i=0; i<size; i++){
			if(distances[index][i] > 0){ 		
				
				//potential new path vs current path of neighbor
				int alternate = city.distance + distances[index][i];
				int shortest = cities->array[i].distance;
				if (alternate < shortest){

					//new path found to neighbor, update city's info
					cities->array[i].distance = alternate;
					cities->array[i].previous = index;
					//get neighbor's index in unexplored, update there as well
					int index2 = getIndex(cities->array[i].cityName, &unexplored, unexplored.size);
					unexplored.array[index2].distance = alternate;
				}

			}
		}

	}

	dynarray_free(&unexplored);
	return cities->array[dest].distance;	


}

/*Opens city.dat file, saves distances in adjacency matrix based on indexes
 * in dynamic array and connections between cities*/
void readDistances(size_t size, int distances[][size], dynarray_t* cities){

	FILE* cityFile = fopen(FILENAME, "r");
	if (cityFile == NULL){
		printf("File not found.");
		exit(EXIT_FAILURE);
	}

	char line[255];	
	
	//if line is empty, loop ends
	while(fgets(line, sizeof(line), cityFile)){
			
		int index1 = -1;
		int index2 = -1;
		char* name = strtok(line, " ");
		
		//reach end of line, loop ends
		while(name != NULL){
			
			//index1 already found (second city in line)
			if (index1 > -1 && index2 < 0){
				index2 = getIndex(name, cities, size);
			}
			//first city in line
			else if(index1 < 0){
				index1 = getIndex(name, cities, size);
			}
			
			
			int distance = atoi(name); //will be 0 until cursor reaches distance (last part of line)
			
			//all parts defined, save values
			if(index1 > -1 && index2 > -1 && distance > 0){
				distances[index1][index2] = distance;
				distances[index2][index1] = distance; //save both!
				
			}
			//cont through line
			name = strtok(NULL, " ");
		}
	}
	fclose(cityFile);

}

/*Checks that an array of characters only contains letters*/
bool isValidName(char* string){

	//iterates through string, makes sure ALL parts are letters
	int i;
	for(i=0; i<strlen(string); i++){	
		if((string[i] < 65) 
		|| (90 < string[i] && string[i] <97) 
		|| (string[i] > 122)){

			return false; //found something weird
		}
	
	}
	return true;

}

/*Opens city.dat, saves any unique names it finds in dynarray*/   
void readNames(dynarray_t* cities){
	
	FILE* cityFile = fopen(FILENAME, "r");
	if(cityFile == NULL){
		printf("File not found.");
		exit(EXIT_FAILURE);
	}

	char line[MAXCHAR];

	//loop line by line in file until an empty line (end of file)
	while (fgets(line, sizeof(line), cityFile)){
		
		char* name = strtok(line, " ");
		
		//loop ends at the end of a line
		while(name != NULL){
			data_t city;
			size_t size = cities->size;
	
			//is an actual name, and is not in the array yet -> save it!
			if(isValidName(name) && getIndex(name, cities, size)<0){
				saveCity(name, &city); 
				dynarray_push(cities, city);
			}
			name = strtok(NULL, " ");	
			
		}
	
	}
	
	fclose(cityFile);

}

/*Uses a string of characters and saves them in a data_t struct*/
void saveCity(char* name, data_t* city){

	//iterate through string, save characters
	int i;
	for(i=0; i<strlen(name); i++){

		if (i< CITYLENGTH-1 && name[i] != '\n'){
			city->cityName[i] = name[i];
		}
		else{
			break; //stop before entire cityName is full
		}
	}
	//null terminate the string, avoid weird data
	while(i < CITYLENGTH){
		city->cityName[i] = '\0';
		i++;
	}

	//initialize to infinity
	city->distance = INT_MAX;
	city->previous = -1;

}

/*Searches for the index of a city using its name, returns -1 if not found*/
int getIndex(char* name, dynarray_t* cities, size_t size){
	
	int index = -1;
	size_t i;
	
	//iterate through array, match name 
	for(i=0; i<size; i++){
		char* city = cities->array[i].cityName;
		//found, stop and return index
		if (strcmp(name, city) ==0){
			index = i;
			return index;
		}
	}
	//return -1, not found
	return index;


}


/*Uses selection sort algorithm to sort a dynamic array of cities alphabetically
 * by name*/
void selectionSort(dynarray_t* dynarray, size_t arrayLength){

	data_t* array = dynarray->array;

        int i;
        for (i=0; i<arrayLength; i++){

                data_t smallest = array[i]; //to start
                data_t* smallest_p = &array[i]; //used for comparison/swap later

                int j;
                for (j = i;  j<arrayLength; j++){ //Run through unsorted items
			
			//this one is alphabetically first
                        if (strcmp(array[j].cityName, smallest.cityName)<0){
			     	smallest = array[j];
                                smallest_p = &array[j];
                        }
                }

		//Compare indexes, not values, to make sure swap is necessary
                if (smallest_p != &array[i]){
                        *smallest_p = array[i]; //swap smallest with array[i]
                        array[i] = smallest; //swap array[i] with smallest
                }
        }
}


/*Removes an element at the chosen index of the array. Shifts affected indexes*/
data_t dynarray_remove(dynarray_t*a, int index){

        assert(a->size >0);
        data_t value = a->array[index];
	
	//iterate through everything after removed element
        int i;
        for (i=index; i< a->size-1; i++){
                a->array[i] = a->array[i+1]; //shift to the left
        }
        a->size --;
        a->front = a->front-1;
        return value;

}




/**************************************
 *         END DANIEL'S CODE
 *		   BEGIN PROFESSOR'S CODE
 *************************************/


void dynarray_init(dynarray_t *a) {

    /* allocate space for data */
    a->array = (data_t*)malloc(DEFAULT_DYNARRAY_CAPACITY * sizeof(data_t));
    if (a->array == NULL) {
        fprintf(stderr, "ERROR: Cannot allocate memory for dynamic array.");
        exit(-1);
    }

    /* initialize other metadata */
    a->capacity = DEFAULT_DYNARRAY_CAPACITY;
    a->size = 0;
    a->front = 0;
}

void dynarray_expand(dynarray_t *a, size_t new_capacity) {

    size_t i;

    /* allocate new array */
    data_t *new_array = (data_t*)malloc(new_capacity * sizeof(data_t));
    if (!new_array) {
        fprintf(stderr, "ERROR: Cannot allocate memory for dynamic array.");
        exit(-1);
    }

    /* copy items to new array */
    for (i = 0; i < a->size; i++) {
        new_array[i] = a->array[(a->front + i) % a->capacity];
    }

    /* delete old array and clean up */
    free(a->array);
    a->array = new_array;
    a->capacity = new_capacity;
    a->front = 0;
}


size_t dynarray_size(dynarray_t *a) {

    return a->size;
}

size_t dynarray_is_empty(dynarray_t *a) {

    return (a->size == 0);
}

void dynarray_free(dynarray_t *a) {

    free(a->array);
    a->array    = NULL;
    a->capacity = 0;
    a->size     = 0;
}


void dynarray_push(dynarray_t *a, data_t item) {

    if (a->size+1 > a->capacity) {
        dynarray_expand(a, a->capacity*2);          /* expand if necessary */
    }
    a->array[a->size++] = item;
}

data_t dynarray_pop(dynarray_t *a) {

    assert(a->size > 0);
    return a->array[--(a->size)];
}

data_t dynarray_top(dynarray_t *a) {

    assert(a->size > 0);
    return a->array[a->size-1];
}

void dynarray_enqueue(dynarray_t *a, data_t item) {

    if (a->size+1 > a->capacity) {
        dynarray_expand(a, a->capacity*2);          /* expand if necessary */
    }
    a->array[(a->front + a->size) % a->capacity] = item;
    a->size++;
}

data_t dynarray_dequeue(dynarray_t *a) {

    assert(a->size > 0);
    data_t value = a->array[a->front];
    a->front = (a->front+1) % a->capacity;
    a->size--;
    return value;
}

data_t dynarray_front(dynarray_t *a) {

    assert(a->size > 0);
    return a->array[a->front];
}


