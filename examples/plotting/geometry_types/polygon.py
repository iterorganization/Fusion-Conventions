import logging

import numpy as np

from .base import GeometryType

logger = logging.getLogger(__name__)


class Polygon(GeometryType):
    def load(self, **kwargs):
        r = self.get_coordinate_from_standard_name(
            "node_coordinates", "_radial_distance"
        )
        phi = self.get_coordinate_from_standard_name("node_coordinates", "_azimuth")
        z = self.get_coordinate_from_standard_name(
            "node_coordinates", "_vertical_distance"
        )

        x = r * np.cos(phi)
        y = r * np.sin(phi)

        # NOTE: this is a bit annoying, is there a simpler way?
        node_count = self.ds[self.geom_container.node_count]
        offsets = node_count.values.cumsum()

        start = 0
        self.data = []
        for end in offsets:
            x_loop = x[start:end]
            y_loop = y[start:end]
            z_loop = z[start:end]
            start = end
            points = np.column_stack((x_loop, y_loop, z_loop))
            self.data.append(self.polyline_from_points(points))

    def plot(self, plotter):
        for polyline in self.data:
            plotter.add_mesh(polyline, line_width=3)
