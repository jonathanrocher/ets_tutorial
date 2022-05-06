from traits.api import Instance

from traitsui.api import InstanceEditor, Item, ModelView, View

from ..model.hello_world import HelloWorldModel


class HelloWorldView(ModelView):
    model = Instance(HelloWorldModel, ())

    def traits_view(self):
        return View(
            Item("model.content")
        )
