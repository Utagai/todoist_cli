import colored

from cli import TodoistCLI
import wrapper
from conf_schema import TodoConfig
from color import prnt_str, PURPLE, ORANGE, BLUE

def init_cli(conf):
    todoist_cli = TodoistCLI(conf)
    todoist_cli.prompt = prnt_str('~', '>', ' ', PURPLE, BLUE, ORANGE)
    todoist_cli.emptyline = lambda *args: None
    todoist_cli.cmdqueue.append('projects')
    todoist_cli.cmdloop(prnt_str('todoist', PURPLE))

def main():
    conf = TodoConfig.get_config()

    wrapper.init(conf)
    init_cli(conf)

if __name__ == '__main__':
    main()
