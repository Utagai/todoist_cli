import readline
import rlcompleter
from cmd import Cmd

import wrapper
from objects import Task, Project
from cli_helpers import arglen, inject, state, emptystate, restrict, command
import cli_helpers as cli
from cmd_error import CmdError
from state import CLIState

class TodoistCLI(Cmd):

    def __init__(self):
        super().__init__()
        self.cli_state = CLIState()

    @command
    @arglen(0)
    @state
    def do_projects(self, args):
        """
        Retrieves a listing of all project names and their ids.

        Takes no arguments.
        """
        projects = wrapper.todoist.get_projects()
        cli.print_listing(projects, 0)
        return projects
    
    @command
    @arglen(0, 1)
    @inject
    @state
    def do_tasks(self, args):
        """
        Retrieves a listing of all tasks.

        Takes an optional project name or id, only listing the tasks of the
        given project.
        """
        project_id = None
        if args:
            project_id = args[0]

        pos = 0
        if project_id:
            project = Project(project_id)
            print("<{}>".format(project))
            pos = cli.print_listing(project, pos)
            return project.tasks
        else:
            projects = wrapper.todoist.get_projects()
            tasks = []
            for project in projects:
                print("<{}>".format(project))
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
            4: complete <id>   - Sets the task with the given id as completed.
        """
        sub_cmd = args[0]
        if sub_cmd == 'create':
            print("Creating with name {}".format(args[1]))
            if not self.cli_state.active_project:
                raise CmdError("No active project. Use the select command.")
            proj_id = self.cli_state.active_project.obj_id
            wrapper.todoist.create_task(args[1], proj_id)
            pass
        elif sub_cmd == 'complete':
            print("Completing id {}".format(args[1]))
            try:
                task = Task(int(args[1]))
                task.complete()
            except ValueError:
                raise CmdError("Task id must be an integer.")
            pass

    @command
    @arglen(1)
    @inject
    def do_select(self, args):
        try:
            self.cli_state.set_project(int(args[0]))
            self.prompt = '~({})> '.format(self.cli_state.active_project.name)
        except (ValueError, CmdError):
            raise CmdError("Argument must be a project id.")
        pass

    def do_project(self, args):
        """
        Performs project operations.

        Takes the arguments (operations):
            1: create <name> - Creates a project with the given name.
            2: show   <id>   - Shows some selected information about the project
                               with the given id.
            3: delete <id>   - Deletes the project with the given id and its
                               constituent tasks.
            4: done   <id>   - Sets all constituent tasks in the project with
                               given id as completed.
            5: clear  <id>   - Clears all tasks in the project with the given 
                               id.
        """
        pass

    def do_exit(self, args):
        """
        Exits the CLI application.
        """
        print("Bye")
        exit(0)
