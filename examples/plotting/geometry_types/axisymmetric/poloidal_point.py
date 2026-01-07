import logging

import numpy as np
import pyvista as pv

from geometry_types.base import GeometryType
from standard_names import RADIAL, VERTICAL

logger = logging.getLogger(__name__)


class PoloidalPoint(GeometryType):
    def load(self, *, max_phi=2 * np.pi, num_phi=20, **kwargs):
        """Load poloidal points and generate toroidally extruded surfaces.

        Args:
            max_phi: Maximum toroidal angle for extrusion.
            num_phi: Number of segments in the toroidal direction.
        """

        r = self._get_coordinate_from_standard_name(RADIAL)
        z = self._get_coordinate_from_standard_name(VERTICAL)

        for r_i, z_i in zip(r, z, strict=True):
            polyline = pv.PolyData([[r_i, 0.0, z_i]])
            surface = polyline.extrude_rotate(
                angle=np.degrees(max_phi),
                resolution=num_phi,
                capping=False,
            )
            self._data.append(surface)

    def _plot_impl(self, plotter, part):
        plotter.add_mesh(part, line_width=3)
