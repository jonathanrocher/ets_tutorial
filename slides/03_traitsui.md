---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.7
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

<!-- #region slideshow={"slide_type": "slide"} -->
## Sharing scientific tools: script to desktop application

### TraitsUI

**Jonathan Rocher, Siddhant Wahal, Jason Chambless, Corran Webster, Prabhu Ramachandran**

**SciPy 2022**

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## TraitsUI: Easy GUI building

- Meant for traits
- Declarative UI
- Interoperates with Qt and wxPython
- Docs: https://docs.enthought.com/traitsui
- GH: https://github.com/enthought/traitsui

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Approach

- Just declare what needs to be done
- Do not need to write a lot of code
- Embed 2D plots with `matplotlib` or `chaco`
- Embed 3D plots with `mayavi`
- Build rich scientific dialogs

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Model-View-Controller (MVC) design pattern

- Model: manages data, state, and internal logic
- View: presents the model in a graphically interactive way
- Controller: manages information between view and model

<br/>

- For simple cases, View and Controller may be the same

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## MVC with traitsui

- Model: `HasStrictTraits` object
- View: `traitsui`,  `View` class
- Controller: `traitsui` `Handler` class

<!-- #endregion -->


<!-- #region slideshow={"slide_type": "slide"} -->
## Views

- A declarative specification for a GUI
- Made up of `Item` and `Group` objects

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Simple example

<!-- #endregion -->

```python
from traits.api import HasStrictTraits, Int, Str, Enum, Bool

class Person(HasStrictTraits):
    name = Str
    age = Int
    handedness = Enum('left', 'right')
    drinks = Bool(False)

```

```python
%gui qt
```

```python
p = Person(name='Worf')
p.edit_traits()
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Specifying a View


<!-- #endregion -->

```python
from traitsui.api import Item, View
view1 = View(
    Item(name='name', style='readonly'),
    Item(name='age'),
    Item(name='handedness'),
    Item(name='drinks', visible_when='age >= 18'),
)
```

```python
p.edit_traits(view=view1)
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Common attributes of `Item`

- `label`: UI label instead of the name
- `show_label`: Bool
- `tooltip`/`help`: Str
- `editor`: `ItemEditor` to use
- `style`: `{'simple', custom', 'text', 'readonly'}`
- `enabled_when`, `visible_when`, `defined_when`: Python expression
- `resizable`: bool

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Groups

- Handy for complex UIs
- Common attributes:
   - `columns`
   - `label`
   - `layout`: `{'normal', 'flow', 'split', 'tabbed'}`
   - `orientation`: ` {'vertical', 'horizontal'}`
   - `show_border`: bool
   - `enabled_when`, `visible_when`, `defined_when`: Python expression
- `HGroup`, `VGroup`, `HSplit`, `VSplit`, `Tabbed`: shortcuts

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## A simpler way

<!-- #endregion -->

```python
from traitsui.api import Group

class Person(HasStrictTraits):
    name = Str
    age = Int
    handedness = Enum('left', 'right')

    traits_view = View(
      Group(
        Item(name='name'),
        Item(name='age'),
        Item(name='handedness'),
        label='Person profile',
        show_border=True
      )
    )
```

```python
p = Person(name='Worf', age=20)
p.edit_traits()
```

```python

```

<!-- #region slideshow={"slide_type": "slide"} -->
## View attributes

- `dock`: `{'fixed', 'horizontal', 'vertical', 'tabbed'}`
- `height`/`width`: int
- `icon`/`image`
- `resizable`: bool
- `scrollable`: bool
- `title`: name of the window
- `buttons`
- `key_bindings`
- See docs for more: https://docs.enthought.com/traitsui/traitsui_user_manual/

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Simple example
<!-- #endregion -->

```python
from traitsui.api import CancelButton, OKButton

class Person(HasStrictTraits):
    name = Str
    age = Int
    likes_queso = Bool
    handedness = Enum('left', 'right')

    traits_view = View(
      Group(
        Item(name='name'),
        Item(name='age'),
        Item(name='handedness'),
        label='Person profile',
        show_border=True,
      ),
      buttons=[OKButton, CancelButton]
    )
```


```python
p = Person(name='Worf', age=20)
p.edit_traits()
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Specifying an editor

- Editors: encapsulate display instructions for a trait type
    - Hide GUI-toolkit code behind an abstraction layer
    - All standard traits has a predefined editor that is automatically
      displayed when the trait is displayed, unless overridden
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Examples

This code automatically uses `StrEditor`, the default for `Str` traits:
<!-- #endregion -->

```python
class Stringy(HasStrictTraits):
    characters = Str()

s = Stringy(characters='<b>Stringy characters</b>')
s.edit_traits(
    view=View(
        Item("characters")
    )
)
```
<!-- #region slideshow={"slide_type": "slide"} -->
This code uses an HTMLEditor:
<!-- #endregion -->
```python
from traitsui.api import HTMLEditor
s.edit_traits(
    view=View(
        Item("characters", editor=HTMLEditor())
    )
)
```

<!-- #region slideshow={"slide_type": "slide"} -->

## A few useful editors
- We illustrate the powerful `InstanceEditor` here
- Consider the following

<!-- #endregion -->

```python
from traits.api import Instance

