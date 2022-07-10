""" Script analyzing an image, detecting human faces inside it, and printing
EXIF data about it.
"""
import PIL.Image
from PIL.ExifTags import TAGS
from skimage import data
from skimage.feature import Cascade
import matplotlib.pyplot as plt
from matplotlib import patches
from os.path import join
import numpy as np

# ETS imports
from traits.api import Dict, File, HasStrictTraits, List, observe


class ImageFile(HasStrictTraits):
    """ Model to hold an image file.
    """
    filepath = File

    faces = List

    metadata = Dict

    def to_array(self):
        with PIL.Image.open(self.filepath) as img:
            return np.asarray(img)

    @observe("filepath")
    def update_metadata(self, event):

        with PIL.Image.open(self.filepath) as img:
            exif = img._getexif()
        self.metadata = {TAGS[k]: v for k, v in exif.items()
                         if k in TAGS}

    def detect_faces(self):
        # Load the trained file from the module root.
        trained_file = data.lbp_frontal_face_cascade_filename()

        # Initialize the detector cascade.
        detector = Cascade(trained_file)

        detected = detector.detect_multi_scale(img=self.to_array(),
                                               scale_factor=1.2,
                                               step_ratio=1,
                                               min_size=(60, 60),
                                               max_size=(600, 600))
        self.faces = detected

        self.metadata["Number of faces detected"] = len(detected)


if __name__ == "__main__":

    # Select image file -------------------------------------------------------

    image_path = join("..", "sample_images", "IMG-0311_xmas_2020.JPG")
    image_path2 = join("..", "sample_images", "20210802_191429.jpg")

    img = ImageFile()
    for path in [image_path, image_path2]:

        img.filepath = path

        # Detect faces --------------------------------------------------------

        img.detect_faces()

        print(img.metadata)

        # Visualize results ---------------------------------------------------

        plt.imshow(img.to_array())
        img_desc = plt.gca()
        plt.set_cmap('gray')

        for patch in img.faces:

            img_desc.add_patch(
                patches.Rectangle(
                    (patch['c'], patch['r']),
                    patch['width'],
                    patch['height'],
                    fill=False,
                    color='r',
                    linewidth=2
                )
            )

        plt.show()
