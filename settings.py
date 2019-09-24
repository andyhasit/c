import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
ALIAS_FILE = os.path.join(THIS_DIR, 'aliases')
MAIN_FILE = os.path.join(THIS_DIR, 'main.py')

DATA_DIR = os.path.join(THIS_DIR, 'data')
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M'


def get_data_dir(namespace):
    path = os.path.join(DATA_DIR, namespace)
    if not os.path.isdir(path):
        os.mkdir(path)
    return path


def get_data_file(namespace, name):
    directory = get_data_dir(namespace)
    path = os.path.join(directory, name)
    return path