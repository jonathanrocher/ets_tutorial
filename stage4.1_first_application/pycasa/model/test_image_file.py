from os.path import dirname, join
from unittest import TestCase

import numpy as np
from numpy.testing import assert_array_equal

from pycasa.model.image_file import ImageFile

import ets_tutorial

TUTORIAL_DIR = dirname(ets_tutorial.__file__)

SAMPLE_IMG_DIR = join(TUTORIAL_DIR, "..", "sample_images")

SAMPLE_IMG1 = join(SAMPLE_IMG_DIR, "IMG-0311_xmas_2020.JPG")


class TestImageFile(TestCase):
    def test_no_image_file(self):
        img = ImageFile()
        self.assertEqual(img.metadata, {})
        data = img.to_array()
        self.assertIsInstance(data, np.ndarray)
        self.assertEqual(data.shape, (0,))

    def test_image_metadata(self):
        img = ImageFile(filepath=SAMPLE_IMG1)
        self.assertNotEqual(img.metadata, {})
        data = img.to_array()
        self.assertEqual(data.shape, (768, 1024, 3))
