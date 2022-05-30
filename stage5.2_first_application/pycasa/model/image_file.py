# General imports
import os
import PIL.Image
from PIL.ExifTags import TAGS
from skimage import data
from skimage.feature import Cascade
import numpy as np

# ETS imports
from traits.api import Array, cached_property, Dict, File, HasStrictTraits, \
    Property

SUPPORTED_FORMATS = [".png", ".jpg", ".jpeg"]


class ImageFile(HasStrictTraits):
    """ Model to hold an image file.
    """
    filepath = File

    metadata = Property(Dict, depends_on="filepath")

    data = Property(Array, depends_on="filepath")

    def to_array(self):
        file_ext = os.path.splitext(self.filepath)[1].lower()
        if not self.filepath or file_ext not in SUPPORTED_FORMATS:
            return np.array([])

        with PIL.Image.open(self.filepath) as img:
            return np.asarray(img)

    @cached_property
    def _get_data(self):
        return self.to_array()

    @cached_property
    def _get_metadata(self):
        file_ext = os.path.splitext(self.filepath)[1].lower()
        if not self.filepath or file_ext not in SUPPORTED_FORMATS:
            return {}

        with PIL.Image.open(self.filepath) as img:
            exif = img._getexif()

        if exif:
            return {TAGS[k]: v for k, v in exif.items()
                    if k in TAGS}
        else:
            return {}

    def detect_faces(self, scale_factor=1.2, step_ratio=1, min_size=60,
                     max_size=600):
        """ Detect faces in the image.
        """
        trained_file = data.lbp_frontal_face_cascade_filename()
        detector = Cascade(trained_file)
        faces = detector.detect_multi_scale(img=self.data,
                                            scale_factor=scale_factor,
                                            step_ratio=step_ratio,
                                            min_size=(min_size, min_size),
                                            max_size=(max_size, max_size))
        return faces
