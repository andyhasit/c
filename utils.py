import os
from collections import defaultdict
import settings

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


def print_table(data, horizontal_borders=None):
    """
    Prints tabular data.
    @borders: specifies where to place horizontal borders
    """
    if horizontal_borders is None:
        horizontal_borders = ()
    max_widths = defaultdict(lambda: 0)
    for row in data:
        for i, col in enumerate(row):
            col_width = len(str(col))
            if col_width > max_widths[i]:
                max_widths[i] = col_width
    line_length = sum([v for v in max_widths.values()])
    line_length += len(data[0]) + 1
    for n, row in enumerate(data):
        if n in horizontal_borders:
            print(' ' + '-' * line_length)
        line = ''
        for i, col in enumerate(row):
            col_as_str = str(col)
            col_width = len(col_as_str)
            padding = max_widths[i] - col_width
            if i == 0: # left pad first col. TODO: make configurable
                line += ' ' + col_as_str + padding * ' ' + ' '
            else:
                line += padding * ' ' + col_as_str + '  '
        print(line)