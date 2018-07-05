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
    if conf["default_project"]:
        project_selection_cmd = 'select %s:"{}"'.format(conf["default_project"])
        config_comment = " # Auto-injected from config file (default_project)."
        todoist_cli.cmdqueue.append(project_selection_cmd + config_comment)
    todoist_cli.cmdloop(prnt_str('todoist', PURPLE))

def main():
    conf = TodoConfig.get_config()

    wrapper.init(conf)
    init_cli(conf)

if __name__ == '__main__':
    main()
