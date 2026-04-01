import logging
import os
from open_file_tracker import OpenFileTracker
from strace_match import StraceMatch, SyscallType

from fio_manager import FileIoManager


class Parser:
    def __init__(self):
        self.tracker = OpenFileTracker()
        self.fio_manager = FileIoManager()

    def parse(self, line):
        data = StraceMatch.match(line)
        if data is None:
            return

        if (data.syscall_type == SyscallType.CREAT or
                data.syscall_type == SyscallType.OPEN or
                data.syscall_type == SyscallType.OPENAT):
            if data.fd < 0:
                return
            # noinspection SpellCheckingInspection
            if (data.syscall_type == SyscallType.OPENAT and data.dir_fd and data.dir_fd != "AT_FDCWD" and
                    not os.path.isabs(data.path)):
                path = self.tracker.get_path(data.dir_fd) + "/" + data.path
            else:
                path = data.path

            self.tracker.register_open(path, data.fd)
        elif data.syscall_type == SyscallType.READ or data.syscall_type == SyscallType.WRITE:
            path = self.tracker.get_path(data.fd)
            if path is None:
                logging.warning(f"fd({data.fd}) not found in tracker for syscall {data.syscall_type}")
                return
            data.path = path
            self.fio_manager.add_data(data)
        elif data.syscall_type == SyscallType.CLOSE:
            self.tracker.register_close(data.fd)
