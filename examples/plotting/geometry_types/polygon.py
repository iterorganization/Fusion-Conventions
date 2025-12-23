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

        # TODO:unify part_node_counts handling between all geometry classes
        part_starts, part_ends, node_starts, node_ends = self.get_part_node_start_ends()

        self.data = []

        for part_start, part_end in zip(part_starts, part_ends):
            parts = []
            for p in range(part_start, part_end):
                n0 = node_starts[p]
                n1 = node_ends[p]

                part_x = x[n0:n1]
                part_y = y[n0:n1]
                part_z = z[n0:n1]

                points = np.column_stack((part_x, part_y, part_z))
                polyline = self.polyline_from_points(points)

                parts.append(polyline)

            self.data.append(parts)

    def plot(self, plotter):
        if not self.data:
            logger.error("Geometry not loaded")
            return

        for parts in self.data:
            for part in parts:
                plotter.add_mesh(part, line_width=3)