class Person(HasStrictTraits):
    name = Str
    age = Int
    handedness = Enum('left', 'right')
    bff = Instance('Person')  # Notice the quotes.

    traits_view = View(
      Group(
        Item(name='name'),
        Item(name='age'),
        Item(name='handedness'),
        Item(name='bff', style='custom'),
        label='Person profile',
      )
    )
```

```python
frodo = Person(name='Frodo', age=30)
sam = Person(name='Sam', age=29, bff=frodo)
```
```python
sam.edit_traits()
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Discussion

- Note the embedding
- Implicitly uses an InstanceEditor
- Can configure the view it uses if needed

<!-- #endregion -->

```python
from traitsui.api import InstanceEditor

bff_view = View(Group(
        Item(name='name'),
        Item(name='age'),
        Item(name='handedness'),
        label='BFF',
        )
    )
```

```python slideshow={"slide_type": "slide"}
class Person(HasStrictTraits):
    name = Str
    age = Int
    handedness = Enum('left', 'right')
    bff = Instance('Person')

    traits_view = View(
      Group(
        Item(name='name'),
        Item(name='age'),
        Item(name='handedness'),
        Item(name='bff', style='custom', show_label=False,
             editor=InstanceEditor(view=bff_view)),
        label='Person profile',
      )
    )
```


```python
frodo = Person(name='Frodo', age=30)
sam = Person(name='Sam', age=29, bff=frodo)
```
```python
sam.edit_traits()
```

<!-- #region slideshow={"slide_type": "slide"} -->
- Another useful editor allows us to interface with `DataFrame`s
<!-- #endregion -->

```python
import pandas as pd
from traits.api import Event, Instance, Int 
from traitsui.api import ModelView
from traitsui.ui_editors.data_frame_editor import DataFrameEditor

class FramedData(HasStrictTraits):
    data = Instance(pd.DataFrame)

    def _data_default(self):
        return pd.DataFrame([
            {'A': 5, 'B': 0, 'C': 3, 'D': 3},
            {'A': 7, 'B': 9, 'C': 3, 'D': 5},
            {'A': 2, 'B': 4, 'C': 7, 'D': 6}
        ])

class FramedDataView(ModelView):
    model = Instance(FramedData)

    view = View(
        Item("model.data", editor=DataFrameEditor(editable=True))
    )

FramedDataView(model=FramedData()).edit_traits()
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Enter plotting
- Another useful editor is the `MplFigureEditor`
- Allows interacting with `matplotlib.figure.Figure` instances
- Included in the `ets_tutorial` package bundled in this repository
<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
Example:
<!-- #endregion -->
```python
from matplotlib.figure import Figure
import numpy as np
from skimage.data import chelsea
from traits.api import Array, HasStrictTraits, Instance
from traitsui.api import View, Item

from ets_tutorial.util.mpl_figure_editor import MplFigureEditor

class ImageViewer(HasStrictTraits):
    data = Array()

    figure = Instance(Figure)

    traits_view = View(
        Item("figure", editor=MplFigureEditor(), show_label=False)
    )

    def _data_default(self):
        return chelsea()

    def _figure_default(self):
        figure = Figure()
        axes = figure.add_subplot(111)
        axes.imshow(chelsea())
        return figure

ImageViewer().edit_traits()
```
<!-- #region slideshow={"slide_type": "slide"} -->
## The ModelView object:
- We want our science model to be free of UI code
- But it's still useful for models and views to respond to changes to one
  another -- `ModelView`s 
- `ModelView`s also monitor UI toolkit events like window creation,
  closing, user clicking OK or Cancel buttons
- Example:
<!-- #endregion -->

```python
from traits.api import observe
class Image(HasStrictTraits):
    data = Array()

    def _data_default(self):
        return chelsea()

class ImageView(ModelView):
    model = Instance(Image)

    figure = Instance(Figure)

    view = View(
        Item("figure", editor=MplFigureEditor(), show_label=False)
    )

    @observe("model.data")
    def build_mpl_figure(self, event):
        figure = Figure()
        axes = figure.add_subplot(111)
        axes.imshow(self.model.data)
        self.figure = figure

```

```python
image = Image()
image_view = ImageView(model=image)
image_view.edit_traits()
```

```python
from skimage.data import astronaut
image.data = astronaut()
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Exercise time!
- Starting from where we left off in Stage 2.1:
    - Create a `ModelView` for the `ImageFile` object that displays its filepath
      (readonly), and the image array in a matplotlib figure
        - Ensure figure is updated if the `filepath` attribute of `ImageFile` is
          modified
    - Create a `ModelView` for the `ImageFolder` object that displays the directory
      (readonly) and the `DataFrame`
    - Bonus points:
        - What mechanism would we use to hide the `DataFrame` if the directory doesn't have any images
          and instead show a helpful message? 
        - Hint: keyword arguments for `Item`
<!-- #endregion -->
<!-- #region slideshow={"slide_type": "slide"} -->
## Solution

<!-- #endregion -->
## Toolkit selection

- TraitsUI supports: Qt or wxPython
- Can set the toolkit in a program
    - 'qt' or 'qt4'
    - 'wx'
    - 'null'
- Or with the `ETS_TOOLKIT` environment variable

```
export ETS_TOOLKIT=qt
```

<!-- #endregion -->

```python
from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt'
```


<!-- #region slideshow={"slide_type": "slide"} -->
## Other documentation

- Interesting tutorial: https://docs.enthought.com/traitsui/tutorials

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Exercise:



<!-- #endregion -->
