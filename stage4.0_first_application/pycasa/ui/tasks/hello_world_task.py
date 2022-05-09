
from pyface.tasks.api import Task
from .hello_world_pane import HelloWorldPane


class HelloWorldTask(Task):
    # 'Task' traits -----------------------------------------------------------

    #: The unique id of the task.
    id = "pycasa.hello_world_task"

    #: The human-readable name of the task.
    name = "Python Editor"

    def create_central_pane(self):
        """ Create the central pane: the script editor.
        """
        return HelloWorldPane()
