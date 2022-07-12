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
## Step1: Using Traits

**Jonathan Rocher, Siddhant Wahal, Jason Chambless, Prabhu Ramachandran**

**SciPy 2022**

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Introduction to Traits

- **trait**: Python object attribute with additional characteristics
    - Typed attributes
    - Reactive
    - Observable
    - Cleaner code
    - Easy UI

<br/>

- https://docs.enthought.com/traits/
- https://github.com/enthought/traits/

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Why all this?

- No pain, no gain! (Only a little pain, we promise!)

- Small change to thinking yields big benefits

- Do not mix GUI code with core model

- Build a clean model first

  - Easier to understand/maintain
  - Separation of concerns
  - Easier to test
  - Generally better reuse

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Trait features

- Initialization: default value
- Validation: strongly typed
- Deferral/Delegation: value delegation
- Notification: events
- Visualization: MVC, automatic GUI!

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## An example

<!-- #endregion -->

```python
from traits.api import Delegate, HasStrictTraits, Instance, Int, Str, observe

class Parent(HasStrictTraits):
    # INITIALIZATION: 'last_name' initialized to ''
    last_name = Str('')

```

```python
class Child(HasStrictTraits):
    age = Int
    # VALIDATION: 'father' must be Parent instance
    father = Instance(Parent)
    # DELEGATION: 'last_name' delegated to father's
    last_name = Delegate('father')
    # NOTIFICATION: Method called when 'age' changes
    def _age_changed(self, old, new):
        print('Age changed from %s to %s ' % (old, new))

```

<!-- #region slideshow={"slide_type": "slide"} -->
## Using this

<!-- #endregion -->

```python
joe = Parent()
joe.last_name = 'Johnson'
moe = Child()
moe.father = joe
```

```python
# Delegation
moe.last_name
```

```python
# Notification
moe.age = 10
```

```python
# Validation
moe.age = '1'
```

```python
# Visualization
moe.configure_traits()
```

- Live editing!

```python
%gui qt
```

```python
moe.edit_traits()
```

```python
moe.age = 21
```

<!-- #region slideshow={"slide_type": "slide"} -->
## What if you want to override `__init__`?

<!-- #endregion -->

```python
class Child(HasStrictTraits):
    age = Int
    father = Instance(Parent)
    last_name = Delegate('father')

    def __init__(self, **traits):
        super(HasStrictTraits, self).__init__(**traits)

    def _age_changed(self, old, new):
        print('Age changed from %s to %s ' % (old, new))
```


<!-- #region slideshow={"slide_type": "slide"} -->
## Predefined trait types

- Standard: `Bool, Complex, Int, Float, Str, Tuple, List, Dict`
- Constrained: `Range, Regex, Expression, ReadOnly`
- Special: `Date, Either/Union, Enum, Array, File, Color, Font, Button`
- Generic: `Instance, Any, Callable`
- Custom traits: 2D/3D plots etc.

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## `HasStrictTraits` vs. `HasStrictTraits`

- Better to use `HasStrictTraits`
- Will catch errors when you mistype or misspell an attribute
- Will not allow setting any attribute not already declared


<!-- #endregion -->


<!-- #region slideshow={"slide_type": "slide"} -->
## Notification example

<!-- #endregion -->

```python
class Parent(HasStrictTraits):
    last_name = Str('')


class Child(HasStrictTraits):
    age = Int
    father = Instance(Parent)

    def _age_changed(self, old, new):
        print('Age changed from %s to %s ' % (old, new))

    @observe('father.last_name')
    def _dad_name_updated(self, event):
        print(Father name changed to', self.father.last_name)

```

```python
dad = Parent(last_name='Zubizaretta')
c = Child(father=Parent)
```

```python
dad.last_name = 'Valderrama'
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Trait change notification

- Static: `def _<trait_name>_changed()`
- Decorator: `@observe('extended.trait.name')`

- See documentation: https://docs.enthought.com/traits/traits_user_manual/notification.html

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Exercise

- Modify the first example to produce the above example
- Add a `first_name` trait
- Add a `Bool` trait to specify if person is alive
- Add an `Enum` for the gender of the child


<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Solution

<!-- #endregion -->

```python
from traits.api import Bool, Enum

class Parent(HasStrictTraits):
    last_name = Str('')


class Child(HasStrictTraits):
    age = Int
    father = Instance(Parent)
    first_name = Str('')
    likes_queso = Bool(True)
    handedness = Enum('right', 'left')

    def _age_changed(self, old, new):
        print('Age changed from %s to %s ' % (old, new))

    @observe('father.last_name')
    def _dad_name_updated(self, event):
        print('Dad name', self.father.last_name)

```

```python
p = Parent(last_name='Ray')
c = Child(age=21, father=p, first_name='Romano', handedness='right')
```


<!-- #region slideshow={"slide_type": "slide"} -->
## Trait change event

- Recall this
<!-- #endregion -->

```python
    @observe('father.last_name')
    def _dad_name_updated(self, event):
        print('Dad name', self.father.last_name)
