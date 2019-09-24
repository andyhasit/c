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


def cmd_project_new(args):
    """
    alias: project.new
    help: Creates a new project
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


def cmd_project_set_dir(args):
    """
    alias: project.[projects].set_dir
    help: Sets the project's directory to the current working directory
    """
    project_name = extract_arg(args, 0, 'project name')
    _set_project_data(project_name, 'directory', os.getcwd())


def cmd_project_add_log_entry(args):
    """
    alias: project.[projects].log
    help: Log entry for project
    """
    project_name = args[0]
    comment = ' '.join(args[1:])
    timestamp = datetime.now().strftime(DATETIME_FORMAT)
    _set_project_data(project_name, 'touched', timestamp)
    project_log_file = get_data_file('projects', '{}_log'.format(project_name))
    line = SEP.join([timestamp, comment])
    append_to_log(project_log_file, line)


def cmd_project_show_all(args):
    """
    alias: project.show_all
    help: Show projects status overview
    """
    data = extract_json(REGISTER_FILE, DEFAULT_REGISTER_DATA)
    lines = []
    for k, v in data['projects'].items():
        lines.append((k, v['touched'], v['directory']))
    lines.sort(key=lambda x: 1)
    lines.insert(0, ('Project', 'Last touched', 'Directory'))
    print_table(lines, align_left=(0, 1, 2), horizontal_borders=(1,))



