# General imports

# ETS imports
import numpy as np
import pandas as pd
from traits.api import Bool, Button, Enum, Instance, List, observe
from traitsui.api import HGroup, Item, Label, ListStrEditor, ModelView, \
    Spring, VGroup, View
from traitsui.ui_editors.data_frame_editor import DataFrameEditor

# Local imports
from ..model.image_folder import FILENAME_COL, ImageFolder, NUM_FACE_COL


DISPLAYED_COLUMNS = [FILENAME_COL, NUM_FACE_COL] + [
    'ApertureValue', 'ExifVersion', 'Model', 'Make', 'LensModel', 'DateTime',
    'ShutterSpeedValue', 'ExposureTime', 'XResolution', 'YResolution',
    'Orientation', 'GPSInfo', 'DigitalZoomRatio', 'FocalLengthIn35mmFilm',
    'ISOSpeedRatings', 'SceneType'
]


class ImageFolderView(ModelView):
    """ ModelView for an image folder object.
    """
    model = Instance(ImageFolder)

    scan = Button("Scan for faces...")

    # Filters widgets
    view_filter_controls = Bool

    filtered_data = Instance(pd.DataFrame)

    year_mask = Instance(pd.Series)

    selected_years = List

    all_years = List

    selected_make = Enum(["All", "Canon", "Nikon", "Sony", "Apple", "samsung"])

    make_mask = Instance(pd.Series)

    def traits_view(self):
        view = View(
            Item("model.path", style="readonly", show_label=False),
            HGroup(
                Spring(),
                Item("view_filter_controls"),
            ),
            HGroup(
                Item("all_years", label="Years",
                     editor=ListStrEditor(selected="selected_years",
                                          multi_select=True)
                     ),
                Item("selected_make", label="Camera make"),
                visible_when="view_filter_controls",
            ),
            Item("filtered_data",
                 editor=DataFrameEditor(columns=DISPLAYED_COLUMNS,
                                        update="data_updated"),
                 show_label=False, visible_when="len(model.data) > 0"),
            HGroup(
                Spring(),
                Label("No images found. No data to show"),
                Spring(),
                visible_when="len(model.data) == 0",
            ),
            HGroup(
                Spring(),
                Item("scan", show_label=False,
                     enabled_when="len(model.data) > 0"),
                Spring(),
            ),
            resizable=True, height=800
        )
        return view

    # Listener methods --------------------------------------------------------

    @observe("scan")
    def scan_for_faces(self, event):
        self.model.compute_num_faces()

    @observe("selected_years")
    def update_years(self, event):
        self.year_mask = self.model.data['Year'].isin(self.selected_years)

    @observe("selected_make")
    def update_make(self, event):
        if self.selected_make == "All":
            self.make_mask = pd.Series(np.ones(len(self.model.data),
                                               dtype=bool))
        else:
            self.make_mask = self.model.data['Make'] == self.selected_make

    @observe("year_mask, make_mask")
    def update_filtered_data(self, event):
        self.filtered_data = self.model.data[self.year_mask & self.make_mask]

    # Initialization methods --------------------------------------------------

    def _make_mask_default(self):
        return pd.Series(np.ones(len(self.model.data), dtype=bool))

    def _year_mask_default(self):
        return pd.Series(np.ones(len(self.model.data), dtype=bool))

    def _filtered_data_default(self):
        return self.model.data

    def _all_years_default(self):
        def parse_year(x):
            return x.split(":")[0] if isinstance(x, str) else "unknown"

        self.model.data['Year'] = self.model.data['DateTime'].apply(parse_year)
        return sorted(self.model.data['Year'].unique().tolist())


if __name__ == '__main__':
    from os.path import dirname, join
    import ets_tutorial

    TUTORIAL_DIR = dirname(ets_tutorial.__file__)
    SAMPLE_IMG_DIR = join(TUTORIAL_DIR, "..", "sample_images")

    image_file = ImageFolder(directory=SAMPLE_IMG_DIR)
    view = ImageFolderView(model=image_file)
    view.configure_traits()