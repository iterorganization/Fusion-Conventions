import logging

import numpy as np

from geometry_types.base import GeometryType
from standard_names import RADIAL, VERTICAL

logger = logging.getLogger(__name__)


class PoloidalPolygon(GeometryType):
    def load(self, *, max_phi=2 * np.pi, num_phi=20, **kwargs):
        """Load poloidal polygon geometry and extrude it toroidally.

        Args:
            max_phi: Maximum toroidal angle for extrusion.
            num_phi: Number of segments in the toroidal direction.
        """
        r = self._get_coordinate_from_standard_name(RADIAL)
        z = self._get_coordinate_from_standard_name(VERTICAL)

        # TODO: implement exterior/interior nodes
        part_starts, part_ends, node_starts, node_ends = (
            self._get_part_node_start_ends()
        )

        for part_start, part_end in zip(part_starts, part_ends):
            for p in range(part_start, part_end):
                n0 = node_starts[p]
                n1 = node_ends[p]

                ring_r = r[n0:n1]
                ring_z = z[n0:n1]

                # Ensure rings are closed
                ring_r = np.append(ring_r, ring_r[0])
                ring_z = np.append(ring_z, ring_z[0])

                points = np.column_stack([ring_r, np.zeros_like(ring_r), ring_z])

                polyline = self._polyline_from_points(points)

                surface = polyline.extrude_rotate(
                    angle=np.degrees(max_phi),
                    resolution=num_phi,
                    capping=False,
                )

                self._data.append(surface)

    def _plot_impl(self, plotter, part):
        plotter.add_mesh(part, show_edges=True)
