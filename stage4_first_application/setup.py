from os.path import abspath, dirname, isfile, join
from setuptools import setup, find_packages
from glob import glob

HERE = dirname(abspath(__file__))

PKG_NAME = "pycasa"

info = {}
init_file = join(HERE, PKG_NAME, "__init__.py")
exec(open(init_file).read(), globals(), info)


setup(
    name=PKG_NAME,
    version=info["__version__"],
    description='Hello world in pyface task',
    ext_modules=[],
    packages=find_packages(),
    data_files=[
        (".", ["README.md"]),
    ],
    entry_points={
        'console_scripts': [
            'pycasa = {}.app.main:main'.format(PKG_NAME),
        ],
    },
)
