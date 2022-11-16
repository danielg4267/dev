#include "pmheap.h"

/**
Daniel Gonzalez
CS5600
Fall 2022
Practicum I
*/

//Not used in program logic, just a way to print results of various functions
FILE* fptr;

char little_e(){
	
	int n = 1;
	//If little endian, reading the first byte will be 1
	return (*(char *)&n == 1);
}

unsigned char valid(p_ptr page){
	
	if(page >= (p_ptr)pm_heap 
	&& page < (p_ptr)(pm_heap + HEAP_SIZE)){
		return 1;
	}
	return 0;
}

v_ptr normalize_offsets(v_ptr ptr){
	
	//Deconstruct pointer
	byte_t* offsets = (byte_t*)&ptr;
	byte_t offset_1 = offsets[f_offset];
	byte_t offset_2 = offsets[s_offset];
	byte_t offset_3 = offsets[d_offset];
	
	int max_entries = PAGE_SIZE/pte_size;
	
	//Iterate and update offset_1 and offset_2
	while(offset_2 > max_entries){
		offset_2 -= max_entries;
		offset_1 ++;
	}
	
	//Put it back together and return it
	byte_t final[4];
	final[d_offset] = offset_3;
	final[s_offset] = offset_2;
	final[f_offset] = offset_1;
	final[extra] = 0;
	return *((v_ptr*)&final);
	
	
}

void init_const(){
	//Indexes to construct v_ptr from bytes
	if(little_e()){
		d_offset = 0;
		s_offset = 1;
		f_offset = 2;
		extra = 3;
	}
	else{
		d_offset = 3;
		s_offset = 2;
		f_offset = 1;
		extra = 0;
	}
	//Indexes for metadata
	present = 0;
	next_alloc = 1;
	access = 2;
	dirty = 3;
	next_f = 4;
	next_s = 5; 
	prev_f = 6; 
	prev_s = 7;
	
	//Max value for a byte, offsets should never reach this value
	o_unavail = 255;
}

void init_heap(){
	
	init_const();
	mmu_cache.free = NULL;
	mmu_cache.q_1 = o_unavail;
	mmu_cache.q_2 = o_unavail;
	
	//Start at the end, iterate backwards and add pages to stack
	p_ptr page = (p_ptr)(pm_heap + HEAP_SIZE - PAGE_SIZE);
	while(valid(page)){
		init_free(page);
		page -= PAGE_SIZE;
	}
	
	//First level page table
	cr3 = init_table();
	
}

void init_free(p_ptr page){
	
	if(valid(page)){
		//Zero-out the entire page
		memset(page, 0, PAGE_SIZE);
		//Write pointer to next in page, push page to stack
		*(p_ptr*)page = mmu_cache.free;
		mmu_cache.free = page;
	}
	
}

p_ptr init_alloc(){
	//Get an allocated page ready, evict page if necessary
	p_ptr page;
	if(!mmu_cache.free){
		evict_page();
	}
	//Remove page from stack
	page = mmu_cache.free;
	mmu_cache.free = *(p_ptr*)page;
	return page;
	
}

p_ptr init_table(){
	
	//Take page from top of stack
	p_ptr page = init_alloc();
	
	//Iterate through memory of page, set each entry to 0
	int max_entries = PAGE_SIZE / pte_size;
	meta metadata = 0;
	byte_t* entry;
	int i;
	for(i=0; i<max_entries; i++){
		entry = (byte_t*)page + (i * pte_size);
		*(meta*)entry = metadata;
		//Set queue data to invalid values (0 is a valid queue value!)
		entry[next_f] = entry[next_s] = entry[prev_f] = entry[prev_s] = o_unavail;
	}
	return page;
	
	
	
}


