from cmd import Cmd

import wrapper
from objects import Project
from color import prnt, prnt_str, VIOLET, PURPLE, ORANGE, TURQ, BLUE
from cli_helpers import arglen, inject, state, emptystate, restrict, command
from cli_helpers import CmdError
import cli_helpers as cli
from state import CLIState


class TodoistCLI(Cmd):

    def __init__(self, conf):
        super().__init__()
        self.conf = conf
        self._wrapper = wrapper.TodoistWrapper(self.conf)
        self.state = CLIState(self._wrapper)
        self.prompt = prnt_str('~', '>', ' ', PURPLE, BLUE, ORANGE)
        self.emptyline = lambda *args: None
        self.cmdqueue.append('projects')
        default_proj = conf["default_project"]
        if default_proj:
            project_selection_cmd = 'select %s:"{}"'.format(default_proj)
            config_comment = " # Auto-injected from config " \
                + "file (default_project)."
            self.cmdqueue.append(project_selection_cmd + config_comment)

    def do(self):
        """
        This function begins the cmdloop for TodoistCLI, and will not return
        until the application exits.
        """
        self.cmdloop(prnt_str('todoist', PURPLE))

    @command
    @arglen(0)
    @state
    def do_projects(self, args):
        """
        Retrieves a listing of all project names and their ids.

        Takes no arguments.
        """
        projects = self._wrapper.get_projects()
        cli.print_listing(projects, 0)
        return projects

    @command
    @arglen(0, 1)
    @inject
    @state
    def do_tasks(self, args):
        """
        Retrieves a listing of all tasks for the currently active project, if
        available. If there is no currently active project, simply lists all
        tasks across all projects.

        Takes an optional project name or id, only listing the tasks of the
        given project.
        """
        project_id = None
        if self.state.active_project:
            project_id = self.state.active_project.obj_id
        elif args:
            project_id = args[0]

        pos = 0
        if project_id:
            project = Project(self._wrapper, project_id)
            prnt('<', project, '>', VIOLET, None, VIOLET)
            pos = cli.print_listing(project, pos)
            return project.tasks
        else:
            projects = self._wrapper.get_projects()
            tasks = []
            for project in projects:
                prnt('<', project, '>', VIOLET, None, VIOLET)
                pos = cli.print_listing(project, pos)
                tasks.extend(project.tasks)
            return tasks

    @command
    @arglen(2)
    @inject
    @restrict(['create', 'complete'])
    @emptystate
    def do_task(self, args):
        """
        Performs task operations.

        Takes the arguments (operations):
            1: create   <name> - Creates a task with the given name in the
                                 currently selected project.
            2: complete <id>   - Sets the task with the given id as completed.
        """
        sub_cmd = args[0]
        if sub_cmd == 'create':
            if self.state.active_project is None:
                raise CmdError("No active project. Use the select command")
            proj_id = self.state.active_project.obj_id
            self._wrapper.create_task(args[1], proj_id)
        elif sub_cmd == 'complete':
            self._wrapper.complete_task(args[1])

        self.do_tasks(str(self.state.active_project.obj_id))

    @command
    @arglen(1)
    @inject
    def do_select(self, args):
        """
        Sets the project with the given id as the currently selected project.

        All commands that implicitly act on a project with use this selected
        project. An example is task create.
        """
        try:
            self.state.set_project(int(args[0]))
            self.prompt = prnt_str(
                    '~',
                    '(', self.state.active_project.name, ')',
                    '>',
                    ' ',
                    PURPLE, TURQ, PURPLE, TURQ, BLUE, ORANGE
                    )
        except (ValueError, CmdError):
            raise CmdError("Argument must be a valid project")

    @command
    @arglen(2)
    @inject
    @restrict(['create', 'complete', 'clear', 'delete'])
    @emptystate
    def do_project(self, args):
        """
        Performs project operations.

        Takes the arguments (operations):
            1: create   <name> - Creates a project with the given name.
            2: complete <id>   - Sets all constituent tasks in the project with
                                 given id as completed.
            3: clear    <id>   - Delete all tasks in the project with the
                                 given id.
            4: delete   <id>   - Delete the project.
        """
        sub_cmd = args[0]
        if sub_cmd == 'create':
            self._wrapper.create_project(args[1])
        elif sub_cmd == 'complete':
            self._wrapper.complete_project(args[1])
        elif sub_cmd == 'clear':
            self._wrapper.clear_project(args[1])
        elif sub_cmd == 'delete':
            self._wrapper.delete_project(args[1])

    @command
    @arglen(0)
    @emptystate
    def do_exit(self, args):
        """
        Exits the CLI application.
        """
        prnt("Bye", VIOLET)
        exit(0)

    def onecmd(self, line):
        """
        An override of Cmd's onecmd(), so that we do not follow the currently
        default behavior of the Cmd module, which I think is dumb, and is that
        whenever a non-falsey value is returned from a do_cmd() function, we
        should stop. Instead, this makes it so that we only stop if we get back
        an error from running a command.
        """
        try:
            super().onecmd(line)
            return False
        except CmdError as err:
            # This code path should actually never happen since do_cmd()
            # methods should be wrapped with the @command decorator, so we
            # throw in this case to make it clear that our code is somehow,
            # somewhere wrong.
            assert err is not None, "CmdError's should _always_ be caught"
            raise
        except Exception as err:
            return err
