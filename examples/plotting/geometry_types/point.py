import logging

import numpy as np
import pyvista as pv

from geometry_types.base import GeometryType
from standard_names import AZIMUTH, RADIAL, VERTICAL

logger = logging.getLogger(__name__)


class Point(GeometryType):
    def load(self, **kwargs):
        r = self._get_coordinate_from_standard_name(RADIAL)
        phi = self._get_coordinate_from_standard_name(AZIMUTH)
        z = self._get_coordinate_from_standard_name(VERTICAL)
        x = r * np.cos(phi)
        y = r * np.sin(phi)

        points = np.column_stack((x, y, z))
        self._data.append(pv.PolyData(points))

    def _plot_impl(self, plotter, part):
        plotter.add_mesh(
            part,
            render_points_as_spheres=True,
            point_size=6,
        )
