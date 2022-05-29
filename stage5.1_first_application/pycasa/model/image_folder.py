# General imports
import os

import pandas as pd
import numpy as np

# ETS imports
from traits.api import Directory, HasStrictTraits, Instance

# Local imports
from .image_file import ImageFile, SUPPORTED_FORMATS


class ImageFolder(HasStrictTraits):
    """ Model to hold an image folder.
    """
    path = Directory

    data = Instance(pd.DataFrame)

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
            return pd.DataFrame({"filename": [], "Num. faces": []})

        data = []
        for filename in os.listdir(self.path):
            file_ext = os.path.splitext(filename)[1].lower()
            if file_ext in SUPPORTED_FORMATS:
                filepath = os.path.join(self.path, filename)
                img_file = ImageFile(filepath=filepath)
                file_data = {"filename": filename, "Num. faces": np.nan}
                try:
                    file_data.update(img_file.metadata)
                except Exception as e:
                    pass
                data.append(file_data)

        return pd.DataFrame(data)
