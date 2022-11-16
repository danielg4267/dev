# Program-Managed Heap

This is a project in which the program itself manages its own heap. A large amount of static memory is allocated to simulate physical RAM, and then the memory is divided into pages of fixed size (256 bytes each, in this case). Memory access is granted through a two-level page table system, virtual pointers (implemented as unsigned integers), and swap files. The concept of this might be a bit confusing, I recommend [reading about the topic](https://en.wikipedia.org/wiki/Page_table) to understand more.

For more details about the actual implementation, see the presentation PDF included in this folder, but I will summarize here:

# Pointers:

A virtual pointer is simply an unsigned integer, or 4 bytes. Three of those bytes are actually used (the fourth and most significant byte is unused). The least significant byte is the offset into the data frame, the second least significant is the offset into the second level page table, and the third least significant byte is the offset into the first level page table.

When attempting to free or access a page, this pointer is split into its offsets. Using the offset in the first level page table, it jumps down by the number of entries specified and reaches the pointer to the second level table. There, it jumps down the number of entries specified by ITS given offset and finds a pointer to the actual dataframe. Then it jumps through the data frame to its given offset, where the user may begin reading/writing data.

# Page Table Entries:

Page table entries are a combination of 8 bytes of metadata and an 8 byte void pointer. Each byte in the metadata represents a different aspect of the entry. It is organized as follows:

[Present] [Next Page Allocated?] [Accessed?] [Dirty] [2 byte-offset to the next page in queue] [2 byte offset into previous page in queue]

The present byte indicates if the entry is occupied and also if the page is in memory or saved to disk. The next page allocated specifies if the next entry in the table adjacent to this one is part of the same memory region (useful for calls to pm_free() ). Access byte is used to indicate when a page was last accessed for implementation of the CLOCK page replacement algorithm. The dirty byte is unused. The next 4 bytes implement a doubly linked list of entries in the table, which is used as a circular queue (again, for CLOCK page replacement).

# Page Swapping:

Pages are written to the .swap folder. I assumed that this folder either already existed or it was possible to create it (creating a directory is relatively easy, but it's platform dependent and so I left it out as it is not important to the design/presentation of the algorithm). The pages are named by their entries in the page tables, so that they are all unique. Multiple files makes it easier to demonstrate what is being written, but a future implementation would use a legitimate ".swap" file, similar to an actual swap algorithm.

I print out results to results.txt. The program also saves a few example pages to .swapRECORD directory (minus any NULL values from the original pages). I have included trial results and trial .swap files so it's not needed to run the program, but running it yourself will also demonstrate it, of course. :)

# To Compile And Run:

"make pmheap"
"./pmheap"