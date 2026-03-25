#!/bin/sh

# Ensure the current directory is accessible and synchronized
cd "$PWD" || exit 1

# Set the log directory (default: strace-logs)
LOGDIR=${LOGDIR:=strace-logs}

# Create the log directory if it does not exist
if [ ! -d "$LOGDIR" ]; then
  mkdir -p "$LOGDIR"
fi

# Set the log filename with hostname and Process ID (PID)
LOGFILE="$LOGDIR/$(hostname).$$.strace"

# Execute strace with the provided arguments ($@)
# -f: Follow child processes
# -r: Print relative timestamp
# -T: Print time spent in system calls
# -o: Write the trace output to a file
strace -f -r -T -o "$LOGFILE" "$@"