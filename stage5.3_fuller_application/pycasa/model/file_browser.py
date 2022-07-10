from os.path import expanduser
from traits.api import Directory, Event, HasStrictTraits


class FileBrowser(HasStrictTraits):
    root = Directory(expanduser("~"))

    #: Item last double-clicked on in the tree view
    requested_item = Event
