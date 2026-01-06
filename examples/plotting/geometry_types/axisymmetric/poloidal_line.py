import logging

import numpy as np

from geometry_types.base import GeometryType

logger = logging.getLogger(__name__)


class PoloidalLine(GeometryType):
    def load(self, *, max_phi=2 * np.pi, num_phi=20, **kwargs):
        """Load poloidal points and generate toroidally extruded surfaces.

        Args:
            max_phi: Maximum toroidal angle for extrusion.
            num_phi: Number of segments in the toroidal direction.
        """
        r = self._get_coordinate_from_standard_name("_radial_distance")
        z = self._get_coordinate_from_standard_name("_vertical_distance")

        for node_range in self._loop_over_parts():
            line_r = r[node_range]
            line_z = z[node_range]

            points = np.column_stack([line_r, np.zeros_like(line_r), line_z])

            polyline = self._polyline_from_points(points)

            surface = polyline.extrude_rotate(
                angle=np.degrees(max_phi),
                resolution=num_phi,
                capping=False,
            )
            self._data.append(surface)

    def _plot_impl(self, plotter, part):
        plotter.add_mesh(part, show_edges=True)
