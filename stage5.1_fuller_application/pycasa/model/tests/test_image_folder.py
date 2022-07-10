from os.path import dirname, join, split
import unittest

from pycasa.model.image_folder import FILENAME_COL, ImageFolder

import ets_tutorial

TUTORIAL_DIR = dirname(ets_tutorial.__file__)
SAMPLE_IMG_DIR = join(TUTORIAL_DIR, "..", "sample_images")


class TestImageFolder(unittest.TestCase):
    def setUp(self):
        self.filenames = ["IMG-0311_xmas_2020.JPG", "20210802_191429.jpg"]
        self.img_folder = ImageFolder(directory=SAMPLE_IMG_DIR)

    def test_with_file(self):
        with self.assertRaises(ValueError):
            ImageFolder(directory=__file__)

    def test_filters_images(self):
        self.assertEqual(
            {split(img.filepath)[1] for img in self.img_folder.images},
            set(self.filenames)
        )

    def test_data_correct(self):
        df = self.img_folder.data
        self.assertEqual(set(df[FILENAME_COL]), set(self.filenames))
        self.assertIn("ExifVersion", df)
        self.assertIn("ApertureValue", df)
