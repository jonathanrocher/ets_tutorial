# General imports

# ETS imports
import numpy as np
import pandas as pd
from traits.api import Bool, Button, Enum, Instance, List, observe
from traitsui.api import HGroup, Item, Label, ListStrEditor, ModelView, \
    Spring, View
from traitsui.ui_editors.data_frame_editor import DataFrameEditor

# Local imports
from pycasa.model.image_folder import FILENAME_COL, ImageFolder, NUM_FACE_COL


DISPLAYED_COLUMNS = [FILENAME_COL, NUM_FACE_COL] + [
    'ApertureValue', 'ExifVersion', 'Model', 'Make', 'LensModel', 'DateTime',
    'ShutterSpeedValue', 'ExposureTime', 'XResolution', 'YResolution',
    'Orientation', 'GPSInfo', 'DigitalZoomRatio', 'FocalLengthIn35mmFilm',
    'ISOSpeedRatings', 'SceneType'
]

YEAR_KEY = "__year__"

DATETIME_COL = "DateTime"

MAKE_COL = 'Make'


class ImageFolderView(ModelView):
    """ ModelView for an image folder object.
    """
    model = Instance(ImageFolder)

    scan = Button("Scan for faces...")

    # Filters widgets
    view_filter_controls = Bool

    # Copy of the model's data, with filtering columns added if missing
    all_data = Instance(pd.DataFrame)

    # Filtered dataframe based on filtering widgets
    filtered_data = Instance(pd.DataFrame)

    year_mask = Instance(pd.Series)

    selected_years = List

    all_years = List

    selected_make = Enum(["All", "Canon", "Nikon", "Sony", "Apple", "samsung"])

    make_mask = Instance(pd.Series)

    def traits_view(self):
        view = View(
            Item("model.directory", style="readonly", show_label=False),
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
        )
        return view

    # Listener methods --------------------------------------------------------

    @observe("scan")
    def scan_for_faces(self, event):
        self.model.compute_num_faces()
        self.all_data.update(self.model.data)

    @observe("selected_years")
    def update_years(self, event):
        self.year_mask = self.all_data[YEAR_KEY].isin(self.selected_years)

    @observe("selected_make")
    def update_make(self, event):
        if self.selected_make == "All":
            self.make_mask = pd.Series([True] * len(self.model.data))
        else:
            self.make_mask = self.all_data[MAKE_COL] == self.selected_make

    @observe("year_mask, make_mask, all_data")
    def update_filtered_data(self, event):
        self.filtered_data = self.all_data[self.year_mask & self.make_mask]

    # Initialization methods --------------------------------------------------

    def _make_mask_default(self):
        return pd.Series(np.ones(len(self.model.data), dtype=bool))

    def _year_mask_default(self):
        return pd.Series(np.ones(len(self.model.data), dtype=bool))

    def _all_data_default(self):
        # Enrich metadata with missing fields: date time, make
        data = self.model.data.copy()

        if DATETIME_COL not in data.columns:
            data[DATETIME_COL] = np.nan

        if MAKE_COL not in data.columns:
            data[MAKE_COL] = np.nan

        def parse_year(x):
            return x.split(":")[0] if isinstance(x, str) else "unknown"
        data[YEAR_KEY] = data[DATETIME_COL].apply(parse_year)

        return data

    def _filtered_data_default(self):
        return self.all_data

    def _all_years_default(self):
        return sorted(self.all_data[YEAR_KEY].unique().tolist())


if __name__ == '__main__':
    from os.path import dirname, join
    import ets_tutorial

    TUTORIAL_DIR = dirname(ets_tutorial.__file__)
    SAMPLE_IMG_DIR = join(TUTORIAL_DIR, "..", "sample_images")

    image_file = ImageFolder(directory=SAMPLE_IMG_DIR)
    view = ImageFolderView(model=image_file)
    view.configure_traits()
