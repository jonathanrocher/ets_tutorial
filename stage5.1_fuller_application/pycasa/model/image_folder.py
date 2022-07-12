
# General imports
import glob
from os.path import basename, expanduser, isdir

import numpy as np
import pandas as pd

# ETS imports
from traits.api import (
    Directory, HasStrictTraits, Instance, List, observe,
)

# Local imports
from pycasa.model.image_file import ImageFile, SUPPORTED_FORMATS

FILENAME_COL = "filename"
NUM_FACE_COL = "Num. faces"


class ImageFolder(HasStrictTraits):
    """ Model for a folder of images.
    """
    directory = Directory(expanduser("~"))

    images = List(Instance(ImageFile))

    data = Instance(pd.DataFrame)

    def __init__(self, **traits):
        # Don't forget this!
        super(ImageFolder, self).__init__(**traits)
        if not isdir(self.directory):
            msg = f"The provided directory isn't a real directory: " \
                  f"{self.directory}"
            raise ValueError(msg)
        self.data = self._create_metadata_df()

    @observe("directory")
    def _update_images(self, event):
        self.images = [
            ImageFile(filepath=file)
            for fmt in SUPPORTED_FORMATS
            for file in glob.glob(f"{self.directory}/*{fmt}")
        ]

    @observe("images.items")
    def _update_metadata(self, event):
        self.data = self._create_metadata_df()

    def _create_metadata_df(self):
        if not self.images:
            return pd.DataFrame({FILENAME_COL: [], NUM_FACE_COL: []})
        return pd.DataFrame([
                {
                    FILENAME_COL: basename(img.filepath),
                    NUM_FACE_COL: np.nan,
                    **img.metadata

                }
                for img in self.images
        ])
