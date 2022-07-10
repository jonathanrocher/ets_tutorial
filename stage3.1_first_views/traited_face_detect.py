# General imports
import PIL.Image
import numpy as np
from matplotlib import patches
from matplotlib.figure import Figure
from PIL.ExifTags import TAGS
from skimage import data
from skimage.feature import Cascade

# ETS imports
from traits.api import (
    Dict,
    File,
    HasStrictTraits,
    Instance,
    List,
    observe,
)
from traitsui.api import Item, ModelView, OKButton, View

# Local imports
from ets_tutorial.util.mpl_figure_editor import MplFigureEditor


class ImageFile(HasStrictTraits):
    """ Model to hold an image file.
    """
    filepath = File

    faces = List

    metadata = Dict

    def to_array(self):
        if not self.filepath:
            return np.array([])

        with PIL.Image.open(self.filepath) as img:
            return np.asarray(img)

    @observe("filepath")
    def _update_faces_and_metadata(self, event):
        self.metadata = {}
        self._update_metadata_with_exif()
        self._detect_faces()
        print(self.metadata)

    def _update_metadata_with_exif(self):
        if not self.filepath:
            return
        with PIL.Image.open(self.filepath) as img:
            exif = img._getexif()
        if not exif:
            return
        self.metadata.update(
            {TAGS[k]: v for k, v in exif.items() if k in TAGS}
        )

    def _detect_faces(self):
        self.faces = []
        if not self.filepath:
            return
        # Load the trained file from the module root.
        trained_file = data.lbp_frontal_face_cascade_filename()
        # Initialize the detector cascade.
        detector = Cascade(trained_file)
        faces = detector.detect_multi_scale(
            img=self.to_array(),
            scale_factor=1.2,
            step_ratio=1,
            min_size=(60, 60),
            max_size=(600, 600)
        )
        self.faces.extend(faces)
        self.metadata['Number of faces'] = len(self.faces)


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
        axes.imshow(self.model.to_array())
        for patch in self.model.faces:
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
