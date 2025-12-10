import logging

import pyvista as pv
import xarray as xr

from geometry_types.poloidal_point import PoloidalPoint
from geometry_types.polygon import Polygon
from geometry_types.unit_vector import UnitVector

logger = logging.getLogger(__name__)


class Plotter:
    GEOMETRY_MAP = {
        "unit_vector": UnitVector,
        "polygon": Polygon,
        "poloidal_point": PoloidalPoint,
    }

    def __init__(self, dataset):
        self.ds = xr.open_dataset(
            dataset,
            engine="netcdf4",
        )
        self.plotter = pv.Plotter()

    def add(self, quantity_name):
        quantity = self.ds[quantity_name]
        geom_container = self.ds[quantity.geometry]

        geom_type = geom_container.geometry_type
        if geom_type not in self.GEOMETRY_MAP:
            logger.error(f"{geom_type} not in geometry map.")

        geometry_cls = self.GEOMETRY_MAP[geom_type]
        geometry = geometry_cls(self.ds, geom_container)
        geometry.plot(self.plotter)

    def show(self):
        self.plotter.show()
