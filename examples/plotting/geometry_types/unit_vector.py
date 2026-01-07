import logging

import numpy as np
import pyvista as pv

from geometry_types.base import GeometryType
from standard_names import AZIMUTH, POL_ANGLE, RADIAL, TOR_ANGLE, VERTICAL

logger = logging.getLogger(__name__)


class UnitVector(GeometryType):
    def load(self, **kwargs):
        r = self._get_coordinate_from_standard_name(RADIAL)
        phi = self._get_coordinate_from_standard_name(AZIMUTH)
        z = self._get_coordinate_from_standard_name(VERTICAL)

        pol_angle = self._get_coordinate_from_standard_name(
            POL_ANGLE, coordinates_name="node_orientations"
        )
        tor_angle = self._get_coordinate_from_standard_name(
            TOR_ANGLE, coordinates_name="node_orientations"
        )

        x = r * np.cos(phi)
        y = r * np.sin(phi)

        # FIXME: This should be verified
        dx = np.cos(pol_angle) * np.cos(phi + tor_angle)
        dy = np.cos(pol_angle) * np.sin(phi + tor_angle)
        dz = -np.sin(pol_angle)

        vec = np.column_stack((dx, dy, dz))
        norm = np.linalg.norm(vec, axis=1, keepdims=True)
        unit_vec = vec / norm

        # Plot unit vectors as points plus direction vector
        polydata = pv.PolyData(np.column_stack((x, y, z)))
        polydata["vectors"] = unit_vec
        self._data.append(polydata)

    def _plot_impl(self, plotter, part):
        plotter.add_arrows(part.points, part["vectors"], color="grey", mag=0.6)
        plotter.add_mesh(
            part,
            point_size=8,
            render_points_as_spheres=True,
        )
