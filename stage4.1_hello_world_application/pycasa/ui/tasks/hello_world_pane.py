from pyface.tasks.api import TraitsTaskPane

from traitsui.api import InstanceEditor, Item, View
from traits.api import Instance

from ..hello_world_view import HelloWorldView


class HelloWorldPane(TraitsTaskPane):

    hello_world_view = Instance(HelloWorldView, ())

    def traits_view(self):
        return View(
            Item("hello_world_view", editor=InstanceEditor(), style="custom",
                 show_label=False)
        )
