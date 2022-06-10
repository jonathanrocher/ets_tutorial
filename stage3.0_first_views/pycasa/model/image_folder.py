import glob
from os.path import expanduser, split

import pandas as pd

from traits.api import (
    Directory, HasStrictTraits, Instance, List, observe,
)

from pycasa.model.image_file import ImageFile

SUPPORTED_FORMATS = [".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG"]


class ImageFolder(HasStrictTraits):
    """ Model for a folder of images.
    """
    directory = Directory(expanduser("~"))

    images = List(Instance(ImageFile))

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
