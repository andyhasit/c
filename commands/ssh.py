"""

for ssh

c.ssh.fibrotx-staging

"""

from settings import DATE_FORMAT, DATETIME_FORMAT
from utils import *


def list_servers():
    # TODO make this data. must not contain spaces
    return [
        'admin',
        'home',
        'body',
        'work',
        'projects',
        'uncategorised'
    ]


def c_alias_ssh():
    """
    alias: ssh.[servers]
    help: connect to ssh server
    generate: yes
    """
    return [
        ('ssh.abc', 'ssh abuchan@fibrotx-staging.novarumcloud.com')
    ]


def c_func_ssh():
    """
    alias: ssh.[servers]
    help: connect to ssh server
    generate: yes
    """
    return [
        ('scp.abc', ['ssh abuchan@fibrotx-staging.novarumcloud.com'])
    ]