# General imports
import os

import pandas as pd
import numpy as np

# ETS imports
from traits.api import (
    Bool, Directory, Event, HasStrictTraits, Instance, observe, Property
)
from traits_futures.api import (
    CallFuture, submit_call, TraitsExecutor
)

# Local imports
from .image_file import ImageFile, SUPPORTED_FORMATS

FILENAME_COL = "filename"

NUM_FACE_COL = "Num. faces"


class ImageFolder(HasStrictTraits):
    """ Model to hold an image folder.
    """
    path = Directory

    data = Instance(pd.DataFrame)

    data_updated = Event

    traits_executor = Instance(TraitsExecutor)

    future = Instance(CallFuture)

    executor_idle = Property(Bool, observe="future.done")

    def __init__(self, **traits):
        # Don't forget this!
        super(ImageFolder, self).__init__(**traits)
        if not os.path.isdir(self.path):
            msg = f"Unable to create an ImageFolder from {self.path} since" \
                  f" it is not a valid directory."
            raise ValueError(msg)

        self.data = self.to_dataframe()

    def to_dataframe(self):
        if not self.path:
            return pd.DataFrame({FILENAME_COL: [], NUM_FACE_COL: []})

        data = []
        for filename in os.listdir(self.path):
            file_ext = os.path.splitext(filename)[1].lower()
            if file_ext in SUPPORTED_FORMATS:
                filepath = os.path.join(self.path, filename)
                img_file = ImageFile(filepath=filepath)
                file_data = {FILENAME_COL: filename, NUM_FACE_COL: np.nan}
                try:
                    file_data.update(img_file.metadata)
                except Exception as e:
                    pass
                data.append(file_data)

        return pd.DataFrame(data)

    def compute_num_faces_background(self, **kwargs):
        self.future = submit_call(
            self.traits_executor,
            self._compute_num_faces,
            **kwargs
        )

    def _compute_num_faces(self, **kwargs):
        image_files = [
            ImageFile(filepath=os.path.join(self.path, filename))
            for filename in self.data[FILENAME_COL]
        ]
        return [
            len(img_file.detect_faces(**kwargs)) for img_file in image_files
        ]

    @observe("future:done")
    def _update_df(self, event):
        num_faces_all_images = self.future.result
        for img_idx, num_faces in enumerate(num_faces_all_images):
            self.data.at[img_idx, NUM_FACE_COL] = num_faces
        self.data_updated = True

    def _get_executor_idle(self):
        return self.future is None or self.future.done
