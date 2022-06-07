from traits.api import Property, observe
from pyface.api import warning
from pyface.tasks.api import Editor

from .image_folder_view import ImageFolderView


class ImageFolderEditor(Editor):
    name = Property

    tooltip = Property

    # -------------------------------------------------------------------------
    # 'Editor' interface methods
    # -------------------------------------------------------------------------

    def create(self, parent):
        """ Create and set the toolkit-specific control that represents the
        editor.
        """
        # Setting the kind and the parent allows for the ui to be embedded
        # within the parent UI
        view = ImageFolderView(model=self.obj)
        ui = view.edit_traits(kind="subpanel", parent=parent)

        # Grab the Qt widget to return to the editor area
        self.control = ui.control

    # -------------------------------------------------------------------------
    # Traits property methods
    # -------------------------------------------------------------------------

    def _get_name(self):
        return self.obj.path[:25]

    def _get_tooltip(self):
        return self.obj.path

    @observe("closing")
    def _veto_if_computing(self, event):
        event.new.veto = not self.obj.executor_idle
        if event.new.veto:
            warning(self.control, "Please wait for computation to finish!")
