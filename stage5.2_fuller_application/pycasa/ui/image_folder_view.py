# General imports

# ETS imports
from traits.api import Bool, Button, Instance, observe
from traitsui.api import HGroup, Item, Label, ModelView, Spring, View
from traitsui.ui_editors.data_frame_editor import DataFrameEditor
# Local imports
from ..model.image_folder import ImageFolder


class ImageFolderView(ModelView):
    """ ModelView for an image folder object.
    """
    model = Instance(ImageFolder)

    cancel = Button("Cancel")

    _cancel_clicked = Bool

    scan = Button("Scan for faces...")

    view = View(
        Item("model.path", style="readonly", show_label=False),
        Item("model.data", editor=DataFrameEditor(update="data_updated"),
             show_label=False, visible_when="len(model.data) > 0"),
        HGroup(
            Spring(),
            Label("No images found. No data to show"),
            Spring(),
            visible_when="len(model.data) == 0",
        ),
        HGroup(
            Spring(),
            Item(
                "scan",
                show_label=False,
                enabled_when="len(model.data) > 0 and model.executor_idle",
            ),
            Item(
                "cancel",
                show_label=False,
                enabled_when="not model.executor_idle and not _cancel_clicked",
            ),
            Spring(),
        )
    )

    @observe("scan")
    def scan_for_faces(self, event):
        self.model.compute_num_faces_background()

    @observe("cancel")
    def _cancel_scan(self, event):
        self.model.future.cancel()
        self._cancel_clicked = True

    @observe("model:future:done")
    def _reset_click_counter(self, event):
        if self.model.future.done:
            self._cancel_clicked = False
