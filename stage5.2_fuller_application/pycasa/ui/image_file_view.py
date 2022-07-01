# General imports
from matplotlib.figure import Figure
from matplotlib import patches

# ETS imports
from traits.api import Button, Instance, observe
from traitsui.api import HGroup, Item, ModelView, Spring, View

# Local imports
from ets_tutorial.util.mpl_figure_editor import MplFigureEditor
from ..model.image_file import ImageFile


class ImageFileView(ModelView):
    """ ModelView for an image file object.
    """
    model = Instance(ImageFile)

    figure = Instance(Figure)

    detect_button = Button("Detect faces")

    view = View(
        Item("model.filepath", style="readonly", show_label=False),
        Item("figure", editor=MplFigureEditor(), show_label=False),
        HGroup(
            Spring(),
            Item("detect_button", show_label=False),
            Spring(),
        ),
    )

    @observe("model.filepath")
    def build_mpl_figure(self, event):
        figure = Figure()
        axes = figure.add_subplot(111)
        axes.imshow(self.model.to_array())
        self.figure = figure

    def _detect_button_fired(self):
        self.model.detect_faces()

    @observe("model.faces")
    def update_mpl_figure_with_faces(self, events):
        [axis] = self.figure.get_axes()
        for face in self.model.faces:
            axis.add_patch(
                patches.Rectangle(
                    (face['c'], face['r']),
                    face['width'],
                    face['height'],
                    fill=False,
                    color='r',
                    linewidth=2
                )
            )
        # Update the figure.
        self.figure.canvas.draw_idle()
        self.figure.canvas.flush_events()
