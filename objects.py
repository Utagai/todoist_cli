import wrapper
from cmd_error import CmdError

class _TodoistObject:
    def __init__(self, obj_id = None, name = None):
        if obj_id:
            self.obj_id = obj_id
            self._raw = None
            self._populate()
        else:
            self.name = name
    
    def _populate(self):
        raise NotImplementedError
    
    def save(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    def __str__(self):
        return "{} ({})".format(self.name, self.obj_id)

class Task(_TodoistObject):
    def _populate(self):
        self._raw = wrapper.todoist.task_data(self.obj_id)
        self.name = self._raw['item']['content']
        self.date = self._raw['item']['date_added']
        self.project_id = self._raw['project']['id']

    def complete(self):
        pass

    def _from_raw(raw):
        task = Task(name = raw['content'])
        task.obj_id = raw['id']
        task.date = raw['date_added']
        task.project_id = raw['project_id']
        return task

    @property
    def project(self):
        if self.project is None:
            self.project = wrapper.todoist.project_data(self.project_id)
        
        return self.project

class Project(_TodoistObject):
    def _populate(self):
        self._raw = wrapper.todoist.project_data(self.obj_id)
        if 'error' in self._raw:
            raise CmdError(str(self._raw['error']))
        project = self._raw['project']
        self.name = self._raw['project']['name']
        self._tasks = None

    @property
    def tasks(self):
        if self._tasks is None:
            self._tasks = [Task._from_raw(raw) for raw in self._raw['items']]

        return self._tasks

    def __iter__(self):
        return iter(self.tasks) 

    def __len__(self):
        return len(self.tasks)
