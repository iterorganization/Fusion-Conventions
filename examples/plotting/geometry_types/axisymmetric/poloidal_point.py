import logging

import numpy as np
import pyvista as pv

from ..base import GeometryType

logger = logging.getLogger(__name__)


class PoloidalPoint(GeometryType):
    def load(self, *, max_phi=2 * np.pi, num_phi=20, **kwargs):
        r = self._get_coordinate_from_standard_name(
            "node_coordinates", "_radial_distance"
        )
        z = self._get_coordinate_from_standard_name(
            "node_coordinates", "_vertical_distance"
        )

        self._data = []

        for r_i, z_i in zip(r, z, strict=True):
            polyline = pv.PolyData([[r_i, 0.0, z_i]])
            surface = polyline.extrude_rotate(
                angle=np.degrees(max_phi),
                resolution=num_phi,
                capping=False,
            )
            self._data.append(surface)

    def _plot_impl(self, plotter):
        for polyline in self._data:
            plotter.add_mesh(polyline, line_width=3)
