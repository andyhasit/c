from datetime import datetime, timedelta
import os
import json
import sys
from collections import defaultdict
import settings

LOG_SEPARATOR = '||'


class OnceList:
    """
    A list which raises an error if you add an item twice.
    """
    def __init__(self, label):
        self.label = label
        self._items = []

    def add(self, item):
        if item in self._items:
            error('{} already defined: {}'.format(self.label, item))
        else:
            self._items.append(item)


def extract_arg(args, index, name, required=True):
    """
    Extracts an arg from a list of args, exiting with an error if it is not found.
    """
    try:
        return args[index]
    except IndexError:
        if required:
            error('Arg required at position {}: {}'.format(index, name))


def extract_remaining_args(args, index, name, required=True):
    """
    Extracts remaining args from a list of args, exiting with an error if it is not found.
    """
    try:
        assert len(args) > index
        return ' '.join(args[index:])
    except AssertionError:
        if required:
            error('Parameter "{}" required at position {}'.format(name, index))


def get_timestamp():
    """
    Returns a string with the timestamp.
    """
    return datetime.now().strftime(settings.DATETIME_FORMAT)


def append_to_log(file, values):
    """
    Adds a line to a log file.
    """
    line = LOG_SEPARATOR.join(values)
    with open(file, 'a') as fp:
        fp.write(line + '\n')


def extract_lines(file):
    """
    Extracts lines from file.
    """
    with open(file) as fp:
        return fp.readlines()


def split_log_line(line):
    """
    Returns a tuple of the log lines split
    """
    return [s.strip() for s in line.split(LOG_SEPARATOR)]


def extract_json(file, default=None):
    """
    Extracts json from json file.
    """
    try:
        with open(file) as fp:
            return json.load(fp)
    except:
        return default


def write_json(file, data):
    """
    Write json to json file.
    """
    with open(file, 'w') as fp:
        return json.dump(data, fp, indent=4, sort_keys=True)


def error(message):
    print('ERROR: ' + message)
    sys.exit(1)

def get_data_dir(namespace):
    """
    Gets a data directory and ensures it exists.
    """
    path = os.path.join(settings.DATA_DIR, namespace)
    if not os.path.isdir(path):
        os.mkdir(path)
    return path


def get_data_file(namespace, name):
    """
    Gets a data file and ensures its parent directory exists.
    """
    directory = get_data_dir(namespace)
    path = os.path.join(directory, name)
    return path


def print_table(data, horizontal_borders=None, align_left=None):
    """
    Prints tabular data.
    @horizontal_borders: <tuple> specifies where to place horizontal borders between lines 
    """
    print(' ')
    if horizontal_borders is None:
        horizontal_borders = ()
    if align_left is None:
        align_left = ()
    max_widths = defaultdict(lambda: 0)
    for row in data:
        for i, col in enumerate(row):
            col_width = len(str(col))
            if col_width > max_widths[i]:
                max_widths[i] = col_width
    line_length = sum([v for v in max_widths.values()])
    line_length += len(data[0]) * 2 + 1
    for n, row in enumerate(data):
        if n in horizontal_borders:
            print(' ' + '-' * line_length)
        line = ''
        for i, col in enumerate(row):
            col_as_str = str(col)
            col_width = len(col_as_str)
            padding = max_widths[i] - col_width
            if i in align_left: # left pad first col. TODO: make configurable
                line += ' ' + col_as_str + padding * ' ' + '  '
            else:
                line += padding * ' ' + ' ' + col_as_str + '  '
        print(line)
    print(' ')