void evict_page(){
	
	//MMU knows the start of the queue
	byte_t offset_1 = mmu_cache.q_1;
	byte_t offset_2 = mmu_cache.q_2;
	byte_t* entry_1;
	p_ptr* table_2;
	byte_t* entry_2;
	
	//Make sure there is a queue to iterate to before doing this!
	if(mmu_cache.q_1 != o_unavail && mmu_cache.q_2 != o_unavail){
		fprintf(fptr,"Evict page called, seeking page to evict.\n");
		//Start entry
		entry_1 = (byte_t*)cr3 + (offset_1 * pte_size);
		table_2 = (p_ptr*)(entry_1 + sizeof(meta));
		entry_2 = (byte_t*)(*table_2) + (offset_2 * pte_size);
		
		//Iterate through each entry, set access to 0
		while(entry_2[access]){
			fprintf(fptr,"Offset %u %u entry access = %u.\n", offset_1, offset_2, entry_2[access]);
			entry_2[access] = 0;
			
			offset_1 = entry_2[prev_f];
			offset_2 = entry_2[prev_s];
			
			entry_1 = (byte_t*)cr3 + (offset_1 * pte_size);
			table_2 = (p_ptr*)(entry_1 + sizeof(meta));
			entry_2 = (byte_t*)(*table_2) + (offset_2 * pte_size);
		}
		fprintf(fptr,"Offset %u %u entry access = %u.\n", offset_1, offset_2, entry_2[access]);
		//Page was not accessed recently enough, write to disk
		mem_to_disk(offset_1, offset_2);
	}
}

void mem_to_disk(byte_t offset_1, byte_t offset_2){
	
	//Find page at given offset
	byte_t* entry_1 = (byte_t*)cr3 + (offset_1 * pte_size);
	p_ptr* table_2 = (p_ptr*)(entry_1 + sizeof(meta));
	byte_t* entry_2 = (byte_t*)(*table_2) + (offset_2 * pte_size);
	p_ptr page = *(p_ptr*)(entry_2 + sizeof(meta));
	
	//Something went terribly wrong, kill the program
	if(entry_2[present] != 1){printf("ENTRY IS NOT VALID\n");exit(-1);}
	
	//Create filename based on offsets
	FILE* outfile;
	char filename[16];
	sprintf(filename, "./.swap/%02u%02u.bin", offset_1, offset_2);
	
	outfile = fopen(filename, "w");
	//Write entire page to file
	fwrite(page, sizeof(byte_t), PAGE_SIZE, outfile);
	fclose(outfile);
	
	//Page is now available, entry is now on disk
	dequeue(offset_1, offset_2);
	init_free(page);
	entry_2[present]++;
	fprintf(fptr,"ENTRY AT OFFSETS %u %u WRITTEN TO DISK IN FILE %s\n", offset_1, offset_2, filename);
	
	
	
}

p_ptr disk_to_mem(byte_t offset_1, byte_t offset_2){
	
	//Get a new page ready!
	p_ptr page = init_alloc();
	
	//Find filename based on offsets and read it into page
	FILE* infile;
	char filename[16];
	sprintf(filename, "./.swap/%02u%02u.bin", offset_1, offset_2);
	infile = fopen(filename, "r");
	fread((void*)page, PAGE_SIZE, 1, infile);
	
	//Move to entry given by offsets
	byte_t* entry_1 = (byte_t*)cr3 + (offset_1 * pte_size);
	p_ptr* table_2 = (p_ptr*)(entry_1 + sizeof(meta));
	byte_t* entry_2 = (byte_t*)(*table_2) + (offset_2 * pte_size);
	
	//Set entry's page pointer to the newly written page
	*(p_ptr*)(entry_2 + sizeof(meta)) = page;
	enqueue(offset_1, offset_2);
	
	fclose(infile);
	remove(filename);
	
	fprintf(fptr,"ENTRY AT OFFSETS %u %u READ FROM DISK IN FILE %s\n", offset_1, offset_2, filename);
}

