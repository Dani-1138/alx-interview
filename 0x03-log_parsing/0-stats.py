#!/usr/bin/env python3

import sys
import signal
from collections import defaultdict

def print_statistics(total_size, status_counts):
    print(f'Total file size: {total_size}')
    for status_code in sorted(status_counts.keys()):
        print(f'{status_code}: {status_counts[status_code]}')

def process_line(line, total_size, status_counts):
    parts = line.split()

    if len(parts) != 12 or parts[5] != '"GET' or parts[7] != 'HTTP/1.1"':
        return total_size, status_counts

    try:
        status_code = int(parts[8])
        file_size = int(parts[11])
    except ValueError:
        return total_size, status_counts

    total_size += file_size
    status_counts[status_code] += 1

    return total_size, status_counts

def main():
    total_size = 0
    status_counts = defaultdict(int)
    lines_processed = 0

    def signal_handler(sig, frame):
        nonlocal total_size, status_counts, lines_processed
        print_statistics(total_size, status_counts)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    try:
        for line in sys.stdin:
            total_size, status_counts = process_line(line.strip(), total_size, status_counts)
            lines_processed += 1

            if lines_processed % 10 == 0:
                print_statistics(total_size, status_counts)

    except KeyboardInterrupt:
        print_statistics(total_size, status_counts)

if __name__ == "__main__":
    main()

