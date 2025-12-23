import logging

import numpy as np
import pyvista as pv

from .base import GeometryType

logger = logging.getLogger(__name__)


class Point(GeometryType):
    def load(self, **kwargs):
        r = self.get_coordinate_from_standard_name(
            "node_coordinates", "_radial_distance"
        )
        phi = self.get_coordinate_from_standard_name("node_coordinates", "_azimuth")
        z = self.get_coordinate_from_standard_name(
            "node_coordinates", "_vertical_distance"
        )
        self.data = []

        for i in range(len(r)):
            x_i = r[i] * np.cos(phi[i])
            y_i = r[i] * np.sin(phi[i])
            z_i = z[i]

            points = np.column_stack((x_i, y_i, z_i))
            self.data.append(pv.PolyData(points))

    def plot(self, plotter):
        if not self.data:
            logger.error(
                "Cannot plot data, it must be loaded from the geometry container first"
            )
            return
        for polydata in self.data:
            plotter.add_mesh(
                polydata,
                render_points_as_spheres=True,
                point_size=6,
            )
