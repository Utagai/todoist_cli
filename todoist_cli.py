import readline
import rlcompleter
from cmd import Cmd

from wrapper import TodoistWrapper

#class ArgCount:
#    def __init__(self, do):
#

class TodoistCLI(Cmd):
    todoist = TodoistWrapper('secret')

    def do_projects(self, args):
        """
        Retrieves a listing of all project names and their ids.

        Takes no arguments.
        """
        pass
    
    def do_tasks(self, args):
        """
        Retrieves a listing of all tasks.

        Takes an optional project name or id, only listing the tasks of the
        given project.
        """
        pass

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
