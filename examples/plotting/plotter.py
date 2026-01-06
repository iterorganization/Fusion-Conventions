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
        "poloidal_line": PoloidalLine,
        "poloidal_polygon": PoloidalPolygon,
    }

    def __init__(self, filename):
        """Initialize the plotter and load a NetCDF dataset.

        Args:
            filename: Path to a NetCDF file
        """
        self._dataset = xr.load_dataset(
            filename,
            engine="netcdf4",
        )
        self._plotter = pv.Plotter()
        logger.info(
            f"{filename} contains the following quantities with geometry containers:\n"
            f"{self._find_geom_containers()}\n"
        )

    def add(self, quantity_name, **kwargs):
        """Add a quantity to the plot based on its geometry container.

        Args:
            quantity_name: Name of the data variable to plot.
            **kwargs: Arguments passed through to the geometry loader.
        """
        quantity = self._dataset[quantity_name]
        if "geometry" not in quantity.attrs:
            logger.error(f"{quantity.name} does not have a geometry container.")
            return

        geom_container = self._dataset[quantity.geometry]
        geom_type = geom_container.geometry_type
        if geom_type not in self.GEOMETRY_MAP:
            logger.error(f"{geom_type!r} is not implemented for plotting.")
            return

        geometry_cls = self.GEOMETRY_MAP[geom_type]
        geometry = geometry_cls(self._dataset, geom_container)
        geometry.load(**kwargs)
        geometry.plot(self._plotter)

    def show(self):
        """Render the current plot."""
        self._plotter.show()

    def _find_geom_containers(self):
        """Find all variables that have an associated geometry container.

        Returns:
            List of variable names that have an associated geometry container.
        """

        return [
            name
            for name, data_array in self._dataset.data_vars.items()
            if hasattr(data_array, "geometry") and data_array.geometry in self._dataset
        ]
