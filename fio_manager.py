from dataclasses import dataclass
from typing import List

from strace_match import SyscallData, SyscallType


@dataclass
class FileIo:
    rtime: float
    path: str
    is_read: bool
    size: int


class FileIoManager:
    def __init__(self):
        self.file_ios: List[FileIo] = []

    def add_data(self, data: SyscallData):
        if data.syscall_type not in [SyscallType.READ, SyscallType.WRITE]:  # Only handle READ and WRITE
            return
        self.file_ios.append(FileIo(data.rtime, data.path, data.syscall_type == SyscallType.READ, data.size))

    def add_io(self, rtime: float, path: str, is_read: bool, size: int):
        self.file_ios.append(FileIo(rtime, path, is_read, size))
