# General imports

# ETS imports
from traits.api import Instance
from traitsui.api import Item, ModelView, FileEditor, View

# Local imports
from ..model.file_browser import FileBrowser


class FileBrowserView(ModelView):
    model = Instance(FileBrowser, ())

    def traits_view(self):
        editor = FileEditor(dclick_name="model.requested_item")
        return View(
            Item("model.root", editor=editor, style="custom",
                 show_label=False),
        )
