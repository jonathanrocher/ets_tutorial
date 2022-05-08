import PIL.Image
from PIL.ExifTags import TAGS

from traits.api import Dict, File, HasStrictTraits, observe, Property


class ImageFile(HasStrictTraits):
    """ Model to hold an image file.
    """
    filepath = File

    metadata = Dict

    @observe("filepath")
    def load_metadata(self, event):
        img = PIL.Image.open(self.filepath)
        exif = img._getexif()
        if exif:
            self.metadata = {TAGS[k]: v for k, v in exif.items()
                             if k in TAGS}
