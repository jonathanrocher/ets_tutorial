# General imports
from matplotlib.figure import Figure
from matplotlib.pyplot import imshow, figure
import imageio

# ETS imports
from traits.api import Instance, observe
from traitsui.api import Item, ModelView, View

# Local imports
from ets_tutorial.util.mpl_figure_editor import MplFigureEditor
from ..model.image_file import ImageFile


class ImageFileView(ModelView):
    """ ModelView for an image file object.
    """
    model = Instance(ImageFile)

    figure = Instance(Figure)

    view = View(
        Item("model.filepath", style="readonly", show_label=False),
        Item("figure", editor=MplFigureEditor(), show_label=False)
    )

    @observe("model.filepath")
    def build_mpl_figure(self, event):
        figure = Figure()
        axes = figure.add_subplot(111)
        data = imageio.imread(self.model.filepath)
        axes.imshow(data)
        self.figure = figure
