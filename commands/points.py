"""
Log points against categories
"""
from collections import defaultdict
from datetime import datetime, timedelta
from settings import DATE_FORMAT, DATETIME_FORMAT
from utils import *


POINTS_LOG = get_data_file('points', 'points_log')


def list_buckets():
    # TODO make this data. must not contain spaces
    return [
        'admin',
        'home',
        'body',
        'work',
        'projects',
        'uncategorised'
    ]

def c_cmd_points_add(args):
    """
    alias: score.[buckets].add
    help: Add points to a bucket.
    """
    bucket_name = args[0]
    points = args[1]
    comment = ' '.join(args[2:])
    append_to_log(POINTS_LOG, [get_timestamp(), bucket_name, points, comment])


def c_cmd_points_stats(args):
    """
    alias: score.stats
    help: Show point stats.
    """
    lines = extract_lines(POINTS_LOG)
    
    # Create dicts to contain scores
    buckets = defaultdict(lambda: {'today': 0, 'yesterday':0, 'total':0})
    totals = {'today': 0, 'yesterday':0, 'total':0}

    # Get date strings for comparison
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    today_str = today.strftime(DATE_FORMAT)
    yesterday_str = yesterday.strftime(DATE_FORMAT)

    # Populate buckets dict
    for bucket_name in list_buckets():
        buckets[bucket_name]

    # Go through log file
    for line in lines:
        timestamp, bucket_name, points, comment = split_log_line(line)
        points = int(points)
        date_str = timestamp.split(' ', 1)[0]
        bucket = buckets[bucket_name]
        bucket['total'] += points
        totals['total'] += points
        if date_str == today_str:
            bucket['today'] += points
            totals['today'] += points
        elif date_str == yesterday_str:
            bucket['yesterday'] += points
            totals['yesterday'] += points

    # Build table
    table = [('Bucket', 'Today', 'Yesterday', 'Total')]
    for bucket_name in sorted(buckets):
        bucket = buckets[bucket_name]
        table.append((bucket_name , bucket['today'], bucket['yesterday'], bucket['total']))
    table.append(('totals', totals['today'], totals['yesterday'], totals['total']))
    
    # Print table
    print_table(table, align_left=(0, ), horizontal_borders=(1, len(table) - 1, ))


def c_cmd_points_log(args):
    """
    alias: score.log
    help: Show all log entries
    """
    lines = []
    for line in extract_lines(POINTS_LOG):
        lines.append(split_log_line(line))
    print_table(lines, align_left=(0, 1, 1, 3))