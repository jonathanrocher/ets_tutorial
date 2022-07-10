# General imports

# ETS imports
from traits.api import Button, Instance, observe
from traitsui.api import HGroup, Item, Label, ModelView, Spring, View
from traitsui.ui_editors.data_frame_editor import DataFrameEditor
# Local imports
from ..model.image_folder import ImageFolder


class ImageFolderView(ModelView):
    """ ModelView for an image folder object.
    """
    model = Instance(ImageFolder)

    scan = Button("Scan for faces...")

    view = View(
        Item("model.directory", style="readonly", show_label=False),
        Item(
            "model.data",
            editor=DataFrameEditor(update="data_updated"),
            show_label=False,
            visible_when="len(model.data) > 0"),
        HGroup(
            Spring(),
            Label("No images found. No data to show"),
            Spring(),
            visible_when="len(model.data) == 0",
        ),
        HGroup(
            Spring(),
            Item("scan", show_label=False, enabled_when="len(model.data) > 0"),
            Spring(),
        )
    )

    @observe("scan")
    def scan_for_faces(self, event):
        self.model.compute_num_faces()
