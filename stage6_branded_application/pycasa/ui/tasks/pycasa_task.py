# General imports
from os.path import splitext

# ETS imports
from traits.api import Instance
from pyface.api import error, ImageResource
from pyface.action.api import StatusBarManager
from pyface.tasks.api import PaneItem, SplitEditorAreaPane, Task, TaskLayout
from pyface.tasks.action.api import DockPaneToggleGroup, SGroup, SMenu, \
    SMenuBar, SToolBar, TaskAction, TaskWindowAction

from traits.api import HasStrictTraits, File
from traitsui.api import Item, OKCancelButtons, View
from pycasa.ui.image_resources import app_icon

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
            obj = ImageFolder(path=filepath)
            self.central_pane.edit(obj, factory=ImageFolderEditor)
        else:
            print("Unsupported file format: {}".format(file_ext))

    # Menu action methods -----------------------------------------------------

    def request_open_new_path(self):
        selector = PathSelector()
        ui = selector.edit_traits(kind="livemodal")
        if ui.result:
            self.open_in_central_pane(selector.filepath)

    def scan_current_path(self):
        if self.central_pane.active_editor is None:
            msg = "No active tab/path. You must open a path before you can " \
                  "scan it for faces"
            error(None, msg)
            return

        active_editor = self.central_pane.active_editor
        model = active_editor.obj

        self.status_bar.messages = ["Scanning..."]

        if isinstance(model, ImageFolder):
            model.compute_num_faces()
        else:
            model.detect_faces()

        self.status_bar.messages = ["Scanning complete."]

    # Initialization methods --------------------------------------------------

    def _tool_bars_default(self):
        # No accelerators here: they are added to menu entries
        # Note: Image resources are looked for in an images folder next to the
        # module invoking the resource.
        tool_bars = [
            SToolBar(
                TaskAction(name='Open...',
                           method='request_open_new_path',
                           image=ImageResource('document-open')),
                TaskAction(name='Scan',
                           method='scan_current_path',
                           image=ImageResource('zoom-draw')),
                image_size=(24, 24), show_tool_names=False, id='ToolsBar',
                name='ToolsBar'
            ),
        ]
        return tool_bars

    def _menu_bar_default(self):
        menu_bar = SMenuBar(
            SMenu(
                SGroup(
                    TaskAction(name='Open...',
                               accelerator='Ctrl+O',
                               method='request_open_new_path',
                               image=ImageResource('document-open')),
                    id='OpenGroup', name='OpenGroup',
                ),
                SGroup(
                    TaskWindowAction(
                        name='Close',
                        accelerator='Ctrl+W',
                        method='close',
                    ),
                    id='CloseGroup', name='CloseGroup',
                ),
                id='File', name='&File'),
            SMenu(DockPaneToggleGroup(),
                  id='View', name='&View'),
            SMenu(
                SGroup(
                    TaskAction(name='Scan',
                               accelerator='Ctrl+R',
                               method='scan_current_path',
                               image=ImageResource('zoom-draw')),
                    id='ScanGroup', name='ScanGroup'
                ),
                id='Tools', name='&Tools',
            ),
            SMenu(
                id='Help', name='&Help'
            )
        )
        return menu_bar

    def _status_bar_default(self):
        return StatusBarManager(messages=["Welcome to Pycasa"])


class PathSelector(HasStrictTraits):
    filepath = File

    view = View(Item("filepath"),
                resizable=True,
                icon=app_icon,
                width=400, height=200,
                buttons=OKCancelButtons)
