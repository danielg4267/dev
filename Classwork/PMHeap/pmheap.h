#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <pthread.h>
#include <string.h>

//5 pages max
//First level table
//Second level table
//Three data frames
#define HEAP_SIZE 1280
#define PAGE_SIZE 256

/**
Daniel Gonzalez
CS5600
Fall 2022
Practicum I
*/

//Virtual address pointer given to users by pm_malloc()
//Passed to pm_free() and pm_read/write(), must be translated
typedef uint32_t v_ptr;

//Metadata of a table entry, 8 bytes that will represent
//different situations. See README for more info
typedef uint64_t meta;

//Page pointer, a traditional pointer in memory
//Renamed for clarity
typedef void* p_ptr;

//A single byte, used to iterate through data byte by byte
typedef uint8_t byte_t;

//Static array of HEAP_SIZE bytes to represent the heap
uint8_t pm_heap[HEAP_SIZE];
//Simulating the CR3 register that stores a pointer to the first level page table
p_ptr cr3;

//MMU always knows where free memory is and first item in queue of entries to evict
typedef struct mmu{
	p_ptr free;
	byte_t q_1;
	byte_t q_2;
}mmu_t;
mmu_t mmu_cache;

//Size of a page table entry (should be 16 bytes)
size_t pte_size = sizeof(meta) + sizeof(p_ptr);

//Offset unavailable, ie "NULL" for a virtual pointer offset (0 is a valid offset)
byte_t o_unavail;

//Variables used to make the heap thread safe
pthread_mutex_t m;
pthread_cond_t C1;

//Metadata is an array of bytes indexed by these values
int present, next_alloc, access, dirty, 
	next_f, next_s, prev_f, prev_s;

//v_ptr is an array of bytes indexed by these values
int f_offset, s_offset, d_offset, extra;

/*****************************
*
*		HELPER FUNCTIONS
* Functions that don't have anything 
* specifically to do with the heap,
* they are small and just help to implement
* it properly. Cleans up the code.
*
*
*****************************/

//Helper function, checks if system is little endian
char little_e();
//Helper function, checks if a pointer is within heap bounds
unsigned char valid(p_ptr page);
//Makes sure offsets in ptr are within bounds of max number of entries per page (16)
v_ptr normalize_offsets(v_ptr ptr);
//Initializes indexes for metadata and v_ptr
void init_const();

/*****************************
*
*	PAGE MANAGEMENT FUNCTIONS
* Functions that initialize regions
* of the heap for different purposes
* when calling free, malloc, access, etc.
*
*
*****************************/

//Initializes the heap by creating stacks of free pages and initializing CR3
void init_heap();
//Sets up the memory starting at the pointer given to be free and adds it to the stack
void init_free(p_ptr page);
//Finds a free page (evicts one if necessary) and removes it from the stack
p_ptr init_alloc();
//Finds a free page and initializes the data to be used as a page table
p_ptr init_table();

/*****************************
*
*	CLOCK PAGE SWAP FUNCTIONS
* Functions whose sole purpose is
* to implement CLOCK page swapping.
* Evict a page, access a page, load
* them into and out of memory, etc.
*
*
*****************************/

//Iterates through the circular queue and writes a page to disk
void evict_page();

//Writes the page in memory referred to by the entry at the given offsets to a disk file
void mem_to_disk(byte_t offset_1, byte_t offset_2);

//Writes the page on disk referred to by the entry at the given offsets back to memory
p_ptr disk_to_mem(byte_t offset_1, byte_t offset_2);

//Adds the given page entry to the CLOCK queue
void enqueue(byte_t offset_1, byte_t offset_2);

//Removes the given page entry from the CLOCK queue
void dequeue(byte_t offset_1, byte_t offset_2);

//Finds the given page, whether it is in memory or on disk
p_ptr access_page(byte_t offset_1, byte_t offset_2);

/*****************************
*
*	HEAP INTERACTION FUNCTIONS
* Functions the user would use to 
* interact with the heap. The only functions
* that the user should have access to.
*
*
*****************************/

//Write data to the heap area given by the pointer. 
//Requires pointer to first byte of data
void pm_write(v_ptr ptr, byte_t* data, size_t size);

//Reads data from the heap into a buffer (could be an int, an array, anything)
void pm_read(v_ptr ptr, void* buffer, size_t size);

//Frees data at the region given by the pointer
void pm_free(v_ptr ptr);

//Allocates data from the heap for the given size
v_ptr pm_malloc(int size);