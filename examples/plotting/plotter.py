import logging

import pyvista as pv
import xarray as xr

from geometry_types.poloidal_point import PoloidalPoint
from geometry_types.poloidal_polygon import PoloidalPolygon
from geometry_types.polygon import Polygon
from geometry_types.unit_vector import UnitVector

logger = logging.getLogger(__name__)


class Plotter:
    GEOMETRY_MAP = {
        "unit_vector": UnitVector,
        "polygon": Polygon,
        "poloidal_point": PoloidalPoint,
        "poloidal_polygon": PoloidalPolygon,
    }

    def __init__(self, dataset):
        self.ds = xr.open_dataset(
            dataset,
            engine="netcdf4",
        )
        self.plotter = pv.Plotter()
        logger.debug(self.ds)

    def add(self, quantity_name, **kwargs):
        quantity = self.ds[quantity_name]
        try:
            geom_container = self.ds[quantity.geometry]
        except AttributeError:
            logger.error(f"{quantity.name} does not have a geometry container")
            return

        geom_type = geom_container.geometry_type
        if geom_type not in self.GEOMETRY_MAP:
            logger.error(f"{geom_type} not in geometry map.")

        geometry_cls = self.GEOMETRY_MAP[geom_type]
        geometry = geometry_cls(self.ds, geom_container, **kwargs)
        geometry.plot(self.plotter)

    def show(self):
        self.plotter.show()
