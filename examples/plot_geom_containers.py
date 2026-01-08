# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "numpy",
#   "pyvista",
#   "xarray",
#   "netCDF4",
# ]
# ///

"""
Examples for plotting different 3D geometries from NetCDF files enriched with geometry
containers using PyVista.

Handles the following geometry types:
- unit_vector
- point
- line
- polygon
- poloidal_point
- poloidal_line
- poloidal_polygon
"""

import logging
from pathlib import Path

import numpy as np
import pyvista as pv
import xarray as xr

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Standard names for coordinates
RADIAL = "_radial_distance"
VERTICAL = "_vertical_distance"
AZIMUTH = "_azimuth"
POL_ANGLE = "_normal_poloidal_angle"
TOR_ANGLE = "_normal_toroidal_angle"


def get_coordinate_from_standard_name(
    dataset, geom_container, standard_name, coordinates_name="node_coordinates"
):
    """Retrieve coordinate values by its standard name."""
    coordinate_names = geom_container.attrs[coordinates_name].split()
    for coordinate_name in coordinate_names:
        coordinate = dataset[coordinate_name]
        if coordinate.standard_name == standard_name:
            return coordinate.values
    raise KeyError(f"{standard_name} does not appear in {coordinates_name}.")


def polyline_from_points(points):
    """Create a PyVista polyline from ordered points."""
    n = len(points)
    lines = np.empty(n + 1, dtype=np.int64)
    lines[0] = n
    lines[1:] = np.arange(n)
    return pv.PolyData(points, lines=lines)


def loop_over_parts(dataset, geom_container):
    """Generate slices corresponding to node ranges for each part."""
    node_count = dataset[geom_container.node_count].values

    if "part_node_count" in geom_container.attrs:
        part_node_count = dataset[geom_container.part_node_count].values
    else:
        part_node_count = node_count

    node_idx = 0
    for count in part_node_count:
        next_node_idx = node_idx + count
        yield slice(node_idx, next_node_idx)
        node_idx = next_node_idx


