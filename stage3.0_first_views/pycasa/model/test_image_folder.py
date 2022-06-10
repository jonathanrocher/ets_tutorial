from os.path import dirname, join, split
import unittest

from image_folder import ImageFolder

import ets_tutorial

TUTORIAL_DIR = dirname(ets_tutorial.__file__)
SAMPLE_IMG_DIR = join(TUTORIAL_DIR, "..", "sample_images")


class TestImageFolder(unittest.TestCase):
    def setUp(self):
        self.filenames = ["IMG-0311_xmas_2020.JPG", "owls.jpg"]
        self.img_folder = ImageFolder(directory=SAMPLE_IMG_DIR)

    def test_filters_images(self):
        self.assertEqual(
            {split(img.filepath)[1] for img in self.img_folder.images},
            set(self.filenames)
        )

    def test_create_metadata_df(self):
        df = self.img_folder.create_metadata_df()
        self.assertEqual(set(df.index), set(self.filenames))
        self.assertIn("ExifVersion", df)
        self.assertIn("ApertureValue", df)