void iterate(){
	printf("Printing queue\n");
	byte_t offset_1 = mmu_cache.q_1;
	byte_t offset_2 = mmu_cache.q_2;
	byte_t* entry_1;
	p_ptr* table_2;
	byte_t* entry_2;
	if(mmu_cache.q_1 != o_unavail && mmu_cache.q_2 != o_unavail){
	
	//in the future, while(entry_2[access]){entry_2[access] = 0; iterate}
		int i = 0;
		while(i < 10){
			printf("%u %u\n", offset_1, offset_2);
			entry_1 = (byte_t*)cr3 + (offset_1 * pte_size);
			table_2 = (p_ptr*)(entry_1 + sizeof(meta));
			entry_2 = (byte_t*)(*table_2) + (offset_2 * pte_size);
			
			offset_1 = entry_2[prev_f];
			offset_2 = entry_2[prev_s];
			i++;
		}
	}
	
}

void enqueue(byte_t offset_1, byte_t offset_2){

	//Queue is empty, add this to the front
	if(mmu_cache.q_1 == o_unavail
	&& mmu_cache.q_2 == o_unavail){
		mmu_cache.q_1 = offset_1;
		mmu_cache.q_2 = offset_2;
		//Go to this offset
		byte_t* entry_1 = (byte_t*)cr3 + (offset_1 * pte_size);
		p_ptr* table_2 = (p_ptr*)(entry_1 + sizeof(meta));
		byte_t* entry_2 = (byte_t*)(*table_2) + (offset_2 * pte_size);
		//Point to itself
		entry_2[next_f] = entry_2[prev_f] = offset_1;
		entry_2[next_s] = entry_2[prev_s] = offset_2;
	}
	
	//Go to first entry in queue
	byte_t* entry_1 = (byte_t*)cr3 + (mmu_cache.q_1 * pte_size);
	p_ptr* table_2 = (p_ptr*)(entry_1 + sizeof(meta));
	byte_t* entry_2 = (byte_t*)(*table_2) + (mmu_cache.q_2 * pte_size);

	//Prev entry to first item = last item in queue
	byte_t prev_1 = entry_2[prev_f];
	byte_t prev_2 = entry_2[prev_s];

	//Move to prev entry
	byte_t* prev_entry_1 = (byte_t*)cr3 + (prev_1 * pte_size);
	p_ptr* prev_table_2 = (p_ptr*)(prev_entry_1 + sizeof(meta));
	byte_t* prev_entry_2 = (byte_t*)(*prev_table_2) + (prev_2 * pte_size);

	//Update values in prev entry's "next" pointer
	prev_entry_2[next_f] = offset_1;
	prev_entry_2[next_s] = offset_2;

	//Set front of queue's prev to this one
	entry_2[prev_f] = offset_1;
	entry_2[prev_s] = offset_2;
	
	//Iterate to new entry to be enqueued
	byte_t* new_entry_1 = (byte_t*)cr3 + (offset_1 * pte_size);
	p_ptr* new_table_2 = (p_ptr*)(new_entry_1 + sizeof(meta));
	byte_t* new_entry_2 = (byte_t*)(*new_table_2) + (offset_2 * pte_size);
	
	//Update new entry to point to prev/first in queue
	new_entry_2[next_f] = mmu_cache.q_1;
	new_entry_2[next_s] = mmu_cache.q_2;
	new_entry_2[prev_f] = prev_1;
	new_entry_2[prev_s] = prev_2;
	
	fprintf(fptr, "Entry at offsets %u %u enqueued.\n", offset_1, offset_2);
}

