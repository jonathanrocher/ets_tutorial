# General imports
import glob
from os.path import basename, expanduser, isdir

import numpy as np
import pandas as pd

# ETS imports
from traits.api import (
    Bool, Directory, Event, HasStrictTraits, Instance, List, observe, Property
)
from traits_futures.api import (
    CallFuture, submit_call, TraitsExecutor
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

    data_updated = Event

    traits_executor = Instance(TraitsExecutor)

    future = Instance(CallFuture)

    executor_idle = Property(Bool, depends_on="future.done")

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

    def compute_num_faces_background(self, **kwargs):
        self.future = submit_call(
            self.traits_executor,
            self._compute_num_faces,
            **kwargs
        )

    def _compute_num_faces(self, **kwargs):
        return [
            len(img_file.detect_faces(**kwargs))
            for img_file in self.images
        ]

    @observe("future:done")
    def _update_data(self, event):
        num_faces_all_images = self.future.result
        for idx, num_faces in enumerate(num_faces_all_images):
            self.data[NUM_FACE_COL].iat[idx] = num_faces
        self.data_updated = True

    def _get_executor_idle(self):
        return self.future is None or self.future.done
