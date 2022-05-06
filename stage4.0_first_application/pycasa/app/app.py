# coding=utf-8
""" TaskApplication object for the Pycasa app.
"""
import logging

from pyface.tasks.api import TasksApplication, TaskFactory
from ..ui.tasks.hello_world_task import HelloWorldTask

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
                id='pycasa.hello_world_task',
                name="Hellow World Editor",
                factory=HelloWorldTask
            )
        ]
