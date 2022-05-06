from pyface.tasks.api import EditorAreaPane, IEditor, IEditorAreaPane, \
    PaneItem, Task, TraitsTaskPane

from traitsui.api import InstanceEditor, Item, ModelView, View
from traits.api import HasStrictTraits, Instance, Str


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

    hello_world_view = Instance(HelloWorldView, ())

    def traits_view(self):
        return View(
            Item("hello_world_view", editor=InstanceEditor(), style="custom",
                 show_label=False)
        )
