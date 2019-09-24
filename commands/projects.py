"""
Track tasks on projects

general
 - show all projects and when last worked on



"""
import os
from collections import defaultdict
from datetime import datetime, timedelta
from settings import DATE_FORMAT, DATETIME_FORMAT
from utils import *


REGISTER_FILE = get_data_file('projects', 'project_register.json')
DEFAULT_REGISTER_DATA = {
    'projects': {
        'misc': {
            'touched': '2000-01-01 00:00',
            'directory': '/home/xyz',
        }
    }
}
SEP = '||'


def list_projects():
    data = extract_json(REGISTER_FILE, DEFAULT_REGISTER_DATA)
    return sorted(data['projects'].keys())


def cmd_new_project(args):
    """
    alias: new_project
    help: Creates a new project using the current working directory.
    """
    project_name = extract_arg(args, 0, 'project name')
    data = extract_json(REGISTER_FILE, DEFAULT_REGISTER_DATA)
    if project_name in data['projects']:
        error('Project "{}" already exists'.format(project_name))
    if not (project_name.islower() and project_name.isalnum()):
        error('Project name may only contain lowercase letters or digits.')
    data['projects'][project_name] = {
        'touched': timestamp(),
        'directory': os.getcwd(),
    }
    write_json(REGISTER_FILE, data)


def _set_project_data(project_name, key, value):
    data = extract_json(REGISTER_FILE, DEFAULT_REGISTER_DATA)
    if project_name not in data['projects']:
        error('Did not recognise project "{}"'.format(project_name))
    data['projects'][project_name][key] = value
    write_json(REGISTER_FILE, data)


def cmd_set_project_dir(args):
    """
    alias: set_project_dir.[projects]
    help: Creates a new project using the current working directory.
    """
    project_name = extract_arg(args, 0, 'project name')
    _set_project_data(project_name, 'directory', os.getcwd())


def cmd_add_project_log_entry(args):
    """
    alias: log.[projects]
    help: Log entry against project
    """
    project_name = args[0]
    comment = ' '.join(args[1:])
    timestamp = datetime.now().strftime(DATETIME_FORMAT)
    _set_project_data(project_name, 'touched', timestamp)
    project_log_file = get_data_file('projects', '{}_log'.format(project_name))
    line = SEP.join([timestamp, comment])
    append_to_log(project_log_file, line)


def cmd_show_projects(args):
    """
    alias: projects
    help: Show projects stats.
    """
    data = extract_json(REGISTER_FILE, DEFAULT_REGISTER_DATA)
    lines = []
    for k, v in data['projects'].items():
        lines.append((k, v['touched'], v['directory']))
    lines.sort(key=lambda x: 1)
    lines.insert(0, ('Project', 'Last touched', 'Directory'))
    print_table(lines, align_left=(0, 1, 2), horizontal_borders=(1,))


def __cmd_show_points(args):
    """
    alias: points
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
    print_table(table, horizontal_borders=(1, len(table) - 1, ))


#def cmd_new_bucket(args):


