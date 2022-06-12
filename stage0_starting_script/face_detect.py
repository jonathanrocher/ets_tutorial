""" Script analyzing an image, detecting human faces inside it, and printing
EXIF data about it.
"""
from os.path import join

import PIL.Image
from PIL.ExifTags import TAGS
from skimage import data
from skimage.feature import Cascade
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches

# Select image file -----------------------------------------------------------

image_paths = [
    join("..", "sample_images", "IMG-0311_xmas_2020.JPG"),
    join("..", "sample_images", "owls.jpg")
]

for path in image_paths:
    img = PIL.Image.open(path)

    img_metadata = {TAGS[k]: v for k, v in img._getexif().items() if k in TAGS}

    # Detect faces ------------------------------------------------------------

    # Load the trained file from the module root.
    trained_file = data.lbp_frontal_face_cascade_filename()

    # Initialize the detector cascade.
    detector = Cascade(trained_file)

    detected = detector.detect_multi_scale(img=np.asarray(img),
                                           scale_factor=1.2,
                                           step_ratio=1,
                                           min_size=(60, 60),
                                           max_size=(600, 600))

    img_metadata["Number of faces detected"] = len(detected)
    print(img_metadata)

    # Visualize results -------------------------------------------------------

    plt.imshow(img)
    img_desc = plt.gca()
    plt.set_cmap('gray')

    for patch in detected:

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
