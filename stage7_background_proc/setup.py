from setuptools import setup, find_packages


setup(
    name="pycasa",
    version="0.0.1",
    description='ETS based GUI application for image exploration and face '
                'detection',
    ext_modules=[],
    packages=find_packages(),
    data_files=[
        (".", ["README.md"]),
    ],
)
