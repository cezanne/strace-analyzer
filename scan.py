import logging
from strace_match import StraceMatch


def scan_strace(parser, strace_files):
    unfinished = {}

    for strace_file in strace_files:
        logging.info(f"Processing {strace_file} ...")
        with open(strace_file, 'r') as fh:
            for line in fh:
                # noinspection SpellCheckingInspection
                if "ERESTARTSYS" in line:
                    continue
                if "exit_group" in line:
                    break

                # Handle unfinished calls
                if "<unfinished ...>" in line:
                    pid = int(line.split()[0])
                    unfinished[pid] = line[:-len(" <unfinished ...>")].rstrip()
                    continue
                elif " resumed> " in line:
                    pid = int(line.split()[0])
                    rest = line[line.find(" resumed> ") + len(" resumed> "):].rstrip()
                    line = unfinished.get(pid, "") + rest
                    if pid in unfinished:
                        del unfinished[pid]

                data = StraceMatch.match(line)
                if data:
                    parser.parse(line)
