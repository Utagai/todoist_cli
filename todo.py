import json
import os

from cli import TodoistCLI 
from wrapper import wrapper_init

def init_cli():
    todoist_cli = TodoistCLI()
    todoist_cli.prompt = '~> '
    def nothing():
        pass
    todoist_cli.emptyline = nothing
    todoist_cli.cmdqueue.append('projects')
    todoist_cli.cmdloop('todoist CLI')

def main():
    with open(os.path.expanduser('~') + '/.todo.conf') as conf_file:
        conf = json.load(conf_file)
        secret = conf['secret']
        wrapper_init(secret)

    init_cli()

if __name__ == '__main__':
    main()
