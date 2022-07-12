# Distributable Applications

What you have now is a working application on your computer.  The problem that
you face is how to distribute this application to your colleagues so that they
can also use your work.

If they are comfortable with Python and tools like `git` and `pip` you may be
able to just give a list of commands to download the code, install an
environment and run the application.

But a major advantage of GUI applications is that they are intended to be
accessible by users who are not as knowledgeable about coding.  For this reason
it's desirable to be able to provide them with simple tools which either
install an application and its environment, or which look and behave like
ordinary applications on their operating system.

A number of solutions are available for this sort of operation, including
some commercial solutions from Anaconda and Enthought.  Tools which you might
consider using include:

- [PyOxidizer](https://pyoxidizer.readthedocs.io/en/stable/), which
  is comprehensive but complex and written in Rust.
- [Py2App](https://py2app.readthedocs.io/en/latest/), which is aimed at
  MacOS applications specifically
- [BeeWare](https://beeware.org/)'s [Briefcase](https://briefcase.readthedocs.io/en/latest/)
  which is new and somewhat incomplete, but aims to be deployable on all
  platforms including iOS and Android.

In this section we will use [PyInstaller](https://pyinstaller.org/en/stable/)
because it works on all major desktop platforms and is fairly mature.

## PyInstaller Basics

At its simplest, using PyInstaller is just a matter of installing pyinstaller
with `pip`:
```
pip install -U pyinstaller
```
changing to the directory of your program, and running
```
pysinstaller my_script.py
```
PyInstaller will create an application file (.exe if on Windows, executable if 
on POSIX systems) and place it in a `dist/` folder
next to your application.  You can run this executable as a command from the
command-line, or by finding the icon in your OS file browser and opening it
that way.

PyInstaller tries to analyse your code and only include modules that it knows
that your application will use, to make the resulting application file as small
as possible.  This is magical, and as with all magical things there are a lot
of options and things to tweak to make sure that the magic works.

### OS and Environment

PyInstaller must be run in a working Python environment containing your
application code and dependencies.  This unfortunately means that you can't
build for a different OS or CPU architecture; indeed in some cases you may
not be able to build an application for an earlier version of the OS you use.
If you have users on many different systems, you may need to have a collection
of virtual machines (or even physical machines) configured appropriately for
performing the builds.

PyInstaller has some additional options for Windows and MacOS to help support
the particular idiosyncracies of each.

### Single Directory vs. Single File

PyInstaller gives you a choice between building an application as an
executable plus auxiliary files as a single directory, or as a single
executable file.  While the single file is nicer, getting it to work can be
more difficult.  For simplicity, we'll use the default single directory
approach for this tutorial.  You can use zip or a similar utility to bundle
this for easier distribution: most users are comfortable with unzipping
a bundle that they have been given before running it.

### Windowed vs. Console

On Windows and MacOS, PyInstaller needs to be told whether the application
needs a text-based terminal window available for input or displaying things
to the user (even if it opens a GUI) or a purely windowed application.
These are controlled by the `--console` and `--windowed` command-line options.

## Common Problems

Because Python is a very dynamic language, it can be difficult or impossible
for PyInstaller to work out exactly what it needs to include in the
application bundle.

### Data Files

It's particularly common for GUI applications to have additional files that
they need to operate.  The most common are image files for icons and logos,
but can include things like HTML files containing documentation, data files,
or trained machine learning model files.

PyInstaller has no way of knowing if any non-Python files are needed, and so
it needs to be told.  This includes any such files needed by libraries that
your application uses.

### Dynamic Imports

Python is a very dynamic language and can import modules by methods other than
the standard `import` statement.  This is commonly used by libraries that need
to decide what code to use based on the environment that they find themselves
in.  For example libraries like Pyface, TraitsUI and Matplotlib will look at
environment variables and/or try importing GUI library dependencies like Qt to
determine which one they should use.  This is very convenient for people who
are writing and distributing scripts, but it makes it difficult for
PyInstaller to perform its import analysis.

### Entry Points

Related to dynamic importing, many Python libraries use "entry points" to
advertise capabilities to other code.  You most likely have seen this in a
package setup file where you may have seen or used lines like:
```
entry_points={
    'console_scripts': [
        'my_script = my_package.my_script:main',
    ],
}
```
which advertise that the package has a command-line script `my_script` that
can be run from the `main` function in `my_package.my_script` and Python tools
will ensure that these are made available when you install them into a Python
environment. However they are a much more general mechanism which can be used
for building general "plugin" capabilities for Python libraries.

Amir Rachum has a [good blog post](https://amir.rachum.com/blog/2017/07/28/python-entry-points/)
from a few years back that explains why you might use or care about entry
points.

Entry points used to be part of the `setuptools` library, but since Python 3.8
they are now available via the
[imporlib.metadata](https://docs.python.org/3/library/importlib.metadata.html)
standard library module.

Again, the problem for PyInstaller is that it can't detect use of code that
comes from entry points, but in addition PyInstaller doesn't expose the entry
points for libraries that it wraps by default.  So if you include code that
expects to load capabilities via this mechanism they will fail even if the
required code is packaged unless you tell PyInstaller about the entry points.

## Spec Files and Hook Files

While many of these problems can be corrected via the use of appropriate
command-line options, once you have any level of complexity you will want to
be putting these into something more repeatable and editable.  PyInstaller
has two mechanisms for this:

- `.spec` files, which are Python files which hold the build instructions for
  an application as a whole
- `hook-` files, which are Python files which hold information about a
  particular package and how it should work with PyInstaller

### Spec Files

When you run `pysinstaller my_script.py`, PyInstaller first creates a
corresponding `my_script.spec` file using the command-line options passed in
and runs the code in that file.  You can also create a `.spec` file using the
`pyi-makespec` commands.  Once you have a `.spec` file, you can instead run
```
pyinstaller my_spec.spec
```
and it will use the options specified there.  If you used the `.spec` file
created automatically, it is probably a good idea to rename it so it doesn't
accidentally get overwritten if you run `pysinstaller my_script.py` again.

The contents of the file might look something like this (depending on the
options used to generate it):
```
block_cipher = None
a = Analysis(
    ['my_script.py'],
    pathex=['/Developer/PItests/minimal'],
    binaries=None,
    datas=None,
    hiddenimports=[],
    hookspath=None,
    runtime_hooks=None,
    excludes=None,
    cipher=block_cipher,
)
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
)
exe = EXE(pyz,... )
coll = COLLECT(...)
```
Most of this you can ignore for simple usage, but there are a few things that
you can use to fix the problems listed above:

- adding data files: the `datas` argument to the `Analysis` function expects
  a list of `(source, dest)` tuples that tell PyInstaller to include the
  file(s) at the `source` path in your code in the directory specified by
  `dest` in your application.  This understands basic "glob"-style wildcards.

  Example: `datas=[("docs/build/html", "documentation"), ("*.txt", ".")]`
  would:
  
  - take the `html` folder as typically built by Sphinx and add it into your
    application distribution as a subdirectory called "documentation".

  - take all files with the `.txt` suffix in the main script directory and add
    them to the top-level application directory alongside the executable.

- adding dynamic imports: the `hiddenimports` argument expects a list of
  additional module names to be added to the modules packaged into the
  application.

  Example: `hiddenimports=["my_package.editors.qt"]` would add the
  `my_package.editors.qt` module and everything that imports to the packaged
  set of modules.

- adding binary dependencies: PyInstaller is usually fairly good about
  detecting and adding Python C extensions, but if it fails to correctly find
  the extension (or its dependencies) you can use the `binaries` argument
  to supply a list of DLLs or folders containing DLLs (or the OS-specific
  equivalents) that you want added to the application.  These are specified
  as `(source, dest)` pairs as for data files.

- specifying a list of additional places to look for hook files with the
  `hookspath` argument.

Manually listing all of these files can be tedious, and so there are several
utility methods that are available to help populate these lists.

### Hook files

Hook files are similar to `.spec` files, but are instead Python files that
have a name in the pattern `hook-package.name.py` and which are expected to
provide particular information that `package.name` needs to correctly work in
a PyInstaller application.  The idea is that these can be defined once for a
given library and then shared by all the applications which use this library.

PyInstaller comes with built-in support for some common libraries which
require additional support, such as Matplotlib: you should not need to do
any additional work to build an application which used matplotlib in a
standard way, for example. Additionally the
[PyInstaller hooks repository](https://github.com/pyinstaller/pyinstaller-hooks-contrib)
has additional community-contributed hook files for popular packages, which
are `pip`-installable as `pyinstaller-hooks-contrib`.

However, if you are the author of, or want to use, a library that needs
additional support, then writing a hookfile may be easier than adding things
to a `.spec` file.

Hook files are expected to populate certain global variables in the module
with appropriate values:

- `datas`: a list of data files in `(source, dest)` form as described above.
  
- `hiddenimports`: a list of additional modules to include in the package.

- `binaries`: a list of binary files to include in `(source, dest)` form as
  described above.

### `PyInstaller.utils.hooks`

Specifying all of the extra files to include can be tedious and error-prone,
particularly as a library or application change over time.  PyInstaller has
some utility files which make it easier to write `.spec` and hook files.  Most
of these can be found in the `PyInstaller.utils.hooks` module, which can be
imported in a `.spec` or hook file as you would for a normal Python file.

- `collect_data_files`: In the simplest form, you pass this the name of a
  Python package and it will generate a list of `(source, dest)` paths for all
  non-Python files in the package, suitable for inclusion in a `datas` list.

- `collect_submodules`: This will create a list of all submodules of a given
  module in a form suitable for use with the `hiddenimports` list.  Submodules
  will be included whether or not they are imported.

- `collect_entry_point`: This inspects the given entry point and returns a
  list of `datas` and a list of `hiddenimports` that are needed to support the
  use of that entry point.

- `collect_dynamic_libs`: This finds all DLLs included in a given package.

## Grace Notes

By default on Windows and Mac OS the application's desktop icon will be the
default PyInstaller icon.  While this is fine in development, it is useful for
users to have a distinct icon on the desktop.  This can be provided using the
`--icon` command-line option.  It can also be specified in a `.spec` file.

For MacOS in particular you can include additional information for the
`.plist` file inside a Mac app bundle.

## Distributing ETS Applications

The ETS libraries require the use of a number of these tools to build
applications with PyInstaller.

- many of the libraries have data files,

- dynamic importing is used, particularly to choose between Qt and Wx backend
  implementations,

- availability of toolkits and other functionality are advertised via entry
  points.

The easiest way to overcome these is to simply use the `collect_...` methods
to gather everything from the top-level package.  For example, the following
code will gather everything that is needed for TraitsUI:
```
from PyInstaller.utils.hooks import (
    collect_data_files, collect_entry_point, collect_submodules
)

data, hiddenimports = collect_entry_point("traitsui.toolkits")
data += collect_data_files("traitsui")
hiddenimports += collect_submodules("traitsui")
```

This will include code that your application does not use, but it is unlikely
that the extra size of the resulting application from this will pose a
problem.

This directory includes hook files suitable for use with the core ETS
libraries.
