import argparse
import logging
import sys

from parser import Parser
from scan import scan_strace
from report import report


def parse_argument():
    parser = argparse.ArgumentParser("usage: %prog [options] STRACE_LOG ...")
    parser.add_argument('--loglevel', type=str, default="ERROR", help="CRITICAL, ERROR, WARNING, INFO, DEBUG")
    parser.add_argument("--path-pattern", action='append', dest='path_patterns',
                        help="Patterns to match for reporting. Can be specified multiple times.")
    parser.add_argument('--report-mode', type=str, default="summary",
                        help="report mode: raw/summary/timeline")
    parser.add_argument('strace_files', nargs='+', help="strace log files to process")

    args = parser.parse_args()
    if not args:
        parser.print_help()
        sys.exit(1)
    return args


def main():
    args = parse_argument()

    # noinspection SpellCheckingInspection
    logging.basicConfig(level=getattr(logging, args.loglevel.upper()), format='%(levelname)s: %(message)s')

    strace_parser = Parser()
    scan_strace(strace_parser, args.strace_files)
    report(args.report_mode, args.path_patterns, strace_parser.fio_manager)


if __name__ == "__main__":
    main()
