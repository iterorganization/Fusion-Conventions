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

    @abstractmethod
    def load(self, **kwargs):
        pass

    @abstractmethod
    def plot(self, plotter):
        pass
