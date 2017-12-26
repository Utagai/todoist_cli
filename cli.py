import readline
import rlcompleter
from cmd import Cmd

import wrapper
from objects import Project
from cli_helpers import parse, arglen, inject, state
import cli_helpers as cli
from state import CLIState

class TodoistCLI(Cmd):

    def __init__(self):
        super().__init__()
        self.state = CLIState()

    @parse
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
    
    @parse
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

    def do_task(self, args):
        """
        Performs task operations.

        Takes the arguments (operations):
            1: create <name> - Creates a task with the given name.
            2: show   <id>   - Shows some selected information about the task
                               with given id.
            3: delete <id>   - Deletes the task with the given id.
            4: done   <id>   - Sets the task with the given id as completed.
        """
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
