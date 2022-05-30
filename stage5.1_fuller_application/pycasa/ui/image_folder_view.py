# General imports

# ETS imports
from traits.api import Instance
from traitsui.api import Item, ModelView, View
from traitsui.ui_editors.data_frame_editor import DataFrameEditor
# Local imports
from ..model.image_folder import ImageFolder


class ImageFolderView(ModelView):
    """ ModelView for an image folder object.
    """
    model = Instance(ImageFolder)

    view = View(
        Item("model.path", style="readonly", show_label=False),
        Item("model.data", editor=DataFrameEditor(), style="readonly",
             show_label=False)
    )
