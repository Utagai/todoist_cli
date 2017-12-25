import json
import os

from cli import TodoistCLI 
from wrapper import wrapper_init

def main():
    secret = None
    with open(os.path.expanduser('~') + '/.todo.conf') as conf_file:
        conf = json.load(conf_file)

        secret = conf['secret']
        print("Calling init")
        wrapper_init(secret)

    todoist_cli = TodoistCLI()
    todoist_cli.prompt = '~> '
    todoist_cli.cmdloop('todoist CLI')
    todoist_cli.use_rawinput = False

if __name__ == '__main__':
    main()
