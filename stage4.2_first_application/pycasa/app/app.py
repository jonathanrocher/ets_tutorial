# coding=utf-8
""" TaskApplication object for the Pycasa app.
"""
import logging

from pyface.tasks.api import TasksApplication, TaskFactory
from ..ui.tasks.pycasa_task import PycasaTask

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
