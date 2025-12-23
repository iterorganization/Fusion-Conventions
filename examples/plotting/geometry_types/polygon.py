import logging

import numpy as np
import pyvista as pv

from .base import GeometryType

logger = logging.getLogger(__name__)


class Polygon(GeometryType):
    def load(self, **kwargs):
        r = self._get_coordinate_from_standard_name(
            "node_coordinates", "_radial_distance"
        )
        phi = self._get_coordinate_from_standard_name("node_coordinates", "_azimuth")
        z = self._get_coordinate_from_standard_name(
            "node_coordinates", "_vertical_distance"
        )

        # TODO: implement exterior/interior nodes

        x = r * np.cos(phi)
        y = r * np.sin(phi)

        # TODO: unify part_node_counts handling between all geometry classes
        part_starts, part_ends, node_starts, node_ends = (
            self._get_part_node_start_ends()
        )

        self._data = []

        for part_start, part_end in zip(part_starts, part_ends):
            parts = []
            for p in range(part_start, part_end):
                n0 = node_starts[p]
                n1 = node_ends[p]
                points = np.column_stack((x[n0:n1], y[n0:n1], z[n0:n1]))

                # Ensure polygon is closed
                if not np.allclose(points[0], points[-1]):
                    points = np.vstack([points, points[0]])

                n = len(points)
                faces = np.hstack([[n], np.arange(n)])
                poly = pv.PolyData(points, faces)
                poly = poly.triangulate()
                parts.append(poly)

            self._data.append(parts)

    def _plot_impl(self, plotter):
        for parts in self._data:
            for part in parts:
                plotter.add_mesh(part)
