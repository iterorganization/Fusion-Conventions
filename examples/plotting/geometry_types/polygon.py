import logging

import numpy as np
import pyvista as pv

from geometry_types.base import GeometryType
from standard_names import AZIMUTH, RADIAL, VERTICAL

logger = logging.getLogger(__name__)


class Polygon(GeometryType):
    def load(self, **kwargs):
        r = self._get_coordinate_from_standard_name(RADIAL)
        phi = self._get_coordinate_from_standard_name(AZIMUTH)
        z = self._get_coordinate_from_standard_name(VERTICAL)

        # TODO: implement exterior/interior nodes

        x = r * np.cos(phi)
        y = r * np.sin(phi)

        for node_range in self._loop_over_parts():
            points = np.column_stack((x[node_range], y[node_range], z[node_range]))

            # Ensure polygon is closed
            if not np.allclose(points[0], points[-1]):
                points = np.vstack([points, points[0]])

            n = len(points)
            faces = np.hstack([[n], np.arange(n)])
            poly = pv.PolyData(points, faces)
            poly = poly.triangulate()
            self._data.append(poly)

    def _plot_impl(self, plotter, part):
        plotter.add_mesh(part, show_edges=True)