void dequeue(byte_t offset_1, byte_t offset_2){
	
	
	//Find the entry pointed to by given offsets
	byte_t* entry_1 = (byte_t*)cr3 + (offset_1 * pte_size);
	p_ptr* table_2 = (p_ptr*)(entry_1 + sizeof(meta));
	byte_t* entry_2 = (byte_t*)(*table_2) + (offset_2 * pte_size);
	
	//Next entry in queue pointed to by metadata
	byte_t next_1 = entry_2[next_f];
	byte_t next_2 = entry_2[next_s];
	
	//If this is the first element in the queue
	if(offset_1 == mmu_cache.q_1
	&& offset_2 == mmu_cache.q_2){
		//If it is the ONLY item in the queue
		if(next_1 == offset_1
		&& next_2 == offset_2){
			mmu_cache.q_1 = o_unavail;
			mmu_cache.q_2 = o_unavail;
		}
		else{
			mmu_cache.q_1 = next_1;
			mmu_cache.q_2 = next_2;
		}
	}
	
	//Move to next entry
	byte_t* next_entry_1 = (byte_t*)cr3 + (next_1 * pte_size);
	p_ptr* next_table_2 = (p_ptr*)(next_entry_1 + sizeof(meta));
	byte_t* next_entry_2 = (byte_t*)(*next_table_2) + (next_2 * pte_size);
	//Update values in next entry's "prev" pointer
	next_entry_2[prev_f] = entry_2[prev_f];
	next_entry_2[prev_s] = entry_2[prev_s];
	
	//Prev entry in queue pointed to by metadata
	byte_t prev_1 = entry_2[prev_f];
	byte_t prev_2 = entry_2[prev_s];
	
	//Move to prev entry
	byte_t* prev_entry_1 = (byte_t*)cr3 + (prev_1 * pte_size);
	p_ptr* prev_table_2 = (p_ptr*)(prev_entry_1 + sizeof(meta));
	byte_t* prev_entry_2 = (byte_t*)(*prev_table_2) + (prev_2 * pte_size);
	//Update values in prev entry's "next" pointer
	prev_entry_2[next_f] = entry_2[next_f];
	prev_entry_2[next_s] = entry_2[next_s];
	
	//Update values in given entry to be invalid (just in case)
	entry_2[next_f] = o_unavail;
	entry_2[next_s] = o_unavail;
	entry_2[prev_f] = o_unavail;
	entry_2[prev_s] = o_unavail;
	
	fprintf(fptr, "Entry at offsets %u %u dequeued.\n", offset_1, offset_2);
	
}


p_ptr access_page(byte_t offset_1, byte_t offset_2){
	
	fprintf(fptr, "\nACCESS PAGE AT ENTRY OFFSETS %u %u.\n", offset_1, offset_2);
	
	//Find page entry at given offsets
	byte_t* entry_1 = (byte_t*)cr3 + (offset_1 * pte_size);
	p_ptr* table_2 = (p_ptr*)(entry_1 + sizeof(meta));
	byte_t* entry_2 = (byte_t*)(*table_2) + (offset_2 * pte_size);
	p_ptr page;
	
	//Page is written to disk, read it back into memory
	if(entry_2[present] > 1){
		disk_to_mem(offset_1, offset_2);
		entry_2[present] = 1;
	}
	
	page = *(p_ptr*)(entry_2 + sizeof(meta));
	entry_2[access] = 1;
	return page;
	
	
}

void pm_write(v_ptr ptr, byte_t* data, size_t size){
	
	ptr = normalize_offsets(ptr);
	
	//Deconstruct pointer
	byte_t* offsets = (byte_t*)&ptr;
	byte_t offset_1 = offsets[f_offset];
	byte_t offset_2 = offsets[s_offset];
	byte_t offset_3 = offsets[d_offset];
	byte_t* page = (byte_t*)access_page(offset_1, offset_2) + offset_3;
	
	//Write byte by byte
	int i;
	for(i=0; i<size; i++){
		page[i] = data[i];
	}
	
	
}

void pm_read(v_ptr ptr, void* buffer, size_t size){
	
	ptr = normalize_offsets(ptr);
	//Deconstruct pointer
	byte_t* offsets = (byte_t*)&ptr;
	byte_t offset_1 = offsets[f_offset];
	byte_t offset_2 = offsets[s_offset];
	byte_t offset_3 = offsets[d_offset];
	byte_t* page = (byte_t*)access_page(offset_1, offset_2) + offset_3;
	
	//Read byte by byte, write into buffer
	int i;
	for(i=0; i<size; i++){
		((byte_t*)buffer)[i] = page[i];
	}
	
}

