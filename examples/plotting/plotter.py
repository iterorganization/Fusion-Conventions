import logging

import pyvista as pv
import xarray as xr
from geometry_types.axisymmetric.poloidal_line import PoloidalLine
from geometry_types.axisymmetric.poloidal_point import PoloidalPoint
from geometry_types.axisymmetric.poloidal_polygon import PoloidalPolygon
from geometry_types.line import Line
from geometry_types.point import Point
from geometry_types.polygon import Polygon
from geometry_types.unit_vector import UnitVector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Plotter:
    GEOMETRY_MAP = {
        "unit_vector": UnitVector,
        "point": Point,
        # "line": Line, TODO: implement line geometry class
        "polygon": Polygon,
        "poloidal_point": PoloidalPoint,
        # "poloidal_line": PoloidalLine, #TODO: implement poloidal line geometry class
        "poloidal_polygon": PoloidalPolygon,
    }

    def __init__(self, filename):
        self.ds = xr.load_dataset(
            filename,
            engine="netcdf4",
        )
        self.plotter = pv.Plotter()
        geom_containers = self._find_geom_containers()
        logger.info(
            f"{filename} contains the following quantities with geometry containers:\n"
            f"{geom_containers}\n"
        )

    def add(self, quantity_name, **kwargs):
        quantity = self.ds[quantity_name]
        if "geometry" not in quantity.attrs:
            logger.error(f"{quantity.name} does not have a geometry container.")
            return

        geom_container = self.ds[quantity.geometry]
        geom_type = geom_container.geometry_type
        if geom_type not in self.GEOMETRY_MAP:
            logger.error(f"{geom_type!r} is not implemented for plotting.")
            return

        geometry_cls = self.GEOMETRY_MAP[geom_type]
        geometry = geometry_cls(self.ds, geom_container)
        geometry.load(**kwargs)
        geometry.plot(self.plotter)

    def show(self):
        self.plotter.show()

    def _find_geom_containers(self):
        return [
            name
            for name, da in self.ds.data_vars.items()
            if hasattr(da, "geometry") and da.geometry in self.ds
        ]
