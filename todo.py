import json
import os
import colored

from app.cli import TodoistCLI 
from app import wrapper
from app.color import prnt_str, PURPLE, ORANGE, BLUE

def init_cli():
    todoist_cli = TodoistCLI()
    todoist_cli.prompt = prnt_str('~', '>', ' ', PURPLE, BLUE, ORANGE)
    def nothing():
        pass
    todoist_cli.emptyline = nothing
    todoist_cli.cmdqueue.append('projects')
    todoist_cli.cmdloop(prnt_str('todoist', PURPLE))

def main():
    with open(os.path.expanduser('~') + '/.todo.conf') as conf_file:
        conf = json.load(conf_file)
        secret = conf['secret']
        wrapper.init(secret)

    init_cli()

if __name__ == '__main__':
    main()
