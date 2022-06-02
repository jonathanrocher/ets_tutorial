# General imports
from matplotlib.figure import Figure

# ETS imports
from traits.api import Instance, observe
from traitsui.api import Item, ModelView, View

# Local imports
from ets_tutorial.util.mpl_figure_editor import MplFigureEditor
from pycasa.model.image_file import ImageFile


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
        axes.imshow(self.model.to_array())
        self.figure = figure


if __name__ == '__main__':
    from os.path import dirname, join
    import ets_tutorial

    TUTORIAL_DIR = dirname(ets_tutorial.__file__)
    SAMPLE_IMG_DIR = join(TUTORIAL_DIR, "..", "sample_images")
    SAMPLE_IMG1 = join(SAMPLE_IMG_DIR, "IMG-0311_xmas_2020.JPG")

    image_file = ImageFile(filepath=SAMPLE_IMG1)
    view = ImageFileView(model=image_file)
    view.configure_traits()
