# (C) Copyright 2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE_Enthought.txt and may be redistributed only
# under the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

data = collect_data_files("kiva")
hiddenimports = collect_submodules("kiva")