def plot_unit_vector(plotter, dataset, geom_container):
    """Plot unit_vector geometry."""
    r = get_coordinate_from_standard_name(dataset, geom_container, RADIAL)
    phi = get_coordinate_from_standard_name(dataset, geom_container, AZIMUTH)
    z = get_coordinate_from_standard_name(dataset, geom_container, VERTICAL)

    pol_angle = get_coordinate_from_standard_name(
        dataset, geom_container, POL_ANGLE, coordinates_name="node_orientations"
    )
    tor_angle = get_coordinate_from_standard_name(
        dataset, geom_container, TOR_ANGLE, coordinates_name="node_orientations"
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

    polydata = pv.PolyData(np.column_stack((x, y, z)))
    polydata["vectors"] = unit_vec

    plotter.add_arrows(polydata.points, polydata["vectors"], color="grey", mag=0.6)
    plotter.add_mesh(polydata, point_size=8, render_points_as_spheres=True)


def plot_point(plotter, dataset, geom_container):
    """Plot point geometry."""
    r = get_coordinate_from_standard_name(dataset, geom_container, RADIAL)
    phi = get_coordinate_from_standard_name(dataset, geom_container, AZIMUTH)
    z = get_coordinate_from_standard_name(dataset, geom_container, VERTICAL)

    x = r * np.cos(phi)
    y = r * np.sin(phi)

    points = np.column_stack((x, y, z))
    polydata = pv.PolyData(points)

    plotter.add_mesh(polydata, render_points_as_spheres=True, point_size=6)


def plot_line(plotter, dataset, geom_container):
    """Plot line geometry."""
    r = get_coordinate_from_standard_name(dataset, geom_container, RADIAL)
    phi = get_coordinate_from_standard_name(dataset, geom_container, AZIMUTH)
    z = get_coordinate_from_standard_name(dataset, geom_container, VERTICAL)

    x = r * np.cos(phi)
    y = r * np.sin(phi)

    for node_range in loop_over_parts(dataset, geom_container):
        points = np.column_stack((x[node_range], y[node_range], z[node_range]))
        polyline = polyline_from_points(points)
        plotter.add_mesh(polyline, show_edges=True, line_width=3)


def plot_polygon(plotter, dataset, geom_container):
    """Plot polygon geometry."""
    r = get_coordinate_from_standard_name(dataset, geom_container, RADIAL)
    phi = get_coordinate_from_standard_name(dataset, geom_container, AZIMUTH)
    z = get_coordinate_from_standard_name(dataset, geom_container, VERTICAL)

    x = r * np.cos(phi)
    y = r * np.sin(phi)

    for node_range in loop_over_parts(dataset, geom_container):
        points = np.column_stack((x[node_range], y[node_range], z[node_range]))

        # Ensure polygon is closed
        if not np.allclose(points[0], points[-1]):
            points = np.vstack([points, points[0]])

        n = len(points)
        faces = np.hstack([[n], np.arange(n)])
        poly = pv.PolyData(points, faces)
        poly = poly.triangulate()
        plotter.add_mesh(poly, show_edges=True)


def plot_poloidal_point(plotter, dataset, geom_container):
    """Plot poloidal_points geometry."""
    r = get_coordinate_from_standard_name(dataset, geom_container, RADIAL)
    z = get_coordinate_from_standard_name(dataset, geom_container, VERTICAL)

    for r_i, z_i in zip(r, z, strict=True):
        polyline = pv.PolyData([[r_i, 0.0, z_i]])
        surface = polyline.extrude_rotate(angle=180, capping=False)
        plotter.add_mesh(surface, line_width=3)


def plot_poloidal_line(plotter, dataset, geom_container):
    """Plot poloidal_line geometry."""
    r = get_coordinate_from_standard_name(dataset, geom_container, RADIAL)
    z = get_coordinate_from_standard_name(dataset, geom_container, VERTICAL)

    for node_range in loop_over_parts(dataset, geom_container):
        line_r = r[node_range]
        line_z = z[node_range]

        points = np.column_stack([line_r, np.zeros_like(line_r), line_z])
        polyline = polyline_from_points(points)

        surface = polyline.extrude_rotate(angle=180, capping=False)
        plotter.add_mesh(surface, show_edges=True)


def plot_poloidal_polygon(plotter, dataset, geom_container):
    """Plot poloidal_polygon geometry."""
    r = get_coordinate_from_standard_name(dataset, geom_container, RADIAL)
    z = get_coordinate_from_standard_name(dataset, geom_container, VERTICAL)

    for node_range in loop_over_parts(dataset, geom_container):
        ring_r = r[node_range]
        ring_z = z[node_range]

        # Ensure rings are closed
        ring_r = np.append(ring_r, ring_r[0])
        ring_z = np.append(ring_z, ring_z[0])

        points = np.column_stack([ring_r, np.zeros_like(ring_r), ring_z])
        polyline = polyline_from_points(points)

        surface = polyline.extrude_rotate(angle=180, capping=False)
        plotter.add_mesh(surface, show_edges=True)


def find_geom_containers(dataset):
    """Find all variables that have an associated geometry container.

    Returns:
        List of variable names that have an associated geometry container.
    """
    return [
        name
        for name, data_array in dataset.data_vars.items()
        if hasattr(data_array, "geometry") and data_array.geometry in dataset
    ]


GEOMETRY_PLOTTER_FUNCTIONS = {
    "unit_vector": plot_unit_vector,
    "point": plot_point,
    "line": plot_line,
    "polygon": plot_polygon,
    "poloidal_point": plot_poloidal_point,
    "poloidal_line": plot_poloidal_line,
    "poloidal_polygon": plot_poloidal_polygon,
}


def add_quantity_to_plot(plotter, dataset, quantity_name):
    """Add a quantity from an Xarray dataset to the plot based on its geometry
    container.

    Args:
        plotter: The PyVista plotter object to add the quantity to.
        dataset: The Xarray dataset.
        quantity_name: Name of the data variable to plot.
    """
    quantity = dataset[quantity_name]
    if "geometry" not in quantity.attrs:
        logger.error(f"{quantity.name} does not have a geometry container.")
        return

    geom_container = dataset[quantity.geometry]
    geom_type = geom_container.geometry_type

    if geom_type not in GEOMETRY_PLOTTER_FUNCTIONS:
        logger.error(f"{geom_type!r} is not implemented for plotting.")
        return

    plotter_function = GEOMETRY_PLOTTER_FUNCTIONS[geom_type]
    plotter_function(plotter, dataset, geom_container)


def plot(filename, quantities):
    """Plot quantities from a NetCDF dataset.

    Args:
        filename: Path to NetCDF file
        quantities: List of quantities to plot
    """
    dataset = xr.load_dataset(filename, engine="netcdf4")
    logger.info(
        f"{filename} contains the following quantities with geometry containers:\n"
        f"{find_geom_containers(dataset)}\n"
    )

    plotter = pv.Plotter()

    for quantity_name in quantities:
        add_quantity_to_plot(plotter, dataset, quantity_name)

    plotter.show()


def main():
    # TODO: Make the example data available
    DATA_PATH = Path("../data")

    # ITER Magnetics
    plot(
        DATA_PATH / "ITER/iter-md-magnetics_geom_container.nc",
        [
            "b_field_pol_probe.field.data",
            "b_field_phi_probe.field.data",
            "flux_loop.flux",
        ],
    )

    # ITER PF Active
    plot(
        DATA_PATH / "ITER/iter-pf-active-111001_geom_container.nc",
        ["coil.resistance"],
    )

    # ITER Wall and Divertor
    plot(
        DATA_PATH / "ITER/iter-first-wall-and-divertor-116000_geom_container.nc",
        ["description_2d.limiter", "description_2d.vessel"],
    )

    # WEST
    plot(
        DATA_PATH / "WEST/west-57929_geom_container.nc",
        [
            "b_field_pol_probe.field.data",
            "b_field_tor_probe.field.data",
            "flux_loop.flux",
        ],
    )

    # MAST
    plot(
        DATA_PATH / "MAST/mast_magnetics-30421_geom_container.nc",
        [
            "b_field_tor_probe_cc_field",
            "b_field_pol_probe_cc_field_adjs",
            "b_field_tor_probe_saddle_field",
        ],
    )


if __name__ == "__main__":
    main()
