import logging

import numpy as np
import pyvista as pv

from .base import GeometryType

logger = logging.getLogger(__name__)


class Point(GeometryType):
    def load(self, **kwargs):
        r = self._get_coordinate_from_standard_name(
            "node_coordinates", "_radial_distance"
        )
        phi = self._get_coordinate_from_standard_name("node_coordinates", "_azimuth")
        z = self._get_coordinate_from_standard_name(
            "node_coordinates", "_vertical_distance"
        )
        x = r * np.cos(phi)
        y = r * np.sin(phi)

        points = np.column_stack((x, y, z))
        self._data = pv.PolyData(points)

    def _plot_impl(self, plotter):
        plotter.add_mesh(
            self._data,
            render_points_as_spheres=True,
            point_size=6,
        )