void pm_free(v_ptr ptr){
	/*
	* Starts at offsets specified by ptr, iterates
	* through all entries reserved for this memory region,
	* updates metadata to indicate it is free and adds 
	* corresponding data frames to the stack
	*/
	
	//No one should be able to access the heap concurrently here
	pthread_mutex_lock(&m);
	pthread_cond_wait(&C1, &m);
	
	fprintf(fptr,"\nPM_FREE() CALLED\n");
	
	//Obtain offsets from the ptr
	byte_t* data = (byte_t*)&ptr;
	byte_t pte_1 = data[f_offset];
	byte_t pte_2 = data[s_offset];
	
	fprintf(fptr,"Freeing data at virtual address ptr:%u %u %u %u\n", data[0],data[1],data[2],data[3]);
	fprintf(fptr, "Offsets: %u %u\n", pte_1, pte_2);
	
	int max_entries = PAGE_SIZE/pte_size;
	
	//Start at entry given by v_ptr offsets
	byte_t* entry_1 = (byte_t*)cr3 + (pte_1 * pte_size);
	if(!entry_1[present]){fprintf(fptr,"Error! No memory reserved at address.\n");return;}
	p_ptr table_2 = *(p_ptr*)(entry_1 + sizeof(meta));
	byte_t* entry_2 = (byte_t*)table_2 + (pte_2 * pte_size);
	if(!entry_2[present]){fprintf(fptr,"Error! No memory reserved at address.\n");return;}
	p_ptr page = *(p_ptr*)(entry_2 + sizeof(meta));
	
	//All page table entries in this area will 
	while(entry_2[next_alloc]){
		
		//Remove disk file
		if(entry_2[present] > 1){
			FILE* outfile;
			char filename[16];
			sprintf(filename, "./.swap/%02u%02u.bin", pte_1, pte_2);
			remove(filename);
			fprintf(fptr, "Entry at offsets %u %u on disk, file deleted.\n", pte_1, pte_2);
		} 
		//Just dequeue it
		else{dequeue(pte_1, pte_2);} 
		//Update metadata, but not the queue data
		*(uint32_t*)entry_2 = 0;
		init_free(page);
		*(p_ptr*)(entry_2 + sizeof(meta)) = NULL;
		
		//Find next entry (might be in a separate second-level table)
		if(pte_2 + 1 > max_entries && pte_1 < max_entries){
			pte_2 = 0;
			pte_1++;
		}
		else{
			pte_2++;
		}
		
		//Iterate to next entry
		entry_1 = (byte_t*)cr3 + (pte_1 * pte_size);
		table_2 = *(p_ptr*)(entry_1 + sizeof(meta));
		entry_2 = (byte_t*)table_2 + (pte_2 * pte_size);
		page = *(p_ptr*)(entry_2 + sizeof(meta));
	}
	
	//Free last page in memory region, same logic
	if(entry_2[present] > 1){
		FILE* outfile;
		char filename[16];
		sprintf(filename, "./.swap/%02u%02u.bin", pte_1, pte_2);
		remove(filename);
		fprintf(fptr, "Entry at offsets %u %u on disk, file deleted.\n", pte_1, pte_2);
	} 
	else{dequeue(pte_1, pte_2);} 
	*(uint32_t*)entry_2 = 0;
	init_free(page);
	*(p_ptr*)(entry_2 + sizeof(meta)) = NULL;
	
	//Exit monitor only after done editing stack and page tables
	pthread_cond_signal(&C1);
	pthread_mutex_unlock(&m);
	
	
}

