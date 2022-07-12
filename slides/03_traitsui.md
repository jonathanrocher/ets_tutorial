---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.0
  kernelspec:
    display_name: Python 3 (ipykernel)
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
