from typing import List
from fnmatch import fnmatch

from fio_manager import FileIoManager


def match_patterns(path: str, patterns: List[str]) -> bool:
    if patterns is None:
        return True
    for pattern in patterns:
        if fnmatch(path, f"{pattern}*"):
            return True
    return False


def report_summary(path_patterns: List[str], fio_manager: FileIoManager):
    total_read = 0
    total_write = 0
    for fio in fio_manager.file_ios:
        if not match_patterns(fio.path, path_patterns):
            continue
        if fio.is_read:
            total_read += fio.size
        else:
            total_write += fio.size

    print("File IO Summary:")
    print("===================")
    print(f"Total Read: {total_read} bytes")
    print(f"Total Write: {total_write} bytes")


def report_timeline(path_patterns: List[str], fio_manager: FileIoManager):
    timeslot_read = 0
    timeslot_write = 0
    rtime_next = 1
    for fio in fio_manager.file_ios:
        if not match_patterns(fio.path, path_patterns):
            continue
        if fio.is_read:
            timeslot_read += fio.size
        else:
            timeslot_write += fio.size
        while rtime_next <= fio.rtime:
            print(f"{rtime_next - 1}: Read: {timeslot_read} bytes, Write: {timeslot_write} bytes")
            timeslot_read = 0
            timeslot_write = 0
            rtime_next += 1
    print(f"{rtime_next - 1}: Read: {timeslot_read} bytes, Write: {timeslot_write} bytes")


def report_raw(path_patterns: List[str], fio_manager: FileIoManager):
    print("File IO Details:")
    print("===================")
    for fio in fio_manager.file_ios:
        if not match_patterns(fio.path, path_patterns):
            continue
        typestr = 'Read' if fio.is_read else 'Write'
        print(f"Time: {fio.rtime:.6f}s, File: {fio.path}, {typestr}: {fio.size}")


def report(mode: str, path_patterns: List[str], fio_manager: FileIoManager):
    if mode == "summary":
        report_summary(path_patterns, fio_manager)
    elif mode == "timeline":
        report_timeline(path_patterns, fio_manager)
    else:
        report_raw(path_patterns, fio_manager)
