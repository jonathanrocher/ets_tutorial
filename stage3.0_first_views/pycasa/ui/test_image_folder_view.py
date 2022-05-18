import unittest
from os.path import dirname, join

from traitsui.testing.api import UITester, IsVisible

import ets_tutorial
from pycasa.model.image_folder import ImageFolder
from image_folder_view import ImageFolderView

TUTORIAL_DIR = dirname(ets_tutorial.__file__)
SAMPLE_IMG_DIR = join(TUTORIAL_DIR, "..", "sample_images")


class TestImageFolderView(unittest.TestCase):
    def test_smoke(self):
        view = ImageFolderView(model=ImageFolder(directory=SAMPLE_IMG_DIR))
        tester = UITester()
        with tester.create_ui(view) as ui:
            df = tester.find_by_name(ui, "metadata_df")
            df.inspect(IsVisible())
