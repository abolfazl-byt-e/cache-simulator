# Cache Policy Evaluation

## Overview
In this assignment, you will write a cache simulator and evaluate the LRU, NMRU, and Random replacement policies using traces of CloudSuite and OLTP workloads. You are free to choose the programming language of your choice among C/C++, Java, Python, or Perl. You are advised to start early.

## Programming Exercise
Code a generic cache component which is parametrized by (1) Cache Block Size, (2) Cache Asso- ciativity, and (3) Cache Size. The cache component, among other things, should have a ’lookup’ method which gets an address and searches the cache to find the address. If the address is in the cache, this lookup is a hit. If the address is not in the cache, it is a miss. In this case, the block that contains the address should be inserted into the cache. If all the frames in the set that the block address maps to are occupied, the cache should pick a victim according to the replacement policy, evict the victim block, and insert the block that holds the address. Write an interface that reads addresses from the input trace files and apply them to the cache using the ’lookup’ method.

**Note 1:** You can find the format of the trace files in the ’readme.txt’ file which is delivered to you along with the trace files (in ’traces/readme.txt’).

**Note 2:** Please ignore the PC field of L1d trace files in this programming assignment.

## Milestone
For every workload, compare the LRU replacement policy against NMRU and Random replacement policies for a 32KB, 8-way associative L1d cache with a 64B block size.

## Deliverable
Hand in the code and a short report (PDF) that describes the three replacement policies and their observed performance (i.e., hit ratio). Please not only include performance numbers per benchmark in your report but also aggregate the performance numbers of each replacement policy. Please spend time to make your graph look great. Rank the replacement policies based on their performance. How much better is the best replacement policy as compared to the others?
