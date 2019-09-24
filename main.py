"""
This file is the entry point for commands called by aliases.

You probably want to call:

    python3 main.py rebuild_aliases

"""
import sys
sys.path.append(".") # This enables commands to import settings for example
from command_info import get_callable_commands


def run(args):
    commands = get_callable_commands()
    cmdname = args[0]
    args = args[1:]
    if cmdname in commands:
        commands[cmdname]['function'](args)
    else:
        print('C command "{}" not found'.format(cmdname))

run(sys.argv[1:])