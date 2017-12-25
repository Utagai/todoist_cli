from todoist_cli import TodoistCLI 

if __name__ == '__main__':
    todoist_cli = TodoistCLI()
    todoist_cli.prompt = '~> '
    todoist_cli.cmdloop('todoist CLI')
