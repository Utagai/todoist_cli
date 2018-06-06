import json
import os
import colored

from cli import TodoistCLI
import wrapper
from conf_schema import conf_filename, validate_conf
from color import prnt_str, PURPLE, ORANGE, BLUE

def init_cli(conf):
    todoist_cli = TodoistCLI(conf)
    todoist_cli.prompt = prnt_str('~', '>', ' ', PURPLE, BLUE, ORANGE)
    def nothing():
        pass
    todoist_cli.emptyline = nothing
    todoist_cli.cmdqueue.append('projects')
    todoist_cli.cmdloop(prnt_str('todoist', PURPLE))

def main():
    conf_filepath = os.path.join(os.path.expanduser('~'), conf_filename)
    with open(conf_filepath) as conf_file:
        conf_json = json.load(conf_file)
        conf = validate_conf(conf_json)
        wrapper.init(conf)

    init_cli(conf)

if __name__ == '__main__':
    main()
