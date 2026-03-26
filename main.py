import optparse
import logging
import re
import sys
from parser import parseInputFiles
from utils import calc_file_access_stats, write_io_details, write_open_details


def save_file_details(filedata):
    """Save detailed statistics to individual files"""
    fname = filedata['filename'].replace("/", "__")
    write_io_details(zip(filedata['write_sizes'], filedata['write_times']), f"{fname}.write.stat.txt")
    write_io_details(zip(filedata['read_sizes'], filedata['read_times']), f"{fname}.read.stat.txt")
    write_open_details(filedata, f"{fname}.open.stat.txt")


def main():
    parser = optparse.OptionParser("usage: %prog [options] STRACE_LOG ...")
    parser.add_option('--loglevel', default="ERROR", help="CRITICAL, ERROR, WARNING, INFO, DEBUG")
    parser.add_option('--filter-files', default=".*", help="Regex filter for filenames")
    parser.add_option('--file-details', action="store_true", default=False, help="Save detailed stats to files")
    parser.add_option('--format',
                      default="write_time,write_count,write_size,read_time,read_count,read_size,open_time,open_count",
                      help="Fields to display")
    parser.add_option('--sort-by', default="write_time", help="Property to sort by")
    parser.add_option('--unknown-call-stats', action="store_true", default=False, help="Print untracked call stats")

    (options, args) = parser.parse_args()
    if not args:
        parser.print_help()
        sys.exit(1)

    logging.basicConfig(level=getattr(logging, options.loglevel.upper()), format='%(levelname)s: %(message)s')

    # 1. Analyze data and calculate
    file_access_stats, unknown_calls = parseInputFiles(args)
    calc_file_access_stats(file_access_stats)

    # 2. Set output format
    properties = options.format.split(',')
    all_props = ['write_time', 'write_count', 'write_size', 'read_time', 'read_count', 'read_size', 'open_time',
                 'open_count', 'open_from_count', 'close_time', 'close_count']
    if 'all' in properties: properties = all_props

    # 3. Sort and output
    sort_key = options.sort_by if options.sort_by in all_props else properties[0]
    sorted_data = sorted(file_access_stats.values(), reverse=True, key=lambda x: x.get(sort_key, 0))

    print(f"\n{'=' * 30} I/O STATISTICS (sorted by {sort_key}) {'=' * 30}")
    header = " ".join([f"{p:>12}" for p in properties]) + " filename"
    print(header)

    for data in sorted_data:
        if re.match(options.filter_files, data['filename']):
            row = []
            for p in properties:
                val = data.get(p, 0)
                row.append(f"{val:>12.6f}" if "_time" in p else f"{val:>12}")
            print(" ".join(row) + f" {data['filename']}")
            if options.file_details: save_file_details(data)

    if options.unknown_call_stats:
        print(f"\n{'=' * 30} UNKNOWN CALLS {'=' * 30}")
        for name, info in sorted(unknown_calls.items(), key=lambda x: sum(x[1]['times']), reverse=True):
            print(f"{name:16} Count: {info['count']:>8} Total Time: {sum(info['times']):>12.6f}")


if __name__ == "__main__":
    main()