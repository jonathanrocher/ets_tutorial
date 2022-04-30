import matplotlib
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)
from pyface.qt import QtGui
from traitsui.api import BasicEditorFactory
from traitsui.qt4.editor import Editor

matplotlib.use('Qt5Agg')


class _MplFigureEditor(Editor):

    scrollable = True

    def init(self, parent):
        self.set_tooltip()
        self.control = self._create_mpl_canvas(parent)

    def update_editor(self):
        pass

    def _create_mpl_canvas(self, parent):
        control = QtGui.QWidget()
        canvas = FigureCanvas(figure=self.value)
        toolbar = NavigationToolbar(canvas, control)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(canvas)
        control.setLayout(layout)
        return control


class MplFigureEditor(BasicEditorFactory):
    klass = _MplFigureEditor
