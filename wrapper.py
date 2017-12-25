from todoist import TodoistAPI

from objects import Task, Project

todoist = None

def wrapper_init(secret):
    global todoist
    todoist = TodoistWrapper(secret)

class TodoistWrapper:
    def __init__(self, secret):
        self.todoist = TodoistAPI(secret)

    def get_projects(self):
        return [Project(project['id']) for project in self.todoist['projects']]

    def project_data(self, project_id):
        return self.todoist.projects.get_data(project_id)

    def task_data(self, task_id):
        return self.todoist.items.get(task_id)
