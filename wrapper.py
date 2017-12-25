class TodoistWrapper:
    def __init__(self, secret):
        # Inititalize todoist api object with secret
        self.todoist = None

    def get_projects(self):
        print("Retrieving all projects.")
        pass

    def get_tasks(self):
        print("Retrieving all tasks.")
        pass

    def get_project(self, project_id):
        print("Fetching project with id: {}".format(project_id))
        pass

    def new_project(self, project_name):
        print("Creating new project with name: {}".format(project_name))
        pass

    def remove_project(self, project_id):
        print("Removing project with id: {}".format(project_id))
        pass

    def add_task(self, task_name, project_id):
        print("Adding task with name {} to project with id: {}".format(
            task_name, project_id))
        pass

    def add_subtask(self, task_name, task_id):
        print("Adding subtask with name {} to task with id: {}".format(
            task_name, task_id))
        pass

    def done_task(self, task_id):
        print("Completing task with id: {}".format(task_id))
        pass

    def remove_task(self, task_id):
        print("Removing task with id: {}".format(task_id))
        pass
