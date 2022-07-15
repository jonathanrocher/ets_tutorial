""" Hello world as a single file Pyface application
"""

from traitsui.api import InstanceEditor, Item, ModelView, View
from traits.api import HasStrictTraits, Instance, Str

from pyface.tasks.api import Task, TasksApplication, TaskFactory, \
    TraitsTaskPane


class HelloWorldModel(HasStrictTraits):

    content = Str

    def _content_default(self):
        return "Hello World!"


class HelloWorldView(ModelView):
    model = Instance(HelloWorldModel, ())

    def traits_view(self):
        return View(
            Item("model.content")
        )


class HelloWorldPane(TraitsTaskPane):

    #: The unique id of the task.
    id = "pycasa.hello_world_pane"

    #: The human-readable name of the task.
    name = "Message Viewer Pane"

    hello_world_view = Instance(HelloWorldView, ())

    def traits_view(self):
        return View(
            Item("hello_world_view", editor=InstanceEditor(), style="custom",
                 show_label=False)
        )


class HelloWorldTask(Task):

    #: The unique id of the task.
    id = "pycasa.hello_world_task"

    #: The human-readable name of the task.
    name = "Message Viewer Task"

    def create_central_pane(self):
        """ Create the central pane: the script editor.
        """
        return HelloWorldPane()


class PycasaApplication(TasksApplication):
    """ An application to say hello.
    """
    id = "pycasa_application"

    name = "Pycasa"

    description = "An example Tasks application that explores image files."

    def _task_factories_default(self):
        return [
            TaskFactory(
                id='pycasa.hello_world_task',
                name="Hello World Editor",
                factory=HelloWorldTask
            )
        ]


def main():
    app = PycasaApplication()
    app.run()


if __name__ == '__main__':
    main()
