from os.path import dirname, join
from unittest import TestCase

import numpy as np

from pycasa.model.image_file import ImageFile

import ets_tutorial

TUTORIAL_DIR = dirname(ets_tutorial.__file__)

SAMPLE_IMG_DIR = join(TUTORIAL_DIR, "..", "sample_images")

SAMPLE_IMG1 = join(SAMPLE_IMG_DIR, "IMG-0311_xmas_2020.JPG")


class TestImageFile(TestCase):
    def test_no_image_file(self):
        img = ImageFile()
        self.assertEqual(img.metadata, {})
        self.assertIsInstance(img.data, np.ndarray)
        self.assertEqual(img.data.shape, (0,))

    def test_image_metadata(self):
        img = ImageFile(filepath=SAMPLE_IMG1)
        self.assertNotEqual(img.metadata, {})
        for key in ['ExifVersion', 'ExifImageWidth', 'ExifImageHeight']:
            self.assertIn(key, img.metadata.keys())
        expected_shape = (img.metadata['ExifImageHeight'],
                          img.metadata['ExifImageWidth'], 3)
        self.assertEqual(img.data.shape, expected_shape)
