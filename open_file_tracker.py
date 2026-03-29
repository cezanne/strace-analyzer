class OpenFileTracker:
    """Class to track currently open file descriptors (FD)"""
    def __init__(self):
        self.open_files = {}

    def register_open(self, filename, fd):
        self.open_files[fd] = filename

    def register_close(self, fd):
        if fd in self.open_files:
            del self.open_files[fd]

    def is_open(self, fd):
        return fd in self.open_files

    def get_filename(self, fd):
        return self.open_files.get(fd)

    def get_open_files(self):
        return self.open_files
