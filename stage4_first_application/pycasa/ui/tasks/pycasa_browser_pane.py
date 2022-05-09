# General imports

# ETS imports
from traits.api import HasStrictTraits, Instance, observe, Str
from traitsui.api import InstanceEditor, Item, ModelView, View
from pyface.tasks.api import EditorAreaPane, IEditor, IEditorAreaPane, \
    PaneItem, Task, TraitsDockPane

# Local imports
from ..file_browser_view import FileBrowserView


class PycasaBrowserPane(TraitsDockPane):

    id = 'pycasa.file_browser_pane'

    file_browser_view = Instance(FileBrowserView, ())

    def traits_view(self):
        return View(
            Item("file_browser_view", editor=InstanceEditor(), style="custom",
                 show_label=False)
        )

    @observe("file_browser_view.model.requested_item")
    def open_in_central_pane(self, event):
        self.task.open_in_central_pane(event.new)
