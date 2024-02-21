# Cache Simulator - measure deadblocks

## Overview
<div style="text-align: justify">
In this assignment, you will extend the cache simulator that you developed in PA3 to assess the effective utilization of the cache silicon real estate using traces of CloudSuite and OLTP workloads.
Unlike commonly used cache assessment metrics (e.g., hit ratio) that consider the input-output relationship, in this programming assignment, you evaluate a cache based on what happens inside the cache. You are free to choose the programming language of your choice among C/C++, Java, Perl,PHP, or Python. You are advised to start early.
</div>

## Programming Exercise
<div style="text-align: justify">
A block that is kept in a cache, but will not be accessed again until it gets evicted is called a dead block (i.e., every block will become dead after the last access to it, and until it gets evicted from the cache). Extend the cache component that you developed in PA3 to measure what fraction of the cache blocks are dead on average. For this purpose, start the simulation with an empty cache, wait until all cache frames are full (i.e., their valid bit is set), and then counts the number of dead blocks after every access to the cache. At the end of the simulation, report the average number of dead blocks by dividing the sum of the dead blocks that you obtained after every access to the cache over the number of such accesses.
</div>

**Note:** <div style="text-align: justify">To classify a cache block as dead, you need to know the future accesses to the cache. Remember you can always move forward in the trace file to see the future!</div>

## Milestone 1
<div style="text-align: justify">
For every workload, measure the average percentage of dead blocks for a 32 KB, 8-way associative L1d cache with a 64B block size that uses the LRU replacement policy.
</div>

## Milestone 2
<div style="text-align: justify">
(OPTIONAL but HIGHLY recommended) Propose an idea to reduce the percentage of dead blocks in a cache. Implement the proposed idea in your cache simulator and measure its effectiveness (what matters the most is innovation!).
</div>

## Deliverable
<div style="text-align: justify">
Hand in the code and a short report (PDF) that describes what you observed in this experiment. Please include the percentage of dead blocks for every workload in your report. What did youlearn from this experiment? If you have done Milestone 2, please clearly explain the proposed idea, justify why you believe it works, and report the simulation numbers to back up your claim.
</div>