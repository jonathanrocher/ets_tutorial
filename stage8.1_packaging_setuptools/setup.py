""" Use this file to share this application with other developers:
1. `python setup.py develop` to code on it
2. `python setup.py bdist_egg` to build and share a binary egg
3. `python setup.py bdist_wheel` to build and share a binary wheel
"""

from os.path import join
from setuptools import setup, find_packages
from glob import glob

PKG_NAME = "pycasa"

# Application image files -----------------------------------------------------
ui_images_files = glob(join(PKG_NAME, "ui", "images", "*.*"))
ui_task_images_files = glob(join(PKG_NAME, "ui", "tasks", "images", "*.*"))
ui_app_images_files = glob(join(PKG_NAME, "app", "images", "*.png"))


setup(
    name=PKG_NAME,
    version="0.0.1",
    description='ETS based GUI application for image exploration and face '
                'detection',
    ext_modules=[],
    packages=find_packages(),
    data_files=[
        (".", ["README.md"]),
        (join(PKG_NAME, "ui", "images"), ui_images_files),
        (join(PKG_NAME, "ui", "tasks", "images"), ui_task_images_files),
        (join(PKG_NAME, "app", "images"), ui_app_images_files),
    ],
    entry_points={
        'console_scripts': [
            'pycasa = {}.app.main:main'.format(PKG_NAME),
        ],
    },
)
