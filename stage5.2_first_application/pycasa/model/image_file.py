# General imports
import os
import PIL.Image
from PIL.ExifTags import TAGS
from skimage import data
from skimage.feature import Cascade
import matplotlib.pyplot as plt
import numpy as np

# ETS imports
from traits.api import cached_property, Dict, File, HasStrictTraits, Property

SUPPORTED_FORMATS = [".png", ".jpg", ".jpeg"]


class ImageFile(HasStrictTraits):
    """ Model to hold an image file.
    """
    filepath = File

    metadata = Property(Dict, depends_on="filepath")

    def to_array(self):
        file_ext = os.path.splitext(self.filepath)[1].lower()
        if not self.filepath or file_ext not in SUPPORTED_FORMATS:
            return np.array([])

        with PIL.Image.open(self.filepath) as img:
            return np.asarray(img)

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

    def detect_faces(self):
        """ Detect faces in the image.
        """
        # Load the trained file from the module root.
        trained_file = data.lbp_frontal_face_cascade_filename()

        # Initialize the detector cascade.
        detector = Cascade(trained_file)

        img = plt.imread(self.filepath)

        faces = detector.detect_multi_scale(img=img,
                                            scale_factor=1.2,
                                            step_ratio=1,
                                            min_size=(60, 60),
                                            max_size=(600, 600))
        return faces
