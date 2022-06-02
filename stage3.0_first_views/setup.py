from os.path import abspath, dirname, join
from setuptools import setup, find_packages

HERE = dirname(abspath(__file__))

PKG_NAME = "pycasa"

info = {}
init_file = join(HERE, PKG_NAME, "__init__.py")

with open(init_file) as fp:
    exec(fp.read(), globals(), info)

setup(
    name=PKG_NAME,
    version=info["__version__"],
    description='Introduction to TraitsUI views',
    ext_modules=[],
    packages=find_packages(),
    data_files=[
        (".", ["README.md"]),
    ],
)
