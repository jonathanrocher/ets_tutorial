# General imports
import PIL.Image
from PIL.ExifTags import TAGS
import numpy as np

# ETS imports
from traits.api import cached_property, Dict, File, HasStrictTraits, Property


class ImageFile(HasStrictTraits):
    """ Model to hold an image file.
    """
    filepath = File

    metadata = Property(Dict, depends_on="filepath")

    def to_array(self):
        if not self.filepath:
            return np.array([])

        with PIL.Image.open(self.filepath) as img:
            return np.asarray(img)

    @cached_property
    def _get_metadata(self):
        if not self.filepath:
            return {}

        with PIL.Image.open(self.filepath) as img:
            exif = img._getexif()

        if exif:
            return {TAGS[k]: v for k, v in exif.items()
                    if k in TAGS}
        else:
            return {}