v_ptr pm_malloc(int size){
	/*
	* Iterates through entries and looks for a block of consecutive
	* addresses that will satisfy the amount of memory requested.
	* Reserves addresses and sets pointer in entry to free pages
	* specified by mmu_cache.
	*/
	
	//Not a concurrent method, monitor required
	pthread_mutex_lock(&m);
	pthread_cond_wait(&C1, &m);
	if(size <= 0){exit(-1);}
	
	fprintf(fptr,"\nPM_MALLOC() CALLED\nMemory requested:%d bytes\n", size);
	
	if(cr3){
		int num_pages = (int)ceil((float)size/(float)PAGE_SIZE);
		fprintf(fptr,"Pages needed for request:%d\n", num_pages);
		
		
		//Find a consecutive block of contiguous *virtual* memory addresses
		//Do not allocate, only count!
		int needed = num_pages;
		int max_entries = PAGE_SIZE / pte_size;
		byte_t pte_1 = 0;
		byte_t pte_2 = 0;
		//The first entry of the contiguous block
		byte_t first_entry[2] = {pte_1, pte_2};
		
		//Nested loop to iterate through both levels of tables and count
		while(pte_1 < max_entries && needed > 0){
			pte_2 = 0; 
			byte_t* entry_1 = (byte_t*)cr3 + (pte_1 * pte_size);
			
			//Second level table doesn't exist yet
			//All entries are free
			if(!entry_1[present]){
				pte_1++;
				needed -= max_entries; 
				continue;
			}
			
			//Iterate through second-level table
			p_ptr table_2 = *((p_ptr*)(entry_1 + sizeof(meta)));
			while(pte_2 < max_entries && needed > 0){
				byte_t* entry_2 = (byte_t*)table_2 + (pte_2*pte_size);
				
				//Page in use, not contiguous start count over
				if(entry_2[present]){
					needed = num_pages;
					//Start of contiguous memory will be next entry
					//Make sure it's not out of bounds of either table
					if(pte_2 >= max_entries && pte_1 < max_entries){
						first_entry[0] = pte_1 + 1;
						first_entry[1] = 0;
					}
					else if(pte_2 < max_entries){
						first_entry[0] = pte_1;
						first_entry[1] = pte_2+1;
					}
					else{
						//No contiguous virtual memory large enough for request
						fprintf(fptr,"Virtual fragmentation!\n"); exit(-1);
					}
					pte_2++;
					continue;
				}
				pte_2++;
				needed--;
			}
			pte_1++;
		}
		//No contiguous virtual memory large enough for request
		if(needed > 0){fprintf(fptr,"Virtual fragmentation!\n");exit(-1);}
		
		//Allocate memory starting at first entry
		pte_1 = first_entry[0];
		pte_2 = first_entry[1];
		needed = num_pages;
		while(pte_1 <= max_entries && needed > 0){
			byte_t* metadata = (byte_t*)cr3 + (pte_1 * pte_size);
			p_ptr* table = (p_ptr*)(metadata + sizeof(meta));
			
			//Create second level table at this first-level entry
			if(!metadata[present]){
				p_ptr level_2 = init_table();
				metadata[present] = 1; //present
				*table = level_2;
			}
			//Iterate through second level table, update metadata
			p_ptr table_2 = *table;
			while(pte_2 <= max_entries && needed > 0){
				needed --;
				byte_t* new_entry = table_2 + (pte_2 * pte_size);
				p_ptr* new_page = (p_ptr*)(new_entry + sizeof(meta));
				new_entry[present] = 1; 
				if(!needed){new_entry[next_alloc]=0;} 
				else{new_entry[next_alloc] = 1;}
				new_entry[access] = 1; //access should be 1 to start 
				new_entry[dirty] = 0; 
				//Grab from stack
				*new_page = init_alloc();
				//Add it to the queue
				enqueue(pte_1, pte_2);
				pte_2++;
			}
			//need to move to next first-level table entry
			pte_1++;
			pte_2 = 0;
		}

		//Done editing stacks/page tables, exit monitor
		pthread_cond_signal(&C1);
		pthread_mutex_unlock(&m);
		
		
		//Create final v_ptr, point to start of virtual memory region
		byte_t final[4];
		final[d_offset] = 0;
		final[s_offset] = first_entry[1];
		final[f_offset] = first_entry[0];
		final[extra] = 0;
		fprintf(fptr,"Final 'pointer': %u %u %u %u\n", final[0],final[1],final[2],final[3]);
		return *((v_ptr*)&final);
		
	}
	fprintf(fptr,"Heap not properly initialized.\n");
	exit(-1);
	
	
}

