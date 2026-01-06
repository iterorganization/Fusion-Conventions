import logging

import numpy as np
import pyvista as pv

from .base import GeometryType

logger = logging.getLogger(__name__)


class UnitVector(GeometryType):
    def load(self, **kwargs):
        r = self._get_coordinate_from_standard_name("_radial_distance")
        phi = self._get_coordinate_from_standard_name("_azimuth")
        z = self._get_coordinate_from_standard_name("_vertical_distance")

        pol_angle = self._get_coordinate_from_standard_name(
            "_normal_poloidal_angle", coordinates_name="node_orientations"
        )
        tor_angle = self._get_coordinate_from_standard_name(
            "_normal_toroidal_angle", coordinates_name="node_orientations"
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
        self._data = pv.PolyData(np.column_stack((x, y, z)))
        self._data["vectors"] = unit_vec

    def _plot_impl(self, plotter):
        plotter.add_arrows(
            self._data.points, self._data["vectors"], color="grey", mag=0.6
        )
        plotter.add_mesh(
            self._data,
            point_size=8,
            render_points_as_spheres=True,
        )
