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
            ImageFolder()

    def test_with_file(self):
        with self.assertRaises(ValueError):
            ImageFolder(path=__file__)

    def test_empty_folder(self):
        img = ImageFolder(path=HERE)
        data = img.to_dataframe()
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(len(data), 0)

    def test_real_folder(self):
        img = ImageFolder(path=SAMPLE_IMG_DIR)
        data = img.to_dataframe()
        self.assertEqual(len(data), 2)
        for key in ['ExifVersion', 'ExifImageWidth', 'ExifImageHeight']:
            self.assertIn(key, data.columns)
