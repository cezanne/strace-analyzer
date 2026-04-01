class OpenFileTracker:
    """Class to track currently open file descriptors (FD)"""
    def __init__(self):
        self.paths_opened = {}

    def register_open(self, path, fd):
        self.paths_opened[fd] = path

    def register_close(self, fd):
        if fd in self.paths_opened:
            del self.paths_opened[fd]

    def is_open(self, fd):
        return fd in self.paths_opened

    def get_path(self, fd):
        return self.paths_opened.get(fd)

    def get_open_files(self):
        return self.paths_opened
