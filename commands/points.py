"""
Log points against categories
"""
from collections import defaultdict
from datetime import datetime, timedelta
from settings import get_data_file, DATE_FORMAT


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


def cmd_score_points(args):
    """
    alias: score.[buckets]
    help: Score points against bucket.
    """
    bucket_name = args[0]
    points = args[1]
    comment = ' '.join(args[2:])
    timestamp = datetime.now().strftime(DATETIME_FORMAT)
    line = SEP.join([timestamp, bucket_name, points, comment])
    with open(POINTS_LOG, 'a') as fp:
        fp.write(line + '\n')


def cmd_show_points(args):
    """
    alias: points
    help: Show point stats.
    """
    with open(POINTS_LOG) as fp:
        lines = fp.readlines()

    table = [
        ('', 'Today', 'Yesterday', 'Total'),
    ]

    # Collect as (today, yesterday, total)
    buckets = defaultdict(lambda: {'today': 0, 'yesterday':0, 'total':0})
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    today_str = today.strftime(DATE_FORMAT)
    yesterday_str = yesterday.strftime(DATE_FORMAT)
    for line in lines:
        timestamp, bucket_name, points = line.split(SEP, 3)[:3]
        points = int(points)
        date_str = timestamp.split(' ', 1)[0]
        bucket = buckets[bucket_name]
        bucket['total'] += points
        if date_str == today_str:
            bucket['today'] += points
        elif date_str == yesterday_str:
            bucket['yesterday'] += points

    for bucket_name in sorted(buckets):
        bucket = buckets[bucket_name]
        table.append((bucket_name , bucket['today'], bucket['yesterday'], bucket['total']))

    print_table(table)


def print_table(table):
    """
    Prints tabular data.
    """
    max_widths = defaultdict(lambda: 0)
    for row in table:
        for i, col in enumerate(row):
            col_width = len(str(col))
            if col_width > max_widths[i]:
                max_widths[i] = col_width
    for row in table:
        line = ''
        for i, col in enumerate(row):
            col_as_str = str(col)
            col_width = len(col_as_str)
            padding = max_widths[i] - col_width
            if i == 0: # left pad first col. TODO: make configurable
                line += ' ' + col_as_str + padding * ' ' + '  '
            else:
                line += padding * ' ' + col_as_str + '  '
        print(line)



#def cmd_new_bucket(args):

