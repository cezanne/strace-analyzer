import re
import logging
import os
from models import new_file_access_stats_entry
from open_file_tracker import OpenFileTracker


def parse_strace(strace_files):
    tracker = OpenFileTracker()
    file_stats = {}

    # Register default streams
    for std in [("stdin", 0), ("stdout", 1), ("stderr", 2)]:
        tracker.register_open(std[0], std[1])
        file_stats[std[0]] = new_file_access_stats_entry(std[0])

    unfinished = {}

    for strace_file in strace_files:
        logging.info(f"Processing {strace_file} ...")
        with open(strace_file, 'r') as fh:
            for line in fh:
                if "ERESTARTSYS" in line: continue
                if "exit_group" in line: break

                # Handle unfinished calls
                if "<unfinished ...>" in line:
                    pid = int(line.split()[0])
                    unfinished[pid] = line[:-len(" <unfinished ...>")].rstrip()
                    continue
                elif " resumed> " in line:
                    pid = int(line.split()[0])
                    rest = line[line.find(" resumed> ") + len(" resumed> "):].rstrip()
                    line = unfinished.get(pid, "") + rest
                    if pid in unfinished: del unfinished[pid]

                # --- System call pattern matching ---

                # 1. Open/Openat
                m = re.search(
                    r'open\(?at\)?\((?:(?P<dirfd>.*), )?\"(?P<filename>.*)\", (?P<mode>.*)\).*= (?P<fd>-?[0-9]+).*<(?P<time>[0-9]+\.[0-9]+)>',
                    line)
                if m:
                    fd = int(m.group('fd'))
                    if fd == -1: continue
                    fname = m.group('filename')
                    if m.group('dirfd') and m.group('dirfd') != "AT_FDCWD" and not os.path.isabs(fname):
                        fname = tracker.get_filename(int(m.group('dirfd'))) + "/" + fname

                    tracker.register_open(fname, fd)
                    if fname not in file_stats: file_stats[fname] = new_file_access_stats_entry(fname)
                    file_stats[fname]['open_times'].append(float(m.group('time')))
                    file_stats[fname]['open_modes'].append(m.group('mode'))
                    file_stats[fname]['open_fds'].append(fd)
                    file_stats[fname]['open_from'][strace_file] = file_stats[fname]['open_from'].get(strace_file, 0) + 1
                    continue

                # 2. Write/Read (including V/64)
                m = re.search(
                    r'p?(?P<type>write|read)(?:64|v)?\((?P<fd>[0-9]+), ?.*, (?P<size>[0-9]+)\).*= (?P<act_size>-?[0-9]+).*<(?P<time>[0-9]+\.[0-9]+)>',
                    line)
                if m and not "process_vm" in line:
                    fd = int(m.group('fd'))
                    if tracker.is_open(fd):
                        fname = tracker.get_filename(fd)
                        t_key, s_key = (f"{m.group('type')}_times", f"{m.group('type')}_sizes")
                        file_stats[fname][t_key].append(float(m.group('time')))
                        file_stats[fname][s_key].append(int(m.group('act_size')))
                    else:
                        logging.warning(f"No Open file for FD {fd}")
                    continue

                # 3. Close
                m = re.search(r'close\((?P<fd>[0-9]+)\).*= (?P<ret>-?[0-9]+).*<(?P<time>[0-9]+\.[0-9]+)>', line)
                if m:
                    fd = int(m.group('fd'))
                    if tracker.is_open(fd):
                        fname = tracker.get_filename(fd)
                        file_stats[fname]['close_times'].append(float(m.group('time')))
                        tracker.register_close(fd)
                    continue

    return file_stats