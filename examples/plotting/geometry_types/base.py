from abc import ABC, abstractmethod

import numpy as np
import pyvista as pv


class GeometryType(ABC):
    def __init__(self, ds, geom_container, **kwargs):
        self.ds = ds
        self.geom_container = geom_container
        self.data = None
        self.load(**kwargs)

    def get_coordinate_from_standard_name(self, coordinates_name, standard_name):
        # FIXME: This is not a nice way to deal with standard coordinates, expensive
        coordinate_names = self.geom_container.attrs[coordinates_name].split()
        for coordinate_name in coordinate_names:
            coordinate = self.ds[coordinate_name]
            if coordinate.standard_name == standard_name:
                return coordinate.values
        raise KeyError(f"{standard_name} does not appear in {coordinates_name}.")

    def polyline_from_points(self, points):
        poly = pv.PolyData()
        poly.points = points
        cell = np.arange(0, len(points), dtype=np.int_)
        cell = np.insert(cell, 0, len(points))
        poly.lines = cell
        return poly

    def get_part_node_start_ends(self):
        node_count = self.ds[self.geom_container.node_count].values.astype(int)

        if "part_node_count" in self.geom_container.attrs:
            part_node_count = self.ds[self.geom_container.part_node_count].values
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

    @abstractmethod
    def load(self, **kwargs):
        pass

    @abstractmethod
    def plot(self, plotter):
        pass
