from pathlib import Path

import numpy as np
from plotter import Plotter


def main():
    # TODO: Make the example data available
    DATA_PATH = Path("../../data")
    # ITER
    ## Magnetics
    iter_magnetics = Plotter(DATA_PATH / "ITER/iter-md-magnetics_geom_container.nc")
    iter_magnetics.add("b_field_pol_probe.field.data")
    iter_magnetics.add("b_field_phi_probe.field.data")
    iter_magnetics.add("flux_loop.flux")
    iter_magnetics.show()

    ## PF Active
    iter_pf_active = Plotter(DATA_PATH / "ITER/iter-pf-active-111001_geom_container.nc")
    iter_pf_active.add("coil.resistance", num_phi=30, max_phi=np.pi)
    iter_pf_active.show()

    # WEST
    plotter_west = Plotter(DATA_PATH / "WEST/west-57929_geom_container.nc")
    plotter_west.add("b_field_pol_probe.field.data")
    plotter_west.add("b_field_tor_probe.field.data")
    plotter_west.add("flux_loop.flux", num_phi=20, max_phi=3 / 2 * np.pi)
    plotter_west.show()

    # MAST
    plotter_mast = Plotter(DATA_PATH / "MAST/mast_magnetics-30421_geom_container.nc")
    plotter_mast.add("b_field_tor_probe_cc_field")
    plotter_mast.add("b_field_pol_probe_cc_field_adjs")
    plotter_mast.add("b_field_tor_probe_saddle_field")
    plotter_mast.show()


if __name__ == "__main__":
    main()
