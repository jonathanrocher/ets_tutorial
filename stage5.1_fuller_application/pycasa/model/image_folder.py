
# General imports
import glob
from os.path import expanduser, isdir, split

import pandas as pd

# ETS imports
from traits.api import (
    Directory, HasStrictTraits, Instance, List, observe,
)

# Local imports
from pycasa.model.image_file import ImageFile

SUPPORTED_FORMATS = [".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG"]


class ImageFolder(HasStrictTraits):
    """ Model for a folder of images.
    """
    directory = Directory(expanduser("~"))

    images = List(Instance(ImageFile))

    def __init__(self, **traits):
        super(ImageFolder, self).__init__(**traits)
        import pdb ; pdb.set_trace()
        if not isdir(self.directory):
            msg = f"The provided directory isn't a real directory: " \
                  f"{self.directory}"
            raise ValueError(msg)

    @observe("directory")
    def _get_images(self, event):
        self.images = [
            ImageFile(filepath=file)
            for fmt in SUPPORTED_FORMATS
            for file in glob.glob(f"{self.directory}/*{fmt}")
        ]

    def create_metadata_df(self):
        return pd.DataFrame(
            [img.metadata for img in self.images],
            index=[split(img.filepath)[1] for img in self.images]
        )
