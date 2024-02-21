# Prefetcher Effectiveness Analysis

## Overview
In this assignment, you will extend the cache simulator that you developed in PA1 to assess the effectiveness of two widely-used prefetchers for hiding instructions and data access latencies of data center and database applications using traces of CloudSuite and OLTP workloads. You are free to choose the programming language of your choice among C/C++, Java, Perl, PHP, or Python.  You are advised to start early.

## Programming Exercise
For this programming assignment, you implement two prefetchers: (1) next-line prefetcher, and (2) stride prefetcher. A next-line prefetcher is a simple prefetcher that after an access to a cache block that results in a miss, predicts future accesses to the next cache block, and prefetches the predicted cache block if it is not in the cache. If a predicted cache block actually being used by the processor, the behavior of a next-line prefetcher is identical to the behavior of the prefetcher in the case of a cache miss.
<br />
While a bit more complex than a next-line prefetcher, a stride prefetcher is a simple prefetcher for prefetching data references characterized by regular strides. A stride prefetcher attempts to uncover regular strides for every static load or store. For this purpose, a stride prefetcher has a reference prediction table (RPT), which is a cache tagged and referenced with the PC of load and store instructions. The entries in the RPT hold the previous address referenced by the corresponding instruction (last address), the offset of that address from the previous data address referenced by that instruction (last stride), and some flags. When a load or store instruction is executed that matches an entry in the RPT, the offset of the data address of that load or store from the previous data address stored in the RPT is calculated (current stride). When this matches the last stride, a prefetch is launched for the data address one offset ahead of the current data address (i.e., current address + stride). Moreover, on every access, the last address and last stride fields of the entry in the RPT that corresponds to the load or store instruction get updated.

**Note 1:** In this programming assignment, there is no restriction on the size of the reference prediction table.

**Note 2:** The first column of the L1d trace files contains the PCs of load and store instructions.

<br />
Please notice that every load or store has a unique PC, and consequently, such PCs can be used to distinguish different load and store instructions.
<br />

## Milestone 1
For every workload, measure the coverage and accuracy of the next-line prefetcher and the stride prefetcher for an L1d cache. Just like PA1, a 32-KB, 8-way associative cache with a 64B block size that uses the LRU replacement policy will be used in this programming assignment.

## Milestone 2 (OPTIONAL but HIGHLY recommended)
Propose a prefetcher with a higher coverage and accuracy as compared to next-line and stride prefetchers. Implement the proposed prefetcher in your cache simulator and measure its effectiveness (what matters the most is innovation!).

## Deliverable
Hand in the code and a short report (PDF) that describes the two prefetchers and what you observed in this experiment. Please include the coverage and accuracy of the two prefetchers for every workload in your report in a form of a graph (more precisely, a bar chart). Your graphs need to be readable and clear. You can look at a prefetching paper to see how such graphs should look (e.g., Figure 6 of Spatial Memory Streaming). Moreover, for every prefetcher, please add a bar to your graphs to show the average coverage and accuracy across all workloads. What did you learn from this experiment?

<br />
If you have done Milestone 2, please clearly explain the proposed prefetcher, justify why you believe it works, and report the simulation numbers to back up your claim.
<br />

**Note:** One of the goals of this programming assignment is for you to learn how to present experimental numbers in a form of a graph. Hence, spend as much time as necessary to make your graphs look great!
