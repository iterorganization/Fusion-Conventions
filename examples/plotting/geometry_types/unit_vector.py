import logging

import numpy as np
import pyvista as pv

from .base import GeometryType

logger = logging.getLogger(__name__)


class UnitVector(GeometryType):
    def load(self, **kwargs):
        r = self.get_coordinate_from_standard_name(
            "node_coordinates", "_radial_distance"
        )
        phi = self.get_coordinate_from_standard_name("node_coordinates", "_azimuth")
        z = self.get_coordinate_from_standard_name(
            "node_coordinates", "_vertical_distance"
        )

        pol_angle = self.get_coordinate_from_standard_name(
            "node_orientations", "_normal_poloidal_angle"
        )
        tor_angle = self.get_coordinate_from_standard_name(
            "node_orientations", "_normal_toroidal_angle"
        )
        # FIXME: Sometimes angles are not filled, but they should
        if pol_angle is None:
            pol_angle = np.zeros_like(r)
        if tor_angle is None:
            tor_angle = np.zeros_like(r)

        # Convert from cylindrical to cartesian
        x = r * np.cos(phi)
        y = r * np.sin(phi)

        # FIXME: This should be verified, perhaps no phi?
        dx = np.cos(pol_angle) * np.cos(phi + tor_angle)
        dy = np.cos(pol_angle) * np.sin(phi + tor_angle)
        dz = -np.sin(pol_angle)

        vec = np.column_stack((dx, dy, dz))
        norm = np.linalg.norm(vec, axis=1)
        unit_vec = vec / norm[:, None]

        # Plot unit vectors as points plus direction vector
        self.data = pv.PolyData(np.column_stack((x, y, z)))
        self.data["vectors"] = unit_vec

    def plot(self, plotter):
        if not self.data:
            logger.error(
                "Cannot plot data, it must be loaded from the geometry container first"
            )
            return
        plotter.add_arrows(
            self.data.points, self.data["vectors"], color="grey", mag=0.6
        )
        plotter.add_mesh(
            self.data,
            point_size=8,
            render_points_as_spheres=True,
        )
