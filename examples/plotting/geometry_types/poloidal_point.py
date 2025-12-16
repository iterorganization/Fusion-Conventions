import logging

import numpy as np

from .base import GeometryType

logger = logging.getLogger(__name__)


class PoloidalPoint(GeometryType):
    def load(self, *, num_phi=20, max_phi=360, **kwargs):
        r = self.get_coordinate_from_standard_name(
            "node_coordinates", "_radial_distance"
        )
        z = self.get_coordinate_from_standard_name(
            "node_coordinates", "_vertical_distance"
        )

        phis = np.linspace(0, np.radians(max_phi), num_phi, endpoint=True)
        self.data = []

        for i in range(len(r)):
            x_i = r[i] * np.cos(phis)
            y_i = r[i] * np.sin(phis)
            z_i = np.full_like(phis, z[i])
            points = np.column_stack((x_i, y_i, z_i))
            self.data.append(self.polyline_from_points(points))

    def plot(self, plotter):
        if not self.data:
            logger.error(
                "Cannot plot data, it must be loaded from the geometry container first"
            )
            return
        for polyline in self.data:
            plotter.add_mesh(polyline, line_width=3)
