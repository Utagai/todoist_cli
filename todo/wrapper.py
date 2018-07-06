from todoist import TodoistAPI
from objects import Project
from cli_helpers import CmdError

todoist = None


def init(conf):
    global todoist
    todoist = TodoistWrapper(conf)


class TodoistWrapper:
    def __init__(self, conf):
        self.todoist = TodoistAPI(conf['secret'])
        self.conf = conf
        self.todoist.sync()

    def get_projects(self):
        projs = [Project(proj['id']) for proj in self.todoist['projects']]
        if not self.conf['show_inbox']:
            return [proj for proj in projs if proj.name != 'Inbox']
        else:
            return projs

    def project_data(self, project_id):
        return self.todoist.projects.get_data(project_id)

    def task_data(self, task_id):
        return self.todoist.items.get(task_id)

    def create_task(self, name, project_id):
        self.todoist.items.add(name, project_id)
        self.todoist.commit()

    def create_project(self, project_name):
        self.todoist.projects.add(project_name)
        self.todoist.commit()

    def complete_task(self, task_id):
        try:
            self.todoist.items.complete([int(task_id)])
            self.todoist.commit()
        except ValueError:
            raise CmdError("Argument must be a task id.")

    def _get_project_task_ids(self, project_id):
        try:
            project = Project(int(project_id))
            task_ids = [task.obj_id for task in project]
            return task_ids
        except ValueError:
            raise CmdError("Argument must be a project id.")

    def complete_project(self, project_id):
        self.todoist.items.complete(self._get_project_task_ids(project_id))
        self.todoist.commit()

    def clear_project(self, project_id):
        self.todoist.items.delete(self._get_project_task_ids(project_id))
        self.todoist.commit()

    def delete_project(self, project_id):
        self.todoist.projects.delete([project_id])
        self.todoist.commit()
