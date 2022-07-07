# coding=utf-8
""" TaskApplication object for the Pycasa app.
"""
import logging

from traits.api import Tuple, Int
from pyface.tasks.api import TasksApplication, TaskFactory
from pyface.api import SplashScreen
from pyface.action.api import Action
from pyface.action.schema.api import SchemaAddition, SGroup

from ..ui.tasks.pycasa_task import PycasaTask
from ..ui.image_resources import app_icon, new_icon

logger = logging.getLogger(__name__)


class PycasaApplication(TasksApplication):
    """ An application to say hello.
    """
    id = "pycasa_application"

    name = "Pycasa"

    description = "An example Tasks application that explores image files."

    def _task_factories_default(self):
        return [
            TaskFactory(
                id='pycasa.pycasa_task_factory',
                name="Main Pycasa Task Factory",
                factory=PycasaTask
            )
        ]

    def _icon_default(self):
        return app_icon

    def _splash_screen_default(self):
        splash_screen = SplashScreen(image=app_icon)
        return splash_screen

    def create_new_task_window(self):
        from pyface.tasks.task_window_layout import TaskWindowLayout

        layout = TaskWindowLayout()
        layout.items = [self.task_factories[0].id]
        window = self.create_window(layout=layout)
        self.add_window(window)
        window.title += " {}".format(len(self.windows))
        return window

    def create_new_task_menu(self):
        return SGroup(
            Action(name="New",
                   accelerator='Ctrl+N',
                   on_perform=self.create_new_task_window,
                   image=new_icon),
            id='NewGroup', name='NewGroup',
        )

    def _extra_actions_default(self):
        extra_actions = [
            SchemaAddition(id='pycasa.custom_new',
                           factory=self.create_new_task_menu,
                           path="MenuBar/File/OpenGroup",
                           absolute_position="first")
        ]
        return super(PycasaApplication, self)._extra_actions_default() + \
            extra_actions
