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
    
def clear_cache(number_of_sets):
    cache = OrderedDict()
    for i in range(number_of_sets):
        cache[f"s{i}"] = []
    return cache

def replacement(policy, cache, mm_block_number, set_number):
    if policy == "LRU":
        cache[f"s{set_number}"] = cache[f"s{set_number}"][1:]
        cache[f"s{set_number}"].append(mm_block_number)
    elif policy == "NMRU":
        random_num = random.randint(0,6)
        cache[f"s{set_number}"].pop(random_num)
        cache[f"s{set_number}"].append(mm_block_number)
    else:
        random_num = random.randint(0,7)
        cache[f"s{set_number}"].pop(random_num)
        cache[f"s{set_number}"].append(mm_block_number)

def measure_cache(policy, hit_count, miss_count):
    hit_ratio = round((hit_count / (hit_count + miss_count)), 8) * 100
    print(f"Hit Ratio = {hit_ratio}%")
    if policy == "LRU": print("--------------------------------")

def get_cache_specification_by_user():
    ''' declare specification of cache by user'''
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
    
    return [cache, block_size, number_of_sets]

def get_benchmarks():
    current_directory = os.getcwd() # fetch the benchmark path
    relative_path = 'traces/'
    main_directory = os.path.join(current_directory, relative_path)
    return main_directory

def lookup(cache, mm_block_number, set_number, policy, hit_count, miss_count):
    missed = 0
    ''' block in cache checking...'''
    if mm_block_number in cache[f"s{set_number}"]:
        ''' hit policy '''
        hit_count+=1
        current_block = cache[f"s{set_number}"].index(mm_block_number)
        element_to_move = cache[f"s{set_number}"].pop(current_block)
        cache[f"s{set_number}"].append(element_to_move)
    else:
        ''' miss policy '''
        missed = 1
        miss_count+=1
        ''' checking if cache is full...'''
        if len(cache[f"s{set_number}"]) < 8:
            cache[f"s{set_number}"].append(mm_block_number)
        else:
            replacement(policy, cache, mm_block_number, set_number)
    return [cache, hit_count, miss_count, missed]

def prefetch(cache, pred_mm_block_number, pred_set_number, policy):
    ''' block in cache checking...'''
    if pred_mm_block_number in cache[f"s{pred_set_number}"]:
        ''' hit policy '''
        current_block = cache[f"s{pred_set_number}"].index(pred_mm_block_number)
        element_to_move = cache[f"s{pred_set_number}"].pop(current_block)
        cache[f"s{pred_set_number}"].append(element_to_move)
    else:
        ''' miss policy '''
        ''' checking if cache is full...'''
        if len(cache[f"s{pred_set_number}"]) < 8:
            cache[f"s{pred_set_number}"].append(pred_mm_block_number)
        else:
            replacement(policy, cache, pred_mm_block_number, pred_set_number)
    return cache

def main():
    cache, block_size, number_of_sets = get_cache_specification_by_user()
    
    # replacement_policies = ["LRU", "NMRU", "RANDOM"]
    replacement_policies = ["LRU"]

    ''' measure hit ratio of cache with some workloads '''
    print("--------------------------------")
    print("The test operation has started")
    print("--------------------------------")

    main_directory = get_benchmarks()

    ''' Iterate through each subdirectory in the main directory (benchmarks paths) '''
    for subdir, dirs, files in os.walk(main_directory):
        for benchmark in files:
            benchmark_path = os.path.join(subdir, benchmark) # Construct the full path to the benchmark
            bechmark_name = (subdir.split("/"))[-1]
            print(f"On {bechmark_name} Benchmark")
            for policy in replacement_policies:
                print(f"with {policy} policy", end=" ")
                with open(benchmark_path) as file:
                    
                    ''' reset the cache '''
                    cache = clear_cache(number_of_sets)
                    hit_count = miss_count = 0
                    pred_mm_block_number = -1

                    for line in file: # read addresses line by line
                        pc_addr = line.split()
                        address = int(pc_addr[1], 16)
                        mm_block_number = address // block_size
                        set_number = mm_block_number % number_of_sets
                        
                        cache, hit_count, miss_count, missed = lookup(cache, mm_block_number, set_number, policy, hit_count, miss_count)

                        if missed:
                            pred_mm_block_number = mm_block_number + 1
                            pred_set_number = pred_mm_block_number % number_of_sets
                            prefetch(cache, pred_mm_block_number, pred_set_number, policy)
                        elif mm_block_number == pred_mm_block_number:
                            pred_mm_block_number = mm_block_number + 1
                            pred_set_number = pred_mm_block_number % number_of_sets
                            prefetch(cache, pred_mm_block_number, pred_set_number, policy)

                                
                measure_cache(policy, hit_count, miss_count)

    print("The test operation is over")
    print("--------------------------------")

if __name__ == "__main__":
    main()