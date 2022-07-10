from os.path import dirname, join
from unittest import TestCase

import pandas as pd

from pycasa.model.image_folder import ImageFolder

import ets_tutorial

TUTORIAL_DIR = dirname(ets_tutorial.__file__)

SAMPLE_IMG_DIR = join(TUTORIAL_DIR, "..", "sample_images")

HERE = dirname(__file__)


class TestImageFolder(TestCase):
    def test_no_folder(self):
        with self.assertRaises(ValueError):
            ImageFolder(directory="path/to/nonexistent/dir")

    def test_with_file(self):
        with self.assertRaises(ValueError):
            ImageFolder(directory=__file__)

    def test_empty_folder(self):
        img_folder = ImageFolder(directory=HERE)
        self.assertIsInstance(img_folder.data, pd.DataFrame)
        self.assertEqual(len(img_folder.data), 0)

    def test_real_folder(self):
        img_folder = ImageFolder(directory=SAMPLE_IMG_DIR)
        self.assertEqual(len(img_folder.data), 2)
        for key in ['ExifVersion', 'ExifImageWidth', 'ExifImageHeight']:
            self.assertIn(key, img_folder.data.columns)
