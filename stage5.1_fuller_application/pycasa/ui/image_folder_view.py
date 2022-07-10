from traits.api import Instance
from traitsui.api import (
    HGroup, Item, Label, ModelView, Spring, View
)
from traitsui.ui_editors.data_frame_editor import DataFrameEditor

from pycasa.model.image_folder import ImageFolder

DISPLAYED_COLUMNS = [
    'ApertureValue', 'ExifVersion', 'Model', 'Make', 'LensModel', 'DateTime',
    'ShutterSpeedValue', 'XResolution', 'YResolution'
]


class ImageFolderView(ModelView):
    """ ModelView for a folder of images.
    """
    model = Instance(ImageFolder)

    view = View(
        Item('model.directory', style="readonly", show_label=False),
        Item(
            'model.data',
            editor=DataFrameEditor(),
            show_label=False,
            visible_when="len(model.data) > 0",
        ),
        HGroup(
            Spring(),
            Label("No images found. No data to show"),
            Spring(),
            visible_when="len(model.data) == 0",
        ),
        resizable=True
    )


if __name__ == '__main__':
    from os.path import dirname, join
    import ets_tutorial

    TUTORIAL_DIR = dirname(ets_tutorial.__file__)
    SAMPLE_IMG_DIR = join(TUTORIAL_DIR, "..", "sample_images")

    image_file = ImageFolder(directory=SAMPLE_IMG_DIR)
    view = ImageFolderView(model=image_file)
    view.configure_traits()
