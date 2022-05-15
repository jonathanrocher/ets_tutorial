# General imports
import PIL.Image
from PIL.ExifTags import TAGS
import numpy as np

# ETS imports
from traits.api import Dict, File, HasStrictTraits, observe


class ImageFile(HasStrictTraits):
    """ Model to hold an image file.
    """
    filepath = File

    metadata = Dict

    def to_array(self):
        with PIL.Image.open(self.filepath) as img:
            return np.asarray(img)

    @observe("filepath")
    def load_metadata(self, event):
        with PIL.Image.open(self.filepath) as img:
            exif = img._getexif()

        if exif:
            self.metadata = {TAGS[k]: v for k, v in exif.items()
                             if k in TAGS}
