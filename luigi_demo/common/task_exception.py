class TaskException(Exception):
    def __init__(self, message, task_name):
        super(TaskException, self).__init__(message)
        self.task_name = task_name
