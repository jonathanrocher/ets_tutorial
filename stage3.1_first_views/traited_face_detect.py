# General imports
from os.path import splitext
import PIL.Image
import numpy as np
from matplotlib import patches
from matplotlib.figure import Figure
from PIL.ExifTags import TAGS
from skimage import data
from skimage.feature import Cascade

# ETS imports
from traits.api import (
    Array, cached_property, Dict, File, HasStrictTraits, Instance, List,
    observe, Property
)
from traitsui.api import Item, ModelView, OKButton, View

# Local imports
from ets_tutorial.util.mpl_figure_editor import MplFigureEditor

SUPPORTED_FORMATS = [".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG"]


class ImageFile(HasStrictTraits):
    """ Model to hold an image file.
    """
    filepath = File

    metadata = Property(Dict, depends_on="filepath")

    data = Property(Array, depends_on="filepath")

    faces = List

    def _is_valid_file(self):
        return (
            bool(self.filepath) and
            splitext(self.filepath)[1].lower() in SUPPORTED_FORMATS
        )

    @cached_property
    def _get_data(self):
        if not self._is_valid_file():
            return np.array([])
        with PIL.Image.open(self.filepath) as img:
            return np.asarray(img)

    @cached_property
    def _get_metadata(self):
        if not self._is_valid_file():
            return {}
        with PIL.Image.open(self.filepath) as img:
            exif = img._getexif()
        if not exif:
            return {}
        return {TAGS[k]: v for k, v in exif.items() if k in TAGS}

    def detect_faces(self):
        # Load the trained file from the module root.
        trained_file = data.lbp_frontal_face_cascade_filename()

        # Initialize the detector cascade.
        detector = Cascade(trained_file)

        detected = detector.detect_multi_scale(img=self.data,
                                               scale_factor=1.2,
                                               step_ratio=1,
                                               min_size=(60, 60),
                                               max_size=(600, 600))
        self.faces = detected
        return self.faces


class ImageFileView(ModelView):
    """ ModelView for an image file object.
    """
    model = Instance(ImageFile)

    figure = Instance(Figure)

    view = View(
        Item("model.filepath", show_label=False),
        Item("figure", editor=MplFigureEditor(), show_label=False),
        buttons=[OKButton],
        resizable=True,
        title="Pycasa"
    )

    @observe("model.filepath")
    def build_mpl_figure(self, event):
        if not self.model.filepath:
            return
        figure = Figure()
        axes = figure.add_subplot(111)
        axes.imshow(self.model.data)
        for patch in self.model.detect_faces():
            axes.add_patch(
                patches.Rectangle(
                    (patch['c'], patch['r']),
                    patch['width'],
                    patch['height'],
                    fill=False,
                    color='r',
                    linewidth=2
                )
            )
        self.figure = figure


if __name__ == '__main__':
    img = ImageFile()
    view = ImageFileView(model=img)
    view.configure_traits()
