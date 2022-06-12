from os.path import dirname, join
from unittest import TestCase

import numpy as np
import pandas as pd

from pyface.toolkit import toolkit_object
from traits_futures.api import TraitsExecutor

from pycasa.model.image_folder import ImageFolder, NUM_FACE_COL

import ets_tutorial

TUTORIAL_DIR = dirname(ets_tutorial.__file__)

SAMPLE_IMG_DIR = join(TUTORIAL_DIR, "..", "sample_images")

HERE = dirname(__file__)

# Maximum timeout for blocking calls.
SAFETY_TIMEOUT = 300

# GuiTestAssistant is only available for Qt.
GuiTestAssistant = toolkit_object("util.gui_test_assistant:GuiTestAssistant")


class TestImageFolder(GuiTestAssistant, TestCase):
    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.traits_executor = TraitsExecutor()

    def tearDown(self):
        self.traits_executor.shutdown(timeout=SAFETY_TIMEOUT)
        GuiTestAssistant.tearDown(self)

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

    def test_compute_num_faces_background(self):
        image_folder = ImageFolder(
            path=SAMPLE_IMG_DIR,
            traits_executor=self.traits_executor
        )
        image_folder.compute_num_faces_background()
        self.assertEventuallyTrueInGui(
            lambda: image_folder.future.done, timeout=SAFETY_TIMEOUT
        )
        self.assertEqual(
            image_folder.data[NUM_FACE_COL].to_list(), [5.0, 3.0]
        )
