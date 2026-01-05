import logging
from abc import ABC, abstractmethod

import numpy as np
import pyvista as pv

logger = logging.getLogger(__name__)


class GeometryType(ABC):
    def __init__(self, ds, geom_container):
        self._ds = ds
        self._geom_container = geom_container
        self._data = None

    def plot(self, plotter):
        """Plot the loaded geometry using a PyVista plotter.

        Args:
            plotter: The PyVista plotter.
        """
        if self._data is None:
            logger.error(
                "Cannot plot data, it must be loaded from the geometry container first"
            )
            return
        self._plot_impl(plotter)

    @abstractmethod
    def load(self, **kwargs):
        pass

    @abstractmethod
    def _plot_impl(self, plotter):
        pass

    def _get_coordinate_from_standard_name(self, coordinates_name, standard_name):
        """Retrieve coordinate values by its standard name.

        Args:
            coordinates_name: Attribute name listing coordinate variables.
            standard_name: Standard name to match.

        Returns:
            Numpy array of coordinate values.
        """
        # FIXME: Is there an easier way to deal with standard coordinates?
        coordinate_names = self._geom_container.attrs[coordinates_name].split()
        for coordinate_name in coordinate_names:
            coordinate = self._ds[coordinate_name]
            if coordinate.standard_name == standard_name:
                return coordinate.values
        raise KeyError(f"{standard_name} does not appear in {coordinates_name}.")

    def _polyline_from_points(self, points):
        """Create a PyVista polyline from ordered points.

        Args:
            points: Array of point coordinates.

        Returns:
            PyVista PolyData representing a polyline.
        """
        n = len(points)
        lines = np.empty(n + 1, dtype=np.int64)
        lines[0] = n
        lines[1:] = np.arange(n)

        poly = pv.PolyData(points)
        poly.lines = lines
        return poly

    def _get_part_node_start_ends(self):
        """Compute start and end indices for parts and nodes.

        Returns:
            Tuple of arrays: part starts, part ends, node starts, and node ends.
        """
        node_count = self._ds[self._geom_container.node_count].values

        if "part_node_count" in self._geom_container.attrs:
            part_node_count = self._ds[self._geom_container.part_node_count].values
        else:
            part_node_count = node_count

        part_node_ends = np.cumsum(part_node_count)
        node_ends = part_node_ends
        node_starts = np.concatenate([[0], node_ends[:-1]])

        geom_node_ends = np.cumsum(node_count)
        geom_part_ends = np.searchsorted(part_node_ends, geom_node_ends, side="right")

        part_ends = geom_part_ends
        part_starts = np.concatenate([[0], part_ends[:-1]])

        return part_starts, part_ends, node_starts, node_ends
