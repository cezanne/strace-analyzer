import re
from enum import Enum
from typing import Optional, Union


class SyscallType(Enum):
    CREAT = 1
    OPEN = 2
    OPENAT = 3
    READ = 4
    WRITE = 5
    CLOSE = 6


class SyscallData:
    rtime: float
    syscall_type: SyscallType
    path: str = None
    fd: int = None
    dir_fd: Union[str, int] = None
    size: int = None


class StraceMatch:
    @staticmethod
    def handle_creat(data: SyscallData, group):
        data.syscall_type = SyscallType.CREAT
        data.path = group('path')
        data.fd = int(group('fd'))

    @staticmethod
    def handle_open(data: SyscallData, group):
        data.syscall_type = SyscallType.OPEN
        data.path = group('path')
        data.fd = int(group('fd'))

    @staticmethod
    def handle_openat(data: SyscallData, group):
        data.syscall_type = SyscallType.OPENAT
        data.path = group('path')
        data.dir_fd = group('dir_fd')
        data.fd = int(group('fd'))

    @staticmethod
    def handle_syscall_read(data: SyscallData, group):
        data.syscall_type = SyscallType.READ
        data.fd = int(group('fd'))
        data.size = int(group('ret'))

    @staticmethod
    def handle_syscall_write(data: SyscallData, group):
        data.syscall_type = SyscallType.WRITE
        data.fd = int(group('fd'))
        data.size = int(group('ret'))

    @staticmethod
    def handle_close(data: SyscallData, group):
        data.syscall_type = SyscallType.CLOSE
        data.fd = int(group('fd'))

    RULES = [
        (re.compile(r'^\s*(?P<pid>\d+)\s+(?P<rtime>\d+\.\d+)\s+creat\("(?P<filename>[^"]*)",\s*'
                    r'(?P<mode>[^)]*)\)\s*=\s*(?P<fd>-?\d+)'), handle_creat),
        (re.compile(r'^\s*(?P<pid>\d+)\s+(?P<rtime>\d+\.\d+)\s+open\("(?P<path>[^"]*)",\s*'
                    r'(?P<mode>[^)]*)\)\s*=\s*(?P<fd>-?\d+)'), handle_open),
        (re.compile(r'^\s*(?P<pid>\d+)\s+(?P<rtime>\d+\.\d+)\s+openat\((?P<dir_fd>[^,]+),\s*"(?P<path>[^"]*)",\s*'
                    r'(?P<mode>[^)]*)\)\s*=\s*(?P<fd>-?\d+)'), handle_openat),
        (re.compile(r'^\s*(?P<pid>\d+)\s+(?P<rtime>\d+\.\d+)\s+read\((?P<fd>\d+),\s*.*,\s*(?P<size>\d+)\)\s*=\s*'
                    r'(?P<ret>-?\d+)'), handle_syscall_read),
        (re.compile(r'^\s*(?P<pid>\d+)\s+(?P<rtime>\d+\.\d+)\s+write\((?P<fd>\d+),\s*.*,\s*(?P<size>\d+)\)\s*=\s*'
                    r'(?P<ret>-?\d+)'), handle_syscall_write),
        (re.compile(r'^\s*(?P<pid>\d+)\s+(?P<rtime>\d+\.\d+)\s+pread64\((?P<fd>\d+),\s*.*,\s*(?P<size>\d+),\s*'
                    r'(?P<offset>-?\d+)\)\s*=\s*(?P<ret>-?\d+)'), handle_syscall_read),
        (re.compile(r'^\s*(?P<pid>\d+)\s+(?P<rtime>\d+\.\d+)\s+pwrite64\((?P<fd>\d+),\s*.*,\s*(?P<size>\d+),\s*'
                    r'(?P<offset>-?\d+)\)\s*=\s*(?P<ret>-?\d+)'), handle_syscall_write),
        (re.compile(r'^\s*(?P<pid>\d+)\s+(?P<rtime>\d+\.\d+)\s+readv\((?P<fd>\d+),\s*.*,\s*(?P<iovcnt>\d+)\)\s*=\s*'
                    r'(?P<ret>-?\d+)'), handle_syscall_read),
        (re.compile(r'^\s*(?P<pid>\d+)\s+(?P<rtime>\d+\.\d+)\s+writev\((?P<fd>\d+),\s*.*,\s*(?P<iovcnt>\d+)\)\s*=\s*'
                    r'(?P<ret>-?\d+)'), handle_syscall_write),
        (re.compile(r'^\s*(?P<pid>\d+)\s+(?P<rtime>\d+\.\d+)\s+close\((?P<fd>\d+)\)\s*=\s*(?P<ret>-?\d+)'),
         handle_close)
    ]

    @staticmethod
    def match(line) -> Optional[SyscallData]:
        for pattern, handler in StraceMatch.RULES:
            m = pattern.search(line)
            if m:
                data = SyscallData()
                data.rtime = float(m.group('rtime'))
                handler(data, m.group)
                return data
        return None
