import statistics


def write_io_details(data, filename):
    """Write detailed I/O statistics to a file in CSV format"""
    stats = {}
    for size, time in data:
        if size not in stats:
            stats[size] = []
        stats[size].append(time)

    with open(filename, "w+") as f:
        f.write(",".join(
            ["size", "count", "time_tot", "time_min", "time_max", "time_median", "bw_avg", "bw_min", "bw_max"]) + "\n")
        for size in sorted(stats.keys()):
            count = len(stats[size])
            t_tot = sum(stats[size])
            t_min = min(stats[size])
            t_max = max(stats[size])
            t_median = statistics.median_high(stats[size])

            # Prevent division by zero when calculating bandwidth (BW)
            bw_avg = (size * count / t_tot) if t_tot > 0 else 0
            bw_min = (size / t_max) if t_max > 0 else 0
            bw_max = (size / t_min) if t_min > 0 else 0

            f.write(",".join(map(str, [size, count, t_tot, t_min, t_max, t_median, bw_avg, bw_min, bw_max])) + "\n")


def write_open_details(filedata, filename):
    """Record from which source (input log) the file was opened"""
    with open(filename, "w+") as f:
        f.write("opened_from,count\n")
        for open_from, count in filedata['open_from'].items():
            f.write(f"{open_from},{count}\n")


def calc_file_access_stats(file_access_stats):
    """Calculate sums and counts based on the collected list data"""
    for filename in file_access_stats.keys():
        f = file_access_stats[filename]
        f['write_time'] = sum(f['write_times'], 0.0)
        f['write_count'] = len(f['write_times'])
        f['write_size'] = sum(f['write_sizes'])
        f['read_time'] = sum(f['read_times'], 0.0)
        f['read_count'] = len(f['read_times'])
        f['read_size'] = sum(f['read_sizes'])
        f['open_time'] = sum(f['open_times'], 0.0)
        f['open_count'] = len(f['open_times'])
        f['close_time'] = sum(f['close_times'], 0.0)
        f['close_count'] = len(f['close_times'])
        f['open_from_count'] = len(f['open_from'])