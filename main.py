import optparse
import logging
import sys

from parser import Parser
from scan import scan_strace
from report import report


def main():
    parser = optparse.OptionParser("usage: %prog [options] STRACE_LOG ...")
    parser.add_option('--loglevel', default="ERROR", help="CRITICAL, ERROR, WARNING, INFO, DEBUG")

    (options, args) = parser.parse_args()
    if not args:
        parser.print_help()
        sys.exit(1)

    # noinspection SpellCheckingInspection
    logging.basicConfig(level=getattr(logging, options.loglevel.upper()), format='%(levelname)s: %(message)s')

    strace_parser = Parser()
    scan_strace(strace_parser, args)
    report(strace_parser.fio_manager)


if __name__ == "__main__":
    main()
