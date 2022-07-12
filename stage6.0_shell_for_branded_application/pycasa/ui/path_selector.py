from traits.api import Bool, HasStrictTraits, File
from traitsui.api import Item, OKCancelButtons, View
from pycasa.ui.image_resources import app_icon


class PathSelector(HasStrictTraits):
    filepath = File

    scan_for_faces = Bool

    view = View(Item("filepath"),
                Item("scan_for_faces"),
                resizable=True,
                icon=app_icon,
                width=400, height=200,
                buttons=OKCancelButtons)
