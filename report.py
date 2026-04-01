from fio_manager import FileIoManager


def report(fio_manager: FileIoManager):
    print("File IO Report:")
    print("===================")
    for fio in fio_manager.file_ios:
        typestr = 'Read' if fio.is_read else 'Write'
        print(f"Time: {fio.rtime:.6f}s, File: {fio.path}, {typestr}: {fio.size}")
