import logging

import numpy as np

from .base import GeometryType

logger = logging.getLogger(__name__)


class PoloidalPolygon(GeometryType):
    def load(self, *, max_phi=270, num_phi=20, **kwargs):
        r = self.get_coordinate_from_standard_name(
            "node_coordinates", "_radial_distance"
        )
        z = self.get_coordinate_from_standard_name(
            "node_coordinates", "_vertical_distance"
        )

        node_count = self.ds[self.geom_container.node_count].values
        part_node_count = self.ds[self.geom_container.part_node_count].values

        geom_node_ends = np.cumsum(node_count)
        part_node_ends = np.cumsum(part_node_count)

        geom_part_ends = np.searchsorted(part_node_ends, geom_node_ends, side="right")

        part_starts = np.concatenate([[0], geom_part_ends[:-1]])
        part_ends = geom_part_ends

        node_starts = np.concatenate([[0], part_node_ends[:-1]])
        node_ends = part_node_ends

        self.data = []

        for part_start, part_end in zip(part_starts, part_ends):
            parts = []

            for p in range(part_start, part_end):
                n0 = node_starts[p]
                n1 = node_ends[p]

                ring_r = r[n0:n1]
                ring_z = z[n0:n1]

                # Ensure rings are closed
                ring_r = np.append(ring_r, ring_r[0])
                ring_z = np.append(ring_z, ring_z[0])

                points = np.column_stack([ring_r, np.zeros_like(ring_r), ring_z])

                polyline = self.polyline_from_points(points)

                surface = polyline.extrude_rotate(
                    angle=max_phi,
                    resolution=num_phi,
                    rotation_axis=(0, 0, 1),
                    capping=True,
                )

                parts.append(surface)

            self.data.append(parts)

    def plot(self, plotter):
        if not self.data:
            logger.error("Geometry not loaded")
            return

        for parts in self.data:
            for surface in parts:
                plotter.add_mesh(surface, opacity=1.0, show_edges=True)
