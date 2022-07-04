---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.7
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

<!-- #region slideshow={"slide_type": "slide"} -->
## Sharing scientific tools: script to desktop application

**Jonathan Rocher, Siddhant Wahal, Jason Chambless, Corran Webster, Prabhu Ramachandran**

**SciPy 2022**

<!-- #endregion -->


<!-- #region slideshow={"slide_type": "slide"} -->
## Motivation

- Some tasks are easier with a GUI
- Seeing a lot of information in one shot
- Easier for non-programmers
- Easier to share

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Why ETS?

- Mature
- Easy to use
- Design promotes reusable code
- Largely declarative UI
- PyQt/PySide and wxPython support

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## What is ETS?

- Enthought Tool Suite: https://docs.enthought.com/ets
- Open Source
- Packages
  - Traits: Python object attributes on steroids
  - TraitsUI: Easy GUI-building
  - PyFace: Low-level GUI components
  - Envisage: plug-in application framework
  - Chaco: interactive plotting library
  - Mayavi: 3D plotting
  - And others

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Layered package design

<center>
<img src="images/layers.png" height="90%" align="center"/>
</center>

<!-- #endregion -->


<!-- #region slideshow={"slide_type": "slide"} -->
## Sample screenshots


<!-- #endregion -->


<!-- #region slideshow={"slide_type": "slide"} -->
## Goals

- Start with simple Python script
  - Detect faces
  - Extract Image metadata

- Build a full-fledged desktop application
  - Easy to use UI
  - Learn a little MVC
  - Design application to scale
- Share the application with others

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Result

XXX Screenshot of initial application
XXX Screenshot of final application

<img src="src" height="90%" width="90%" align="center"/>

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Schedule

- Step 0: Python script
- Step 1: Using Traits.
- Step 2: Basic GUI using TraitsUI
- Step 3: PyFace application: tree navigator
- Step 4: More features
- Step 5: Installer


<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Basic Python script

- Uses: `PIL`, `skimage`, and `matplotlib`
- Detects faces in a given image
- Look inside ...

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Next steps

- Learn more about traits
- Build a clean model for our task with traits
- Learn why models are useful

<!-- #endregion -->
