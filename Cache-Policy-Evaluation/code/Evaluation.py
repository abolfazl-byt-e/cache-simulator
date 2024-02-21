import matplotlib.pyplot as plt

# Data
benchmarks = ["TPCC Oracle", "Media Streaming", "MapReduce", "TPCC DB2", "Web Search", "Web Frontend", "SAT Solver", "Data Serving"]
lru_hit_ratios    = [93.6, 96.5, 94.8, 93.4, 98.3, 96.5, 97.0, 94.3]
nmru_hit_ratios   = [63.2, 75.1, 62.3, 64.3, 66.2, 70.5, 61.3, 68.2]
random_hit_ratios = [72.9, 81.5, 72.9, 73.7, 76.8, 79.0, 73.1, 76.7]

# Plotting
bar_width = 0.25
index = range(len(benchmarks))

plt.bar(index, lru_hit_ratios, width=bar_width, label='LRU')
plt.bar([i + bar_width for i in index], nmru_hit_ratios, width=bar_width, label='NMRU')
plt.bar([i + 2 * bar_width for i in index], random_hit_ratios, width=bar_width, label='Random')

# Customize the plot
plt.xlabel('Benchmarks')
plt.ylabel('Hit Ratio (%)')
plt.title('Cache Hit Ratios for Different Benchmarks and Replacement Policies')
plt.xticks([i + bar_width for i in index], benchmarks)
plt.legend()

# Show the plot
plt.show()