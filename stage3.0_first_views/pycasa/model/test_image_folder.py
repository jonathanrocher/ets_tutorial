from os.path import dirname, join, split
import unittest

from image_folder import ImageFolder

import ets_tutorial

TUTORIAL_DIR = dirname(ets_tutorial.__file__)
SAMPLE_IMG_DIR = join(TUTORIAL_DIR, "..", "sample_images")


class TestImageFolder(unittest.TestCase):
    def test_filters_images(self):
        img_folder = ImageFolder(directory=SAMPLE_IMG_DIR)
        self.assertEqual(
            sorted([split(img.filepath)[1] for img in img_folder.images]),
            sorted(["IMG-0311_xmas_2020.JPG", "owls.jpg"])
        )
