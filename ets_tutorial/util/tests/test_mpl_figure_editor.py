import unittest

import numpy as np
from matplotlib.figure import Figure
from traits.api import HasTraits, Instance
from traitsui.api import Item, View
from traitsui.testing.api import UITester, IsVisible

from ets_tutorial.util.mpl_figure_editor import MplFigureEditor


class Plot(HasTraits):
    figure = Instance(Figure, ())

    view = View(
        Item("figure", editor=MplFigureEditor(), show_label=False),
        resizable=True
    )

    def _figure_default(self):
        figure = Figure()
        axes = figure.add_subplot(111)
        time = np.linspace(0, 2 * np.pi, 200)
        axes.plot(
            np.sin(time) * (1 + 0.5 * np.cos(11 * time)),
            np.cos(time) * (1 + 0.5 * np.cos(11 * time)),
        )
        return figure


class TestMplFigureEditor(unittest.TestCase):
    def test_mpl_figure_editor(self):
        tester = UITester()
        plot = Plot()
        with tester.create_ui(plot) as ui:
            # smoke test: just check if Plot can create its UI
            figure = tester.find_by_name(ui, "figure")
            figure.inspect(IsVisible())
