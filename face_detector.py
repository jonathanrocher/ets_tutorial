from collections import namedtuple
from chaco.api import AbstractOverlay, ArrayPlotData, Plot
from enable.api import ColorTrait, ComponentEditor
from skimage import data
from skimage.feature import Cascade
from traits.api import ArrayOrNone, Float, HasTraits, Instance, Int
from traitsui.api import Item, View


FaceRectangle = namedtuple(
    'FaceRectangle', ['anchor_point', 'width', 'height']
)


class FaceOverlay(AbstractOverlay):
    """ Draws a rectangle around a detected face.
    """

    #: Anchor point of the rectangle in data space. This point is one of the
    #: corners of the rectangle in data space, depending on the direction of
    #: the axes and the sign of width and height. If width and height are
    #: positive, and the origin is at the bottom left, this is the bottom left
    #: corner of the rectangle.
    anchor_point = ArrayOrNone()

    #: Width of the rectangle in data space.
    width = Float()

    #: Height of the rectangle in data space.
    height = Float()

    #: Rectangle border color
    border_color = ColorTrait("red")

    #: Rectangle border thickness
    border_thickness = Int(8)

    def overlay(self, component, gc, view_bounds=None, mode="normal"):
        bottom_left = component.map_screen(self.anchor_point)
        top_right = component.map_screen([
            self.anchor_point[0] + self.width,
            self.anchor_point[1] + self.height
        ])
        with gc:
            gc.set_stroke_color(self.border_color_)
            gc.set_line_width(self.border_thickness)
            self._add_rect_from_corners(gc, bottom_left, top_right)
            gc.stroke_path()

    def _add_rect_from_corners(self, gc, bottom_left, top_right):
        width = top_right[0] - bottom_left[0]
        height = top_right[1] - bottom_left[1]
        gc.rect(bottom_left[0], bottom_left[1], width, height)


class FaceDetector(HasTraits):

    #: Chaco plot for rendering the source image.
    plot = Instance(Plot)

    #: Image on which faces are to be detected.
    image = ArrayOrNone()

    traits_view = View(
        Item('plot', editor=ComponentEditor(), show_label=False),
        title="Face Detector"
    )

    def _image_default(self):
        return data.astronaut()

    def _plot_default(self):
        plot_data = ArrayPlotData(imagedata=self.image)
        plot = Plot(plot_data, default_origin="top left")
        plot.img_plot("imagedata")
        for face in self.detect_faces():
            face_overlay = FaceOverlay(
                anchor_point=face.anchor_point,
                width=face.width,
                height=face.height,
            )
            plot.overlays.append(face_overlay)
        return plot

    def detect_faces(self):
        """ Finds bounding rectangles for each human face in the image.

        Returns
        -------
        List[FaceRectangle]

        """
        # Load the trained file from the module root.
        trained_file = data.lbp_frontal_face_cascade_filename()
        # Initialize the detector cascade.
        detector = Cascade(trained_file)
        faces = detector.detect_multi_scale(
            img=self.image,
            scale_factor=1.2,
            step_ratio=1,
            min_size=(60, 60),
            max_size=(123, 123)
        )
        return [
            FaceRectangle(
                anchor_point=[face['c'], face['r'] + face['height']],
                width=face['width'],
                height=-face['height']
            ) for face in faces
        ]


if __name__ == '__main__':
    FaceDetector().configure_traits()