```

- `event` is a `TraitChangeEvent` instance


```python slideshow={"slide_type": "slide"}
class Child(HasStrictTraits):
    age = Int
    father = Instance(Parent)
    first_name = Str('')
    likes_queso = Bool(True)
    handedness = Enum('right', 'left')

    def _age_changed(self, old, new):
        print('Age changed from %s to %s ' % (old, new))

    @observe('father.last_name')
    def _dad_name_updated(self, event):
        print(event.object, event.name, event.old, event.new)
        print('Dad name', self.father.last_name)

```

```python
p = Parent(last_name='Ray')
c = Child(age=21, father=p, first_name='Romano', handedness='right')
```

```python
p.last_name = 'Ahmed'
```



<!-- #region slideshow={"slide_type": "slide"} -->
## Container traits

- `List`, `Dict` and `Set`

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Trait Lists


<!-- #endregion -->

```python
from traits.api import List

class Bowl(HasStrictTraits):
    fruits = List(Str)

    @observe("fruits")
    def _fruits_list_updated(self, event):
        print("fruits list updated", type(event))
        print(event.old, event.new)

    @observe("fruits.items")
    def _fruits_updated(self, event):
        print("Fruits items changed", type(event))
        print(event.added, event.index, event.removed)

```

```python
b = Bowl()
b.fruits = ['apple']
b.fruits.append('mango')
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Other Trait Events

- `List` trait changes: `ListChangeEvent`
- `Dict` trait changes: `DictChangeEvent`
- `Set` trait changes: `SetChangeEvent`

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Some more useful traits

- `File`, `Directory` and `Dict`
- Useful for our application

<!-- #endregion -->

```python
from traits.api import Dict, Directory, File

class Folder(HasStrictTraits):
    root = Directory
    files = List(File)
    sizes = Dict
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Walk through

- Here the dictionary can have any keys or values
- Can use the `key_trait` and `value_trait` to specify them

<!-- #endregion -->


```python
class Folder(HasStrictTraits):
    root = Directory
    files = List(File)
    sizes = Dict(key_trait=Str, value_trait=Dict(Str, Int))
```

```python
f = Folder(root='/tmp')
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Exercise

Modify the above example so when you set `root`, it finds all the files in
that directory and the file sizes and sets the appropriate traits.

Hint: Use `os.listdir` and `os.path.getsize`

<!-- #endregion -->

```python
# Solution
```



<!-- #region slideshow={"slide_type": "slide"} -->
## Property traits

- What if you have a quantity that is computed?
- Use `Property` traits here
- Use the `observe=` kwarg
- Use `@cached_property` to cache output
- Use the `_get_propname` and `_set_propname` (optional)

<!-- #endregion -->

```python
from math import pi
from traits.api import Range, Float, Property, cached_property

class Circle(HasTraits):
    radius = Range(0.0, 1000.0)
    area = Property(Float, observe='radius')

    @cached_property
    def _get_area(self):
        print("computing area")
        return pi*self.radius**2
```

```python
c = Circle(radius=2)
c.area
```

```python
c.area
```

<!-- #region slideshow={"slide_type": "slide"} -->
## `Array` traits

- Can handle numpy arrays of arbitrary shape
- Can specify dtype, shape, and casting options using kwargs
- Warning: cannot "listen" to changes inside the array
- Simple example

<!-- #endregion -->

```python
import numpy as np
from traits.api import Array, Range, observe

class Beats(HasTraits):
    f1 = Range(1.0, 200.0, value=100)
    f2 = Range(low=1.0, high=200.0, value=104)
    signal = Array(dtype=float, shape=(None,))

    @observe('f1, f2')
    def update(self, event=None):
        t = np.linspace(0, 1, 500)
        pi = np.pi
        self.signal = np.sin(2*pi*self.f1*t) + np.sin(2*pi*self.f2*t)
```

```python
b = Beats()
b.f2 = 103
```
<!-- #region slideshow={"slide_type": "slide"} -->
## Setting default values

- For simple cases, use the default of the trait
- For more complex cases use a special method
- A simple example

<!-- #endregion -->

```python
import datetime

from traits.api import HasStrictTraits, Date, Range

class Thing(HasStrictTraits):
    date = Date()
    age = Int(12)

    def _date_default(self):
        print('default')
        return datetime.datetime.today()
```


```python
t = Thing()
```

```python
type(c.age)
```

<!-- #region slideshow={"slide_type": "slide"} -->
## `Event` traits

- Holds no value but can be set and be listened to

<!-- #endregion -->

```python
from traits.api import HasTraits

class DataFile(HasStrictTraits):
    file = File
    data_changed = Event


class DataReader(HasStrictTraits):
    file = DataFile
    content = Str

    @observe("file.data_changed")
    def file_data_changed(self, event):
        print("File data changed")

```

```python
f = DataFile(file='/tmp/junk.dat')
r = DataReader(file=f)
```
```python
f.data_changed = True
```


<!-- #region slideshow={"slide_type": "slide"} -->
## Exercise time!

- Take the simple example without traits
- Create a simple Traits model for it
- *Do not do any plotting in the model!*

<!-- #endregion -->
