from traits.api import Instance, Property
from traitsui.api import Item, ModelView, View
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

    metadata_df = Property(depends_on="model.images.items")

    view = View(
        Item('model.directory', style="readonly", show_label=False),
        Item(
            'metadata_df',
            editor=DataFrameEditor(columns=DISPLAYED_COLUMNS),
            show_label=False,
            width=1200,
        ),
        resizable=True
    )

    def _get_metadata_df(self):
        return self.model.create_metadata_df()


if __name__ == '__main__':
    from os.path import dirname, join
    import ets_tutorial

    TUTORIAL_DIR = dirname(ets_tutorial.__file__)
    SAMPLE_IMG_DIR = join(TUTORIAL_DIR, "..", "sample_images")

    image_file = ImageFolder(directory=SAMPLE_IMG_DIR)
    view = ImageFolderView(model=image_file)
    view.configure_traits()
