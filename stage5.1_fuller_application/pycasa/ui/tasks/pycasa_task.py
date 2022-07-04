# General imports
from os.path import splitext

# ETS imports
from traits.api import Instance
from pyface.tasks.api import PaneItem, SplitEditorAreaPane, Task, TaskLayout

# Local imports
from .pycasa_browser_pane import PycasaBrowserPane
from ...model.image_folder import ImageFolder
from ..image_folder_editor import ImageFolderEditor
from ...model.image_file import ImageFile, SUPPORTED_FORMATS
from ..image_file_editor import ImageFileEditor


class PycasaTask(Task):
    # 'Task' traits -----------------------------------------------------------

    #: The unique id of the task.
    id = "pycasa.pycasa_task"

    #: The human-readable name of the task.
    name = "Pycasa"

    central_pane = Instance(SplitEditorAreaPane)

    # Task interface ----------------------------------------------------------

    def create_central_pane(self):
        """ Create the central pane: the script editor.
        """
        # Let's keep a handle on it so we can invoke it later to open objects
        # in it:
        self.central_pane = SplitEditorAreaPane()
        return self.central_pane

    def create_dock_panes(self):
        return [PycasaBrowserPane()]

    def _default_layout_default(self):
        """ Control where to place each (visible) dock panes.
        """
        return TaskLayout(
            left=PaneItem('pycasa.file_browser_pane', width=300)
        )

    # Task interface ----------------------------------------------------------

    def open_in_central_pane(self, filepath):
        file_ext = splitext(filepath)[1].lower()
        if file_ext in SUPPORTED_FORMATS:
            obj = ImageFile(filepath=filepath)
            self.central_pane.edit(obj, factory=ImageFileEditor)
        elif file_ext == "":
            obj = ImageFolder(directory=filepath)
            self.central_pane.edit(obj, factory=ImageFolderEditor)
        else:
            print("Unsupported file format: {}".format(file_ext))
