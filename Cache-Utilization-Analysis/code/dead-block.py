import os
from collections import OrderedDict
import random

def convert_to_bytes(size):
    if not size:
        return 0
    # Split the input string into numeric part and unit
    x_str = ''.join(filter(str.isdigit, size))
    x = float(x_str) if x_str else 0  # Convert numeric part to float, default to 0 if not present
    y = ''.join(filter(str.isalpha, size)).upper()

    # Convert based on the unit
    if y == "B":
        return x
    elif y == "KB":
        return x * 1024
    elif y == "MB":
        return x * 1024 * 1024
    elif y == "GB":
        return x * 1024 * 1024 * 1024
    else:
        raise ValueError("Invalid unit: {}".format(y))
    
def clear_cache(cache):
    cache = cache
    cache = OrderedDict()
    for i in range(number_of_sets):
        cache[f"s{i}"] = []
    return cache

def replacement(policy): # implement some policys for replacement blocks when cache is full
    if policy == "LRU":
        evicted = cache[f"s{set_number}"][0]
        cache[f"s{set_number}"] = cache[f"s{set_number}"][1:]
        cache[f"s{set_number}"].append(mm_block_number)
        return evicted
    elif policy == "NMRU":
        random_num = random.randint(0,6)
        cache[f"s{set_number}"].pop(random_num)
        cache[f"s{set_number}"].append(mm_block_number)
        return cache[f"s{set_number}"][random_num]
    else:
        random_num = random.randint(0,7)
        cache[f"s{set_number}"].pop(random_num)
        cache[f"s{set_number}"].append(mm_block_number)
        return cache[f"s{set_number}"][random_num]

''' declare specification of cache '''
cache_size = convert_to_bytes(input("(enter the Cache size - use KB, MB, GB ... - or press ENTER for default (32KB)\ncache size : "))
block_size = convert_to_bytes(input("(enter the Block size - use B, KB, ... - or press ENTER for default (64B)\nBlock size : "))
word_size = convert_to_bytes(input("(enter the Word size - use B, ... - or press ENTER for default (1B)\nWord size : "))
way = input("enter the assosiativity of cache - x-way set-assosiative - or press ENTER for default (8)\nx: ")

if cache_size == 0: cache_size = 32*1024 # 32KB
if word_size == 0: word_size = 1
way = 8 if way == "" else int(way)
block_size = int(64 / word_size) if block_size == 0 else int(block_size / word_size)

number_of_sets = int(((cache_size / block_size)) / way)

cache = OrderedDict()
for i in range(number_of_sets):
    cache[f"s{i}"] = []


# replacement_policies = ["LRU", "NMRU", "RANDOM"]
replacement_policies = ["LRU"] # test on just LRU

''' measure hit ratio of cache with some workloads '''
print("--------------------------------")
print("The test operation has started")
print("--------------------------------")

current_directory = os.getcwd() # fetch the benchmark path
relative_path = 'traces/'
main_directory = os.path.join(current_directory, relative_path)

''' Iterate through each subdirectory in the main directory (benchmarks paths) '''
for subdir, dirs, files in os.walk(main_directory):
    for benchmark in files:
        benchmark_path = os.path.join(subdir, benchmark) # Construct the full path to the benchmark
        benchmark_name = (subdir.split("/"))[-1]
        print(f"On {benchmark_name} Benchmark")
        for policy in replacement_policies:
            print(f"with {policy} policy", end=" ")
            with open(benchmark_path) as file:
                ''' reset the cache '''
                cache = clear_cache(cache)
                hit_count = miss_count = start_here_flag = start_here = 0
                last_hit_times = {}
                
                ''' complete test '''
                if benchmark_name == "MapReduce":
                    dead_blocks_trace = [0] * 9332922
                else:
                    dead_blocks_trace = [0] * 10000000
                
                # ''' quick test '''
                # dead_blocks_trace = [0] * 50000
                
                for line in file: # read addresses line by line
                    pc_addr = line.split()
                    address = int(pc_addr[1], 16)
                    mm_block_number = address // block_size
                    set_number = mm_block_number % number_of_sets
                    
                    if start_here_flag == 0 and len(cache) == 512:
                        start_here = hit_count + miss_count
                        start_here_flag = 1

                    ''' block in cache checking...'''
                    if mm_block_number in cache[f"s{set_number}"]:
                        ''' hit policy + dead policy'''
                        last_hit_times[mm_block_number] = hit_count + miss_count
                        hit_count+=1
                        current_block = cache[f"s{set_number}"].index(mm_block_number)
                        element_to_move = cache[f"s{set_number}"].pop(current_block)
                        cache[f"s{set_number}"].append(element_to_move)
                    else:
                        ''' miss policy + dead policy'''
                        last_hit_times[mm_block_number] = hit_count + miss_count
                        miss_count+=1
                        ''' checking if cache is full...'''
                        if len(cache[f"s{set_number}"]) < 8:
                            cache[f"s{set_number}"].append(mm_block_number)
                        else:
                            evicted = replacement(policy)
                            evicted_time = hit_count + miss_count
                            for d in range(last_hit_times[evicted], evicted_time):
                                dead_blocks_trace[d] += 1
            
            ''' calculate hit ratio'''
            hit_ratio = round((hit_count / (hit_count + miss_count)), 8) * 100
            print(f"Hit Ratio = {hit_ratio}%")
            dead_blocks_trace = dead_blocks_trace[start_here : len(dead_blocks_trace)-start_here]

            ''' calculate average deadblock'''      
            average_dead_block =  (sum(dead_blocks_trace) / (len(dead_blocks_trace) * 512) ) * 100
            print(f"Average Dead Block = {average_dead_block}%")
            if policy == "LRU": print("--------------------------------")

print("The test operation is over")
print("--------------------------------")