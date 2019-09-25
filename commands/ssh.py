from utils import *


SERVER_DATA_FILE = get_data_file('servers', 'servers.json')
DEFAULT_SERVER_DATA = {
    'servers': {
        'server1': {
            'domain': 'server1.example.com',
            'usernames': ['bob', 'jane'],
        }
    }
}


def get_server_data():
    return extract_json(SERVER_DATA_FILE, DEFAULT_SERVER_DATA)


def c_alias_ssh():
    """
    alias: ssh.[servers]
    help: Quick connect to ssh server.
    """
    entries = []
    for server_name, server_entry in get_server_data()['servers'].items():
        domain = server_entry['domain']
        for username in server_entry['usernames']:
            alias = 'ssh.{}.{}'.format(server_name, username)
            command = 'ssh {}@{}'.format(username, domain)
            entries.append((alias, command))
    return entries


# def c_func_ssh():
#     """
#     alias: ssh.[servers]
#     help: connect to ssh server
#     generate: yes
#     """
#     return [
#         ('scp.abc', ['ssh abuchan@fibrotx-staging.novarumcloud.com'])
#     ]