//This function has no bearing on program logic,
//this is just a way to save files that have been written to disk
//for demonstration purposes only
//It's not smart code, it exists purely for the presentation
void record_file_contents(){
	FILE* src;
	FILE* dest;
	byte_t byte;
	int i;
	
	
	//First X page
	src = fopen("./.swap/0000.bin", "r");
	dest = fopen("./.swapRECORD/0000.bin", "w");
	if(src == NULL || dest == NULL){
		return;
	}
	byte = fgetc(src);
	while(byte){
		fputc(byte, dest);
		byte = fgetc(src);
	}
	fclose(src);
	fclose(dest);
	
	//Second X page
	src = fopen("./.swap/0001.bin", "r");
	dest = fopen("./.swapRECORD/0001.bin", "w");
	if(src == NULL || dest == NULL){
		return;
	}
	byte = fgetc(src);
	while(byte){
		fputc(byte, dest);
		byte = fgetc(src);
	}
	fclose(src);
	fclose(dest);
	
	//Third X page
	src = fopen("./.swap/0002.bin", "r");
	dest = fopen("./.swapRECORD/0002.bin", "w");
	if(src == NULL || dest == NULL){
		return;
	}
	byte = fgetc(src);
	while(byte){
		fputc(byte, dest);
		byte = fgetc(src);
	}
	fclose(src);
	fclose(dest);
	
	//Fourth X page
	src = fopen("./.swap/0003.bin", "r");
	dest = fopen("./.swapRECORD/0003.bin", "w");
	if(src == NULL || dest == NULL){
		return;
	}
	byte = fgetc(src);
	while(byte){
		fputc(byte, dest);
		byte = fgetc(src);
	}
	fclose(src);
	fclose(dest);
	
	
	
}



int main(){
	
	fptr = fopen("results.txt", "w");
	
	
	init_heap();
	
	fprintf(fptr, "\nMalloc X (1024)\n");
	v_ptr x = pm_malloc(1024);
	
	int data = 312;
	fprintf(fptr, "\nWrite to X (%d)\n", data);
	pm_write(x, (void*)&data, sizeof(int));
	
	data = 523;
	fprintf(fptr, "\nWrite to X+sizeof(int) (%d)\n", data);
	pm_write(x+sizeof(int), (void*)&data, sizeof(int));
	
	data = 432;
	fprintf(fptr, "\nWrite to X+PAGE_SIZE (third X page) (%d)\n", data);
	pm_write(x+(PAGE_SIZE*2), (void*)&data, sizeof(int));
	
	//Malloc enough memory that EVERYTHING gets evicted
	fprintf(fptr, "\nMalloc Z (2048)\n");
	v_ptr z = pm_malloc(2048);
	record_file_contents();
	
	int y = 0;
	
	pm_read(x, (void*)&y, sizeof(int));
	fprintf(fptr, "\nRead at X: (%d)\n", y);
	
	pm_read(x+sizeof(int), (void*)&y, sizeof(int));
	fprintf(fptr, "\nRead at X+sizeof(int): (%d)\n", y);
	
	pm_read(x+(PAGE_SIZE*2), (void*)&y, sizeof(int));
	fprintf(fptr, "\nRead at X+PAGE_SIZE*2 (third x page): (%d)\n", y);
	
	fprintf(fptr, "\nFree X (4 pages)\n");
	pm_free(x);
	
	fprintf(fptr, "\nFree Z (8 pages)\n");
	pm_free(z);
	
	fclose(fptr);
	
	printf("Results printed to results.txt, check .swapRECORD directory for examples of .bin files.");
	
	
}