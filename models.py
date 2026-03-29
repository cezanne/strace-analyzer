import logging

def new_file_access_stats_entry(filename):
    """Create a new file access statistics entry"""
    return {
        'filename': filename,
        'open_times': [], 'open_modes': [], 'open_fds': [], 'open_from': {},
        'write_times': [], 'write_sizes': [], 'read_times': [], 'read_sizes': [], 'close_times': [],
        # Cached calculated values
        'write_time': 0.0, 'write_count': 0, 'write_size': 0.0,
        'read_time': 0.0, 'read_count': 0, 'read_size': 0.0,
        'open_time': 0.0, 'open_count': 0, 'open_from_count': 0,
        'close_time': 0.0, 'close_count': 0
    }
