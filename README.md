# Sharing your scientific tools: from a script to a desktop application
This repository contains a GUI building and packaging tutorial using the 
[Enthought Tool Suite](https://docs.enthought.com/ets/) accepted for the 
SciPy2022 conference.

## Tutorial summary

In this workshop, we will learn to embed scientific tools into a robust 
scientific application that can scale from a tiny UI to a large platform. As an 
example, attendees will build an image browser application (including 
face-detection capabilities), allowing users to search through their pictures, 
based on various criteria. We will start from a simple jupyter notebook and 
progressively turn it into a complete application using Matplotlib and several 
packages from the Enthought Tool Suite such as Traits, TraitsUI and Pyface. In 
the process, attendees will learn how to design clean, maintainable and 
scalable applications, and package them into an installer.

## Set up instructions

### Requirements

- Python 3.6+
- Pandas
- matplotlib
- traits
- traitsui
- scikits.image

### EDM users (recommended)
First, download and install EDM from https://www.enthought.com/edm/. Then, run 
the following in `Terminal`/`Powershell`/`Cmd Prompt`/... to create a dedicated 
Python environment and install all dependencies in it:
```commandline
edm env create ets_tutorial
edm shell -e ets_tutorial
edm install pandas matplotlib traits traitsui scikits.image
```

### Conda users

### pip users
Assuming a Python environment is created and activated on your machine, for 
example from https://www.python.org/, 
```commandline
pip install pandas matplotlib traits traitsui scikits-image
```

## Contributing
### Code structure

### Rules for contributing to the repository
Contributing to this repository requires:
1. to make a Pull Request
2. all code contributed must be pep8 compliant
3. all unit tests must pass
