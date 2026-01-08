import logging

import numpy as np

from geometry_types.base import GeometryType
from standard_names import AZIMUTH, RADIAL, VERTICAL

logger = logging.getLogger(__name__)


class Line(GeometryType):
    def load(self, **kwargs):
        r = self._get_coordinate_from_standard_name(RADIAL)
        phi = self._get_coordinate_from_standard_name(AZIMUTH)
        z = self._get_coordinate_from_standard_name(VERTICAL)

        x = r * np.cos(phi)
        y = r * np.sin(phi)

        for node_range in self._loop_over_parts():
            points = np.column_stack((x[node_range], y[node_range], z[node_range]))
            polyline = self._polyline_from_points(points)
            self._data.append(polyline)

    def _plot_impl(self, plotter, part):
        plotter.add_mesh(part, show_edges=True)
