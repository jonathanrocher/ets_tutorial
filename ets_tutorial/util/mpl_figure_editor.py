import matplotlib
from matplotlib.backends.backend_qt5agg import (
        FigureCanvasQTAgg, NavigationToolbar2QT
)
from matplotlib.backend_bases import FigureCanvasBase
from pyface.qt import QtGui
from traitsui.api import BasicEditorFactory
from traitsui.qt4.editor import Editor

matplotlib.use('Qt5Agg')


class _MplFigureEditor(Editor):

    scrollable = True

    def init(self, parent):
        """Create and initialize the underlying toolkit widget.
        """
        self.set_tooltip()
        self.control = QtGui.QWidget()
        self.control.setLayout(QtGui.QVBoxLayout())
        self._do_layout()

    def update_editor(self):
        """Updates the editor when the value changes externally to the editor.
        """
        self.clear_layout()
        self._do_layout()

    def _do_layout(self):
        """Creates sub-widgets and does layout.
        """
        canvas = FigureCanvasQTAgg(figure=self.value)
        # Allow the figure canvas to expand and shrink with the main widget.
        canvas.setSizePolicy(
            QtGui.QSizePolicy.Policy.Expanding,
            QtGui.QSizePolicy.Policy.Expanding,
        )
        toolbar = NavigationToolbar2QT(canvas, self.control)
        layout = self.control.layout()
        layout.addWidget(toolbar)
        layout.addWidget(canvas)


class MplFigureEditor(BasicEditorFactory):
    klass = _MplFigureEditor
