/*
 * Daniel Gonzalez
 * CS5008
 * Summer 2021
 * Lab 6 - Dijkstra's Algorithm Driver File
 *
 * This is the driver file that utilizes the implementation
 * of Dijkstra's Algorithm and its helper functions to
 * obtain path data from a file, save it, print out a user's
 * options, take in the user's options, and run the algorithm
 * until the user quits.
 *
 */

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "lab6.h"


int main() {


	//create dynarray of city structs
	dynarray_t cities;
	dynarray_init(&cities);
	
	//save names and sort
	readNames(&cities);
	size_t size = cities.size;
	selectionSort(&cities, size);

	//All distance values start at 0
	int distances[cities.size][cities.size];
	int i;
	for(i=0; i<cities.size; i++){
		int j;
		for(j=0; j<cities.size; j++){
			distances[i][j] = 0;
		}
	}
	//input distances where applicable
	readDistances(cities.size, distances, &cities);
	char exit[2] = {'0', '\n'};
	char input[MAXCHAR];

	//ends when user chooses to break the loop
	while(true){
		int source = -1;
		int dest = -1;
		printf("\n");

		//get input for origin, runs until valid input or quit
		while (source < 0 || cities.size <= source){
			printf("Please select an origin city\n");
			printf("Enter a number associated with one of the cities below:\n\n");
			for(i=0; i<size; i++){
				printf("%2d ---- %s\n", i+1, cities.array[i].cityName);
			}
			printf("%2d ---- QUIT\n\n", 0);
			fgets(input, MAXCHAR, stdin);

			source = atoi(input);
			
			//exit
			if (strcmp(input, exit) == 0){
				printf("Exiting...\n");
				dynarray_free(&cities);
				return 0;
			}
			source --; //to get actual index
			printf("\n");
			
		}

		//get input for destination, runs until valid input or quit
		while (dest < 0 || cities.size - 1 < dest){
			printf("Please select a destination city\n");
			printf("Enter a number associated with one of the cities below:\n\n");
			for(i=0; i<size; i++){

				//if block lets us skip the chosen origin city
				if(i==source && !(i+1 >= size-1)){
					i++; //skip it
					printf("%2d ---- %s\n", i, cities.array[i].cityName);
				}
				else if(i > source){
					printf("%2d ---- %s\n", i, cities.array[i].cityName);
				}
				else if(i < source){
					printf("%2d ---- %s\n", i+1, cities.array[i].cityName);
				}
			}
			printf("%2d ---- QUIT\n\n", 0);
			fgets(input, MAXCHAR, stdin);
			dest = atoi(input);

			//exit
			if(strcmp(input, exit) == 0){
				printf("Exiting...\n");
				dynarray_free(&cities);
				return EXIT_SUCCESS;
			}
			//for proper index, since nothing shifted below source
			if (dest <= source){
				dest--;
			}
			printf("\n\n");
						
		}

		//INPUTS OBTAINED, RUN ALGORITHM, PRINT PATH
		printf("ORIGIN: %s\nDESTINATION: %s\n", cities.array[source].cityName, 
							    cities.array[dest].cityName); 

		int shortest;
		shortest = dijkstra(&cities, source, dest, cities.size, distances);
		printf("PATH LENGTH: %d\n", shortest);
		printPath(&cities, dest);
		printf("\n");
	}
	
	dynarray_free(&cities);	
	return EXIT_SUCCESS;
}
