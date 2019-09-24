"""
Log points against categories
"""
from collections import defaultdict
from datetime import datetime, timedelta
from settings import DATE_FORMAT, DATETIME_FORMAT
from utils import *


POINTS_LOG = get_data_file('points', 'points_log')
SEP = '||'


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


#def cmd_new_bucket(args):



def cmd_points_log(args):
    """
    alias: points.[buckets].log
    help: Log points against bucket.
    """
    bucket_name = args[0]
    points = args[1]
    comment = ' '.join(args[2:])
    line = SEP.join([timestamp(), bucket_name, points, comment])
    with open(POINTS_LOG, 'a') as fp:
        fp.write(line + '\n')


def cmd_points_status(args):
    """
    alias: points.status_all
    help: Show point stats.
    """
    with open(POINTS_LOG) as fp:
        lines = fp.readlines()

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
        timestamp, bucket_name, points = line.split(SEP, 3)[:3]
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
    table = [('', 'Today', 'Yesterday', 'Total')]
    for bucket_name in sorted(buckets):
        bucket = buckets[bucket_name]
        table.append((bucket_name , bucket['today'], bucket['yesterday'], bucket['total']))
    table.append(('totals', totals['today'], totals['yesterday'], totals['total']))
    
    # Print table
    print_table(table, align_left=(0, ), horizontal_borders=(1, len(table) - 1, ))
