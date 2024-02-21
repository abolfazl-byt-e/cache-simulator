import matplotlib.pyplot as plt
import numpy as np

# Benchmark names
benchmarks = ['TPCC Oracle', 'Media Streaming', 'MapReduce', 'TPCC DB2', 'Web Search', 'Web Frontend', 'SAT Solver', 'Data Serving']
 
set_associative_hit_ratios = [93.40015000000001, 94.81148999999999, 94.819565, 93.25688, 98.30555, 96.43351, 96.93481, 94.2478]
next_line_prefetcher_hit_ratios = [94.96109, 95.58776, 95.528635, 94.40631, 99.27844, 97.36738, 97.37915000000001, 96.21625]
next_2line_prefetcher_hit_ratios = [94.94601, 94.93047, 95.691939, 94.57397, 99.31173, 97.44652, 97.35145, 96.55354]
next_3line_prefetcher_hit_ratios = [94.84651, 94.25729000000001, 95.693482, 94.60065, 99.30105, 97.43579, 97.28676, 96.59522]
stride_prefetcher_hit_ratios = [93.79937000000001, 95.3705, 94.969293, 93.52728, 98.63181, 96.75218, 97.17662, 94.89635]
combined_next_line_stride_hit_ratios = [95.01006, 95.60271999999999, 95.623611, 94.4658, 99.32775000000001, 97.40801, 97.52746, 96.35323]
combined_next_2line_stride_hit_ratios = [94.98143, 94.95126, 95.769449, 94.61888, 99.34054, 97.4859, 97.48924, 96.59805]
combined_next_3line_stride_hit_ratios = [94.87706, 94.26681, 95.77087399999999, 94.64074, 99.32686, 97.46177, 97.43096, 96.66127]

bar_width = 0.1
bar_positions_set = np.arange(len(benchmarks))
bar_positions_next_line = bar_positions_set + bar_width
bar_positions_stride = bar_positions_set + 2 * bar_width
bar_positions_combined_next_line_stride = bar_positions_set + 3 * bar_width
bar_positions_next_2line = bar_positions_set + 4 * bar_width
bar_positions_next_3line = bar_positions_set + 5 * bar_width
bar_positions_combined_next_2line_stride = bar_positions_set + 6 * bar_width
bar_positions_combined_next_3line_stride = bar_positions_set + 7 * bar_width

fig, ax = plt.subplots(figsize=(18, 10))

ax.bar(bar_positions_set, set_associative_hit_ratios, width=bar_width, label='Set-Associative Cache')
ax.bar(bar_positions_next_line, next_line_prefetcher_hit_ratios, width=bar_width, label='Next-Line Prefetcher')
ax.bar(bar_positions_stride, stride_prefetcher_hit_ratios, width=bar_width, label='Stride Prefetcher', color='green')
ax.bar(bar_positions_combined_next_line_stride, combined_next_line_stride_hit_ratios, width=bar_width, label='Combined next-line + stride', color='orange')
ax.bar(bar_positions_next_2line, next_2line_prefetcher_hit_ratios, width=bar_width, label='Next-2Line Prefetcher', color='purple')
ax.bar(bar_positions_next_3line, next_3line_prefetcher_hit_ratios, width=bar_width, label='Next-3Line Prefetcher', color='cyan')
ax.bar(bar_positions_combined_next_2line_stride, combined_next_line_stride_hit_ratios, width=bar_width, label='Combined Next-2Line + Stride', color='red')
ax.bar(bar_positions_combined_next_3line_stride, combined_next_2line_stride_hit_ratios, width=bar_width, label='Combined Next-3Line + Stride', color='blue')

ax.set_xlabel('Benchmarks')
ax.set_ylabel('Hit Ratio (%)')
ax.set_title('Comparison of Hit Ratios for Different Prefetchers')
ax.set_xticks(bar_positions_set + 3.5 * bar_width)
ax.set_xticklabels(benchmarks)
ax.legend(loc='lower right', bbox_to_anchor=(1, 0))

plt.show()
