# General imports
from os.path import splitext
import PIL.Image
from PIL.ExifTags import TAGS
from skimage import data
from skimage.feature import Cascade
import numpy as np

# ETS imports
from traits.api import (
    Array, cached_property, Dict, File, HasStrictTraits, List, Property
)

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
